#!/usr/bin/env python
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import pdfquery
from spacy.pipeline import EntityRuler
import spacy

from io import StringIO
import os
import sys
import re
import csv

def pdf2text(path, number=None):
    """
    Given a PDF and a possible page number, extract the text.
    """
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    device = TextConverter(rsrcmgr, retstr, codec='utf-8', laparams=LAParams())
    with open(path, 'rb') as fp:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        pagenos=set()
        allpages = PDFPage.get_pages(fp, pagenos, maxpages=0, password='', caching=True, check_extractable=False)
        if not number:
            for page in allpages:
                interpreter.process_page(page)
        else:
            for index, page in enumerate(allpages):
                if index == number:
                    interpreter.process_page(page)
        text = retstr.getvalue()
        # text = text.replace('\u00a0', ' ') # no-break space
        # text = text.replace('\u000c', ' ') # vertical tab
    device.close()
    retstr.close()
    return text

def pdf2textCached(filename):
    """
    Cache PDF text if it exists: this speeds up program execution.
    """
    textfilename = filename + '.txt'
    if not os.path.isfile(textfilename):
        text = pdf2text(filename)
        with open(textfilename, 'w+') as fd:
            fd.write(text)
    return '\n'.join(open(textfilename, 'r+').readlines())

def expand_audit_numbers(doc):
    """
    We cannot use a conventional pipe here, because spacy sometimes
    parses 2xxx-yyy as a single entity (DATE or CARDINAL). Here, we
    explicitly match against a regexp and create custom spans; as
    such, this function _must_ be the first pipe executed, otherwise
    we will get overlapping entities for the same token.
    """
    new_ents = []
    for match in re.finditer('2\d{3}-\d{3}', doc.text):
        start, end = match.span()
        span = doc.char_span(start, end, label='AUDIT_NUMBER')
        if span is not None:
            new_ents.append(span)
    doc.ents = new_ents
    return doc

def sentences(doc, what):
    """
    Given a document with named entities, extract the sentence
    belonging to the named entity.
    """
    return [ent.sent for ent in doc.ents if ent.label_ == what]

def clean(s):
    result = s.strip().replace('\n', ' ')
    while '  ' in result:
        result = result.replace('  ', ' ')
    return result

def paragraphs(doc, what, startswith=False, experimental=False):
    """
    Given a document with named entities, extract the paragraph
    belonging to the named entity.
    """
    start = False
    overflow = 0
    current_audit = None
    current_sentence = ''
    sentences = []
    for sent in doc.sents:
        labels = [ent.label_ for ent in sent.ents]
        if 'AUDIT_NUMBER' in labels:
            index = labels.index('AUDIT_NUMBER')
            current_audit = sent.ents[index].text
        if what in labels:
            if experimental:
                # experimental: if we have a secondary then we likely
                # accidentally hit the audit finding itself.
                if set(labels).intersection(set(secondaries)):
                    continue
            text = sent.text
            if startswith:
                index = labels.index(what)
                start = sent.ents[index].start
                text = doc[start:sent.end].text
            current_sentence = text
            start = True
            overflow = 0
        else:
            if start:
                if not '\n\n\n' in sent.text:
                    current_sentence += sent.text
                    overflow += 1
                else:
                    sentences.append((current_audit, clean(current_sentence)))
                    current_sentence = ''
                    start = False
                    overflow = 0
                if overflow > 20:
                    # prevent excessively large text dumps
                    sentences.append((current_audit, (clean(current_sentence))))
                    current_sentence = ''
                    start = False
                    overflow = 0
    return sentences

def get_page_limit(sentence, limit=50):
    """
    Assume a page is approximately `limit` words. We could do better by
    leveraging PDF parsing here.
    """
    rest = sentence.doc[sentence.start:]
    # index = rest.text.find('\n\n')
    # return sentence.start + index
    words = rest.text.split(' ')
    length = len(words)
    if length > limit: words = words[0:limit]
    return len(' '.join(words))

def extract_findings(doc):
    """
    Given a header, examine the relevant context and see if we have a
    finding on our hands. This is a quick and dirty heuristic: we want
    to over-capture here.
    """
    findings = []
    for sentence in sentences(doc, 'HEADER'):
        limit = sentence.start + get_page_limit(sentence)
        captured_audit = []
        count = 0
        for ent in doc.ents:
            if ent.start > sentence.start and ent.end < limit:
                if ent.label_ in secondaries:
                    count += 1
                if ent.label_ in ['AUDIT_NUMBER']:
                    # we almost certainly have a finding if we have a
                    # header followed by an audit number
                    count += 3
                    captured_audit.append(ent.text)
        if count > 3:
            finding = clean(doc[sentence.start:limit].text)
            findings.append((captured_audit, finding))
    return findings

def nlp_results(doc):
    return [(ent.text.strip(), ent.label_) for ent in doc.ents]

def audit_numbers(doc):
    return {ent.text for ent in doc.ents if ent.label_ == 'AUDIT_NUMBER'}

def split_pattern(string):
    return [{'LOWER': s} for s in string.split(' ')]

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print('usage: ', sys.argv[0], '<file.pdf>', '<page?>')
    sys.exit(1)

# a sample of different headers that start audit findings
headers = [
    'federal award findings and questioned costs',
    'financial statement findings',
    'findings and questioned costs – major federal award programs audit',
    'findings – financial statement audit',
    'findings related to the financial statements'
    'major federal award findings and questioned costs',
    'schedule of findings and questioned costs',
    'summary schedule of prior audit findings',
]

# phrases that may indicate CAP text
corrective_actions = [
    'corrective action',
    'corrective action plan',
    'planned corrective actions',
    'planned corrective action'
]

patterns = [
    # secondary criteria: used to identify where the audit is
    {'label': 'CONDITION', 'pattern': [{'LOWER': 'observation'}]},
    {'label': 'CONDITION', 'pattern': [{'LOWER': 'condition'}]},
    {'label': 'CRITERIA', 'pattern': [{'LOWER': 'criteria'}]},
    {'label': 'CRITERIA', 'pattern': split_pattern('criteria or specific requirement')},
    {'label': 'CONTEXT', 'pattern': [{'LOWER': 'context'}]},
    {'label': 'CAUSE', 'pattern': [{'LOWER': 'cause'}]},
    {'label': 'CAUSE', 'pattern': split_pattern('cause of the condition')},
    {'label': 'EFFECT', 'pattern': [{'LOWER': 'effect'}]},
    {'label': 'EFFECT', 'pattern': split_pattern('effect or possible effect')},
    {'label': 'RECOMMENDATION', 'pattern': [{'LOWER': {'REGEX': 'recommendations?'}}]},
    {'label': 'RESPONSE', 'pattern': [{'LOWER': 'response'}]},
]

secondaries = [pattern["label"] for pattern in patterns]

for header in headers:
    pattern = {'label': 'HEADER', 'pattern': split_pattern(header)}
    patterns.append(pattern)

for cap in corrective_actions:
    pattern = {'label': 'CORRECTIVE_ACTION', 'pattern': split_pattern(cap)}
    patterns.append(pattern)

nlp = spacy.load('en_core_web_sm') # or 'en'
ruler = EntityRuler(nlp, overwrite_ents=True)
sentencizer = nlp.create_pipe('sentencizer')
ruler.add_patterns(patterns)
nlp.add_pipe(sentencizer, first=True)
nlp.add_pipe(expand_audit_numbers, first=True)
nlp.add_pipe(ruler)

filename = sys.argv[1]
outputfile = sys.argv[2] if len(sys.argv) == 3 else 'test.csv'
pagenumber = None # int(sys.argv[2]) if len(sys.argv) == 3 else None
sample = pdf2textCached(filename) if not pagenumber else pdf2text(filename, number=pagenumber)
doc = nlp(sample)
audits = audit_numbers(doc)
if not audits:
    print('No audit numbers found; it is likely this PDF has no findings.')
    sys.exit(1)

findings = paragraphs(doc, 'HEADER', startswith=True)
caps = paragraphs(doc, 'CORRECTIVE_ACTION', startswith=True)

with open(outputfile, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['Associated Audit Number(s)', 'Audit Findings', 'Corrective Action Plan'])
    for finding, cap in zip(findings, caps):
        (_, finding_text) = finding
        (audits, cap_text) = cap
        writer.writerow([audits, finding_text, cap_text])

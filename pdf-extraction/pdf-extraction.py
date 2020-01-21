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

def sentences(doc, text, what, startwith=False):
    """
    Given a document with named entities, extract the sentence
    belonging to the named entity.
    """
    result = []
    for index, ent in enumerate(doc.ents):
        if ent.label_ == what:
            sentence = ent.sent.string
            # make sure we start with the given text
            if startwith and not sentence.startswith(ent.text):
                index = sentence.index(ent.text)
                sentence = sentence[index:]
            # replace whitespace and newlines
            sentence = sentence.strip().replace('\n', '')
            result.append(sentence)
    return result

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

def nlp_results(doc):
    return [(ent.text.strip(), ent.label_) for ent in doc.ents]

def audit_numbers(doc):
    return {ent.text for ent in doc.ents if ent.label_ == 'AUDIT_NUMBER'}

def split_pattern(string):
    return [{'LOWER': s} for s in string.split(' ')]

if len(sys.argv) != 2 and len(sys.argv) != 3:
    print('usage: ', sys.argv[0], '<file.pdf>', '<page?>')
    sys.exit(1)

patterns = [
    # primary criteria
    {'label': 'CORRECTIVE_ACTION', 'pattern': split_pattern('corrective action plan')},
    {'label': 'CORRECTIVE_ACTION', 'pattern': split_pattern('corrective action')},
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

nlp = spacy.load('en_core_web_sm') # or 'en'
ruler = EntityRuler(nlp, overwrite_ents=True)
sentencizer = nlp.create_pipe('sentencizer')
ruler.add_patterns(patterns)
nlp.add_pipe(sentencizer, first=True)
nlp.add_pipe(expand_audit_numbers, first=True)
nlp.add_pipe(ruler)

filename = sys.argv[1]
pagenumber = int(sys.argv[2]) if len(sys.argv) == 3 else None
sample = pdf2textCached(filename) if not pagenumber else pdf2text(filename, number=pagenumber)
doc = nlp(sample)
audits = audit_numbers(doc)
if not audits:
    print('No audit numbers found; it is likely this PDF has no findings.')
    sys.exit(1)

print('found the following audit numbers:', audits)

print('*** sentence extracts')
for pattern in ['CORRECTIVE_ACTION', 'AUDIT_NUMBER']:
    print(pattern, sentences(doc, sample, pattern))
print('*** end sentence extracts')

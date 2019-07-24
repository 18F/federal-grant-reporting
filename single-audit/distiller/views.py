import os
from io import StringIO

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

import pandas as pd
import mechanicalsoup

from .forms import AgencySelectionForm, __get_agency_name_from_prefix, __is_valid_agency_prefix

# @todo: Update this to actually download the file from the FAC. We'll get there.
#        https://harvester.census.gov/facdissem/PublicDataDownloads.aspx
#        Do it on some cached ongoing basis so you're not making people wait for
#        a 500-MB download.
directory_name = 'single_audit_data_dump'
files_directory = os.path.join(settings.BASE_DIR, 'distiller', directory_name)

# @todo: Improve the naming here and make it more possible for it to be
#        extendable to different kinds of URLs.
fac_url = 'https://harvester.census.gov/facdissem/SearchA133.aspx'

current_fiscal_year = '2018'  # @todo: Encapsulate this in a proper function.


def download_pdfs_from_fac(agency_prefix='20'):
    # @todo: Put this in a function and call it from somewhere, no? Just update the
    #        function named in urls.py. (Then you can refactor to use a template.)
    browser = mechanicalsoup.StatefulBrowser()
    # 1. Go to https://harvester.census.gov/facdissem/SearchA133.aspx
    browser.open(fac_url)
    # browser.get_current_page().find_all('legend')  # ...nah.
    browser.select_form('form[action="./SearchA133.aspx"]')  # @todo: Check whether that period is necessary. It's in the source code, but.

    # Just for actively working on this: gets the form field options.
    browser.get_current_form().print_summary()

    # [SEEMS UNNECESSARY] 2. Click the “General Information” accordion, if you must. (May be unnecessary.)
    # 3. Select “2018” checkbox under “Fiscal Year (Required)”.

    # For radio buttons, well, it’s simple too: radio buttons have several input tag with the same name and different values, just select the one you need ("size" is the name attribute, "medium" is the "value" attribute of the element we want to tick):
    # browser['ctl00$MainContent$UcSearchFilters$FYear$CheckableItems$1'] = current_fiscal_year
#      Can't assign. Figure out what that's about.
    browser['ctl00$MainContent$UcSearchFilters$FYear$CheckableItems$1'] = '2018'

    # 3b. ...and deselect the "All Years" checkbox.
    browser['ctl00$MainContent$UcSearchFilters$FYear$CheckableItems$0'] = '0'

    # (@todo: Come to think of it, check: do they want to filter by fiscal year? Or do
    # they just want everything that's come in recently, fiscal year be damned?
    # Probably the latter...)

    # 4. TO CUT DOWN ON OVERLOAD: Try entering [7 days ago] and today into the “FAC Release Date” fields (“From” and “To,” respectively).
    #     ex: 07/16/2019, 07/23/2019. Must be MM/DD/YYYY.
    # @todo: circle back and update this to actually calculate the "From" date.
    browser['ctl00$MainContent$UcSearchFilters$DateProcessedControl$FromDate'] = '07/16/2019'
    browser['ctl00$MainContent$UcSearchFilters$DateProcessedControl$ToDate'] = '07/23/2019'

    # [SEEMS UNNECESSARY] 5. Click the ‘Federal Awards’ accordion, if you must. (Ditto.)
    # 6. Under “Federal Agencies with Current or Prior Year Audit Findings on Direct Awards”, select [as described above. In the case of DOT, we’ll start with ’20’.]
    browser['ctl00$MainContent$UcSearchFilters$FedAgency$CheckableItems$22'] = '20'
    # browser['ctl00$MainContent$UcSearchFilters$FedAgency$CheckableItems$22'] = agency_prefix
    #       I agree, it's strange that this is "CheckableItems22" when the value is 20. Not a typo though. (And 22 is probably pure order.)

    # First, let's check our work. (Just during development. @todo: Remove when done, or leave commented-out with documented notes for future troubleshooting.)
    browser.get_current_form().print_summary()  # or, sure, you can try browser.launch_browser().

    # 7. Click the ‘Search’ button.
    response = browser.submit_selected(btnName='ctl00$MainContent$UcSearchFilters$btnSearch_bottom')  # @todo: Modify this to submit the
    #                                       #        SPECIFIC select button.
    #
    # name="ctl00$MainContent$UcSearchFilters$btnSearch_bottom" value="Search"

    # (It does indeed have an onClick, so... maybe you'll need to switch to Selenium
    # after all.)

    # For temporary debugging:
    html = response.text
    print(html)
    # @todo: finish, and move this to the end. But just for now:
    return HttpResponse(html)

    # 8. A new page loads. Click the ‘I acknowledge that I have read and understand the above statements’ checkbox.
    # 9. Click the ‘Continue to Search Results’ button.#

    # (Oh, this is better! Because it gives you the summary report too, as a link: “Download Summary Report”) [@todo: Include.]#

    # 10. [@todo: Determine whether or not you need to use the “Selected Audit Reports” dropdown — specifically, how to handle having more than one page of results and how best to “select” those for download.]#

    # 11. Click the ‘Download Audits’ button.#

    # 12. Hit ‘Save’! You’ve got your download, a ZIP file of PDFs. :) And... a cross-reference filename spreadsheet. :shrug:

    # @todo: Update this method to return something appropriate.
    # @todo: Document it too.


def prompt_for_agency_name(request):
    if request.method == 'POST':
        form = AgencySelectionForm(request.POST)

        if form.is_valid():
            #cd = form.cleaned_data
            #agency_prefix = cd['agency']
            # @todo: Run the calculations here instead?
            pass

    else:
        form = AgencySelectionForm()

    return render(request, 'distiller/index.html', {'form': form})


def __get_findings(agency_df):
    '''
    Takes:
        A dataframe of agency data, currently derived from genXX.txt.

    Returns:
        A dataframe of findings, or 'None'.

    Room for improvement:
        Modify this function to retrieve the cross-referenced findings instead
        of just 'Y/N'.
    '''

    try:
        findings_df = agency_df.loc[agency_df['CYFINDINGS'] == 'Y']
        return findings_df

    except:
        # @todo: Figure out what exception to actually raise here.
        Exception(" Error generating findings dataframe.")


def __get_number_of_findings(agency_df):
    '''
    Takes:
        A dataframe of agency data, currently derived from genXX.txt.

    Returns:
        An integer, or 'None'.
    '''

    try:
        findings_df = __get_findings(agency_df)
        return len(findings_df.index)

    except:
        Exception(" Error getting number of findings.")


def filter_general_table_by_agency(agency_prefix, filename="gen18.txt"):
    actual_filename = files_directory + '/' + filename

    # Not using the index for anything, so let's leave it arbitrary for now.
    df = pd.read_csv(actual_filename, low_memory=False, encoding='latin-1')

    agency_df = df.loc[df['COGAGENCY'] == agency_prefix]

    return agency_df


# @todo: clean up the naming here.
def generate_csv_download(dataframe, results_filename='agency-specific-results.csv'):
    # Use a buffer so we can prompt the user to download the file.
    new_csv = StringIO()

    dataframe.to_csv(new_csv, encoding='utf-8', index=False)
    # Rewind the buffer so we don't get a zero-length error.
    new_csv.seek(0)

    response = HttpResponse(new_csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s"' % results_filename

    return response


def offer_download_of_agency_specific_csv(request, agency_prefix='20'):
    agency_df = filter_general_table_by_agency(agency_prefix)

    response = generate_csv_download(agency_df)

    return response


def derive_agency_highlights(agency_prefix, filename='gen18.txt'):
    agency_df = filter_general_table_by_agency(agency_prefix)

    highlights = {  # or "overview"
        'agency_prefix': agency_prefix,
        'agency_name': __get_agency_name_from_prefix(agency_prefix),
        'filename': filename,
        'results': {
            'cognizant_sum': len(agency_df.index),
            'findings': __get_number_of_findings(agency_df),
        }
        # 'cog_or_oversight': [_____]  # @todo: Think through and add this later.
    }

    return highlights


def show_agency_level_summary(request):
    agency_prefix = request.POST['agency']
    try:
        __is_valid_agency_prefix(agency_prefix)
        highlights = derive_agency_highlights(agency_prefix)

        return render(request, 'distiller/results.html', highlights)

    except:
        ValueError("That doesn't seem to be a valid federal agency prefix.")


def extract_findings_from_pdf():
    # @todo: Rework this to actually show something. For now, just log to console.
    # @todo: Rework this to be more dynamic. For now, start with parsing just
    # one PDF and expand from there.



    return findings

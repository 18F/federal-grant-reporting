import os
import time  # for use with selenium; may or may not need it.
from io import StringIO

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select

from .forms import AgencySelectionForm, __get_agency_name_from_prefix, __is_valid_agency_prefix

# @todo: Update this to actually download the file from the FAC. We'll get there.
#        https://harvester.census.gov/facdissem/PublicDataDownloads.aspx
#        Do it on some cached ongoing basis so you're not making people wait for
#        a 500-MB download.
DIRECTORY_NAME = 'single_audit_data_dump'
FILES_DIRECTORY = os.path.join(settings.BASE_DIR, 'distiller', DIRECTORY_NAME)
DEPT_OF_TRANSPORTATION_PREFIX = '20'

CHROME_DRIVER_LOCATION = os.path.join(settings.BASE_DIR, 'distiller', 'chromedriver')

# Received from FTA on July 29, 2019 for testing.
# @todo at some point: figure out how to automatically update them. But at
#                      minimum/as an interim measure, the user can enter them
#                      manually.
#
# @todo: Check whether searching for "20.5*" pulls up the same list. Dante
#        confirmed that 20.5 is FTA.
#
# @todo at some point: See where you might be able to find a lookup of subagencies.
#                      You already have the initial agency prefixes.
CFDA_NUMBERS = (
    20.500,
    20.505,
    20.507,
    20.509,
    20.513,
    20.514,
    20.516,
    20.518,
    20.519,
    20.520,
    20.521,
    20.522,
    20.523,
    20.524,
    20.525,
    20.526,
    20.527,
    20.528,
    20.529,
    20.530,
    20.531,
    )

# @todo: Improve the naming here and make it more possible for it to be
#        extendable to different kinds of URLs.
FAC_URL = 'https://harvester.census.gov/facdissem/SearchA133.aspx'

current_fiscal_year = '2018'  # @todo: Encapsulate this in a proper function.


def download_pdfs_from_fac(agency_prefix=DEPT_OF_TRANSPORTATION_PREFIX):
    # @todo: Refactor urls.py, etc. to call this via the appropriate template.

<<<<<<< HEAD
    # Setting subagency_extension default to DOT FTA for testing and demo purposes.
    # @todo: Revisit this once you have an actual CFDA-to-subagency lookup table.
=======
    # From https://realpython.com/modern-web-automation-with-python-and-selenium/:
    # from selenium.webdriver import Firefox
    # from selenium.webdriver.firefox.options import Options
    # opts = Options()
    # opts.set_headless()
    # assert opts.headless  # Operating in headless mode
    # browser = Firefox(options=opts)

    # From https://duo.com/decipher/driving-headless-chrome-with-python:
#    from selenium.webdriver.common.keys import Keys
#    from selenium.webdriver.chrome.options import Options

#    chrome_options = Options()
#    chrome_options.add_argument("--headless")
#   # @todo: Update for deployed location, presumably.
#   # @todo: Check whether you can just pull some of what you used for functional testing already.
>>>>>>> 3d4fa50... Replace magic number with a named constant

    # @todo: LOOK INTO CHROME DRIVER SERVICE and how you'd use that on cloud.govself.

    driver = webdriver.Chrome(CHROME_DRIVER_LOCATION)  # Optional argument, if not specified will search path.

    # 1. Go to https://harvester.census.gov/facdissem/SearchA133.aspx
    driver.get(FAC_URL)
    time.sleep(5)  # ...just in case.

    # Just for actively working on this: gets the form field options.
#    browser.get_current_form().print_summary()

    # [SEEMS UNNECESSARY] 2. Click the “General Information” accordion, if you must. (May be unnecessary.)
    # 3. Select “2018” checkbox under “Fiscal Year (Required)”.
    #       name = ctl00$MainContent$UcSearchFilters$FYear$CheckableItems$1
    #       id = ctl00$MainContent$UcSearchFilters$FYear$CheckableItems$1
#    driver.find_element_by_name('ctl00$MainContent$UcSearchFilters$FYear$CheckableItems$1').click()
    checkbox_for_fy2018 = driver.find_element_by_name('ctl00$MainContent$UcSearchFilters$FYear$CheckableItems$1')
    print(checkbox_for_fy2018.get_property('name'))
    checkbox_for_fy2018.click()
    # @todo: Find out whether there's a performance or other reason to prefer
    # 'name' over 'id' or vice versa.

    # 3b. ...and deselect the "All Years" checkbox.
#    browser['ctl00$MainContent$UcSearchFilters$FYear$CheckableItems$0'] = '0'

    #driver.find_element_by_name('ctl00$MainContent$UcSearchFilters$FYear$CheckableItems$1').click()
#    all_years = Select(driver.find_element_by_name('ctl00$MainContent$UcSearchFilters$FYear$CheckableItems$1'))
#    all_years.deselect_all()

    #  select = Select(driver.find_element_by_id('id'))
    #  select.deselect_all()

    # (@todo: Come to think of it, check: do they want to filter by fiscal year? Or do
    # they just want everything that's come in recently, regardless of fiscal year?
    # Probably the latter...)

    # 4. TO CUT DOWN ON OVERLOAD: Try entering [7 days ago] and today into the “FAC Release Date” fields (“From” and “To,” respectively).
    #     ex: 07/16/2019, 07/23/2019. Must be MM/DD/YYYY.
    # @todo: circle back and update this to actually calculate the "From" date.
#    browser['ctl00$MainContent$UcSearchFilters$DateProcessedControl$FromDate'] = '07/16/2019'
#    browser['ctl00$MainContent$UcSearchFilters$DateProcessedControl$ToDate'] = '07/23/2019'

    # [SEEMS UNNECESSARY] 5. Click the ‘Federal Awards’ accordion, if you must. (Ditto.)
    # 6. Under “Federal Agencies with Current or Prior Year Audit Findings on Direct Awards”, select [as described above. In the case of DOT, we’ll start with ’20’.]
#    browser['ctl00$MainContent$UcSearchFilters$FedAgency$CheckableItems$22'] = '20'
    # browser['ctl00$MainContent$UcSearchFilters$FedAgency$CheckableItems$22'] = agency_prefix
    #       I agree, it's strange that this is "CheckableItems22" when the value is 20. Not a typo though. (And 22 is probably pure order.)

    # First, let's check our work. (Just during development. @todo: Remove when done, or leave commented-out with documented notes for future troubleshooting.)
#    browser.get_current_form().print_summary()  # or, sure, you can try browser.launch_browser().

    # 7. Click the ‘Search’ button.
#    response = browser.submit_selected(btnName='ctl00$MainContent$UcSearchFilters$btnSearch_bottom')  # @todo: Modify this to submit the
    #                                       #        SPECIFIC select button.
    #
    # name="ctl00$MainContent$UcSearchFilters$btnSearch_bottom" value="Search"
    # id="MainContent_UcSearchFilters_btnSearch_bottom"
    # @todo: Doublecheck whether you have to save an element before you can
    #        interact with it. Seems like you do.
    search_button = driver.find_element_by_id('MainContent_UcSearchFilters_btnSearch_bottom')
    search_button.click()

    # For temporary debugging:
#    html = response.text
#    print(html)
    # @todo: finish, and move this to the end. But just for now:
#    return HttpResponse(html)

    # 8. A new page loads. Click the ‘I acknowledge that I have read and understand the above statements’ checkbox.
    # 9. Click the ‘Continue to Search Results’ button.#

    # (Oh, this is better! Because it gives you the summary report too, as a link: “Download Summary Report”) [@todo: Include.]#

    # 10. [@todo: Determine whether or not you need to use the “Selected Audit Reports” dropdown — specifically, how to handle having more than one page of results and how best to “select” those for download.]#

        # @todo: Add error handling, for the very likely circumstance in which
        # more results are returned than can be handled.
        # assert "No results found." not in driver.page_source # <-- This isn't the right text to use, but it's an example.

    # 11. Click the ‘Download Audits’ button.

    # 12. Hit ‘Save’! You’ve got your download, a ZIP file of PDFs. :) And... a cross-reference filename spreadsheet. :shrug:

    # @todo: Update this method to return something appropriate.
    # @todo: Document it too.
    driver.quit()

    # @todo: Return a more appropriate HttpResponse.
    return HttpResponse("Done for now.", content_type="text/plain")


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


def offer_download_of_agency_specific_csv(request, agency_prefix=DEPT_OF_TRANSPORTATION_PREFIX):
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

    findings = True

    return findings

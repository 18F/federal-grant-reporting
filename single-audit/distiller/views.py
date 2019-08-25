import os
from datetime import date, timedelta
import time  # For use with Selenium. @todo: Replace with explicit waits
from io import StringIO

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from .forms import AgencySelectionForm, __get_agency_name_from_prefix, __is_valid_agency_prefix

# @todo: Update this to actually download the file from the FAC. We'll get there.
#        https://harvester.census.gov/facdissem/PublicDataDownloads.aspx
#        Do it on some cached ongoing basis so you're not making people wait for
#        a 500-MB download.
DIRECTORY_NAME = 'single_audit_data_dump'
FILES_DIRECTORY = os.path.join(settings.BASE_DIR, 'distiller', DIRECTORY_NAME)

CHROME_DRIVER_LOCATION = os.path.join(settings.BASE_DIR, 'distiller/chromedriver')
FAC_URL = 'https://harvester.census.gov/facdissem/SearchA133.aspx'

DEPT_OF_TRANSPORTATION_PREFIX = '20'
FTA_SUBAGENCY_CODE = '5'

# @todo: Improve the naming here and make it more possible for it to be
#        extendable to different kinds of URLs.
FAC_URL = 'https://harvester.census.gov/facdissem/SearchA133.aspx'

current_fiscal_year = '2018'  # @todo: Encapsulate this in a proper function.


def _calculate_start_date(time_difference=90, end_date=date.today()):
    """
    Calculate the date that's a certain number of days earlier than a given end
    date.

    Args:
        time_difference (int): non-negative integer representing how many days
                               earlier to calculate.

    Returns:
        A (date) string formatted appropriately for the Federal Audit Clearinghouse.
    """

    start_date = end_date - timedelta(time_difference)
    return _format_date_for_fac_fields(start_date)


def _format_date_for_fac_fields(date):
    """
    Format a date into a string that's consistent with the Federal Audit
    Clearinghouse's "from" and "to" date input requirements.

    Args:
        date (date): date object.

    Returns:
        A (date) string formatted for the Federal Audit Clearinghouse (MM/DD/YYYY).
    """

    return date.strftime("%m/%d/%Y")


# Setting subagency_extension default to DOT FTA for testing and demo purposes.
# @todo: Revisit this once you have an actual CFDA-to-subagency lookup table.
def download_pdfs_from_fac(agency_prefix=DEPT_OF_TRANSPORTATION_PREFIX,
                           subagency_extension=FTA_SUBAGENCY_CODE):
    """
    Search the Federal Audit Clearinghouse for relevant single audits, then
    download the results.

    Args:
        agency_prefix (string): a string representation of a two-digit integer
                                corresponding to a federal agency. These can be
                                found on the Federal Audit Clearinghouse itself.

        subagency_extension (string): a string representation of a one-digit
                                      integer representing a subagency's prefix.
                                      @todo: Replace this with a direct CFDA
                                             lookup soon, having learned that
                                             though subagencies' prefixes
                                             reliably map to CFDA numbers in
                                             some agencies, that's not the case
                                             in all agencies.

    Returns:
        A (date) string formatted for the Federal Audit Clearinghouse (MM/DD/YYYY).
    """

    driver = webdriver.Chrome(CHROME_DRIVER_LOCATION)  # Optional argument, if not specified will search path.

    # 1. Go to the Federal Audit Clearinghouse's search page.
    driver.get(FAC_URL)
    time.sleep(2)  # ...just in case.

    # 2. Click the “General Information” accordion. Otherwise Selenium will
    #    throw an "Element Not Interactable" exception.
    driver.find_element_by_id('ui-id-1').click()

    # 3. To get all recent results, enter [90 days ago] and today into the
    #    “FAC Release Date” fields (“From” and “To,” respectively).
    from_date_field = driver.find_element_by_id('MainContent_UcSearchFilters_DateProcessedControl_FromDate')

    from_date = _calculate_start_date(90)
    from_date_field.clear()
    from_date_field.send_keys(from_date)
    from_date_field.send_keys(Keys.RETURN)

    to_date = _format_date_for_fac_fields(date.today())
    to_date_field = driver.find_element_by_id('MainContent_UcSearchFilters_DateProcessedControl_ToDate')
    to_date_field.clear()
    to_date_field.send_keys(to_date)
    to_date_field.send_keys(Keys.RETURN)

    # 4. Click the ‘Federal Awards’ accordion, so the elements under it will be
    #    'interactable.'
    driver.find_element_by_id('ui-id-5').click()

    # 5. Search by CFDA number:
    driver.find_element_by_id('MainContent_UcSearchFilters_CDFASelectionControl_SelectionControlTable')
    cfda_select = Select(driver.find_element_by_id('cfdaPrefix'))

    # Select the option whose value (mercifully) matches the agency prefix.
    cfda_select.select_by_value(agency_prefix)

    # Enter suffix/additional search
    cfda_extension = driver.find_element_by_id('cfdaExt')
    cfda_extension.clear()
    cfda_extension.send_keys(subagency_extension)
    # Don't send 'Keys.RETURN' here, otherwise the entire form will get
    # submitted instead of filling out the remainder first.

    # Click the 'includes' checkbox. Otherwise you'd need to enter exact matches.
    time.sleep(1)  # ...just in case. There's likely a more elegant way to handle this.
    driver.find_element_by_id('cfdaContains').click()

    # Add the filter. (It won't happen automatically.)
    driver.find_element_by_id('btnAdd').click()

    # 7. Click the ‘Search’ button.
    driver.find_element_by_id('MainContent_UcSearchFilters_Panel4')  # in case you just need to break it out of the focus on the accordions?
    driver.find_element_by_id('MainContent_UcSearchFilters_btnSearch_bottom').click()

    # 8. A new page loads. Click the ‘I acknowledge that I have read and
    #    understand the above statements’ checkbox.
    driver.find_element_by_id('chkAgree').click()

    # @todo: Replace this with a better 'wait', but the point is to make sure
    #        the button has loaded and can be clicked:
    time.sleep(1)

    # 9. Click the ‘Continue to Search Results’ button.
    driver.find_element_by_id('btnIAgree').click()

    time.sleep(1)

    # 10. Click the ‘Download Audits’ button.
    driver.find_element_by_id('MainContent_ucA133SearchResults_btnDownloadZipTop').click()
    # Apparently there's no need to then hit the ‘Save’ button. You’ve got your
    # download, a ZIP file of PDFs. :) And... a cross-reference filename
    # spreadsheet. :shrug:
    #
    # @todo: Consider elaborating on this such that you unzip the ZIP file and
    #        rename the filenames to match something clearer, like the grantee
    #        name and the fiscal year of the report.

    driver.quit()
    # @todo: Improve the contents of this HttpResponse.
    return HttpResponse("Your download has completed.", content_type="text/plain")


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
    """
    Args:
        A dataframe of agency data, currently derived from genXX.txt.

    Returns:
        A dataframe of findings, or 'None'.

    Room for improvement:
        Modify this function to retrieve the cross-referenced findings instead
        of just 'Y/N'.
    """

    try:
        findings_df = agency_df.loc[agency_df['CYFINDINGS'] == 'Y']
        return findings_df

    except:
        # @todo: Figure out what exception to actually raise here.
        Exception(" Error generating findings dataframe.")


def __get_number_of_findings(agency_df):
    """
    Args:
        agency_df: A dataframe of agency data, currently derived from genXX.txt.

    Returns:
        An integer, or 'None'.
    """

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

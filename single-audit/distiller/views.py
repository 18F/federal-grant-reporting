import os
from io import StringIO

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render

import pandas as pd

from .forms import AgencySelectionForm

# @todo: Update this to actually download the file from the FAC. We'll get there.
#        https://harvester.census.gov/facdissem/PublicDataDownloads.aspx
#        Do it on some cached ongoing basis so you're not making people wait for
#        a 500-MB download.
directory_name = 'single_audit_data_dump'
files_directory = os.path.join(settings.BASE_DIR, 'distiller', directory_name)


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

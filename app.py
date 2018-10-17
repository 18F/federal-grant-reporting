#!python

# to run:
# FLASK_APP=app.py flask run
# You'll need to set PDFTK_PATH env variable if 'which pdftk' returns anything other than
# '/usr/bin/pdftk'.

PDF_FILENAME = 'SF425-V2.pdf'

import os
import pypdftk

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def hello():
    return render_template('get-this-party-started.html')


@app.route("/generate-sf425")
def generate_sf425():
    '''
    Using sample data, fill out and display the specified PDF.
    '''
    pdf_directory = os.path.dirname(os.path.abspath(__file__))
    original_pdf_path = pdf_directory + '/' + PDF_FILENAME

    destination_pdf_file = pdf_directory + '/' + 'filled-out.pdf'

    sample_values = generate_sample_field_values()

    # Documentation: https://github.com/revolunet/pypdftk
    return pypdftk.fill_form(original_pdf_path, sample_values, destination_pdf_file)


def generate_sample_field_values():
    '''
    Provide sample data for all SF-425 fields for which we can find answers via
    the SAM API (http://gsa.github.io/sam_api/sam/index.html).

    Here's the field inventory, for reference:
    https://docs.google.com/spreadsheets/d/1TIAfrbB4fglEk66jqRmug5qUE16MHZ0A_nhg-crCl9g/edit#gid=872605059
    '''

    fields =    {
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P2[0].PDEmail[0]': 'email',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P2[0].FirstName[0]': '(first name from govtBusinessPoc)',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P2[0].LastName[0]': 'Last name',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P2[0].MiddleName[0]': 'Middle name',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P2[0].PDPhone[0]': 'usPhone, plus usPhoneExt if not blank',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P2[0].Prefix[0]': 'Prefix, from a list?',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P2[0].Suffix[0]': 'Suffix, from a list?',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P2[0].TitleAuthorizeCertifyingOfficial[0]': 'Official title',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P1[0].DUNSID[0]': 'duns',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P1[0].OrganizationCity[0]': 'city',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P1[0].OrganizationCountry[0]': 'countryCode',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P1[0].OrganizationCounty[0]': 'county',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P1[0].OrganizationName[0]': 'legalBusinessName',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P1[0].OrganizationProvince[0]': 'stateOrProvince',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P1[0].OrganizationState[0]': 'stateOrProvince',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P1[0].OrganizationStreet1[0]': 'line1',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P1[0].OrganizationStreet2[0]': 'line2',
                    'GrantApplicationWrapper[0].SF425_2_0_Main[0].SF425_2_0_P1[0].OrganizationZipCode[0]': 'zip'
                }

    return fields


if __name__ == "__main__":
    app.run()

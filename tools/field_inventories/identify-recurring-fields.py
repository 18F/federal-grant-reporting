#!/usr/bin/python3

# Originally created for https://github.com/18F/federal-grant-reporting/issues/63.

import csv
import os
import sys

from collections import defaultdict
from itertools import islice

# The CDER downloads included 10 header rows. We have no need for them, so we'll
# ignore them.
rows_of_preamble = 10

# Intentionally focusing on just the 'standard', not 'variant', ones for now.
# @someday: Rework this to be more robust and flexible.
files_directory = 'csvs/standard'


def get_filenames_of_field_inventories(directory=files_directory):
    return os.listdir(directory)


def get_form_name_from_filename(filename):
    if filename.endswith('.csv'):
        return filename[:-4]
    else:
        return filename


def process_fields(filename, field_occurrences=defaultdict(list)):
    """
    Create a dict of fieldnames and the forms that include them.

    Args:
        filename (str): CSV
        field_occurrences (dict): A dictionary of the sort we'll be returning.

    Returns:
        A dictionary of lists, indexed by fieldname; values are names of the
        forms that include those fields.
    """

    actual_filename = files_directory + '/' + filename
    with open(actual_filename, "r") as csvfile:
        # Ignore the preamble at the beginning of each CDER-generated CSV.
        for row in islice(csv.reader(csvfile), rows_of_preamble, None):
            fieldname = str(row)
            if fieldname != "[]":
                form_name = get_form_name_from_filename(filename)
                field_occurrences[fieldname].append(form_name)

    return field_occurrences


def discard_non_duplicates(field_occurrences):
    """
    Create a dict of fieldnames (if and only if they're included more than once)
    and the forms that include them.

    Put differently: remove any fieldnames that appear in only one form.

    This is currently also what's removing the cruft (download timestamp, etc.).

    Args:
        field_occurrences (dict): A dictionary of the sort we'll be returning.

    Returns:
        A dictionary of lists, indexed by fieldname; values are names of the
        forms that include those fields.
    """

    repeated_fields = dict()

    for k, v in field_occurrences.items():
        if len(v) < 2:
            continue
        else:
            repeated_fields[k] = v

    return repeated_fields


def print_dictionary(dictionary):
    """
    Print each field and the names of the forms in which it's found.

    Currently used only for debugging.
    """
    for k, v in dictionary.items():
        print(k + " appears in the following forms:")
        print(v)


def describe_repeats(repeated_fields):
    print("There are " + str(len(repeated_fields)) + " repeated fields.")

    print("They are: ")
    for k, v in repeated_fields.items():
        print(k + ", which appears in:")
        print(v)


def identify_and_describe_duplicate_fields():
    forms = get_filenames_of_field_inventories()

    field_inventory = defaultdict(list)

    for form in forms:
        process_fields(form, field_inventory)

    print("These " + str(len(forms)) + " forms include "
          + str(len(field_inventory)) + " fields total.")

    repeated_fields = discard_non_duplicates(field_inventory)

    describe_repeats(repeated_fields)


if __name__ == "__main__":
    if len(sys.argv) != 1:
        print("Usage: {}".format(sys.argv[0]))
        print("This script doesn't take any arguments. Just run the filename.")
        sys.exit(1)

    identify_and_describe_duplicate_fields()

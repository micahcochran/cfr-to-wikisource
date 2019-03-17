#!/usr/bin/env python3

########################################################################
#
# Name: proc-cfrxml-to-wikisource.py
# License: MIT
# Copyright (c) Micah Cochran 2018 
#
# Purpose:  This script scrapes XML from the U.S. Code of Federal Regulations,
# Title 3: President Documents and reformats it into wikitext for Wikisource's
# lists of United States Presidential Proclamations.
#
# See: https://en.wikisource.org/wiki/Portal:Presidents_of_the_United_States
#
# Note: The XML for Title 3: President Documents is only available for years
# 2001 and later.
#
# Requirements:
#    Python 3.x           (written on Python 3.4)
#    BeautifulSoup 4.x.x  (written on 4.6.0)
#    requests 2.x.x       (written on 2.10.0)
#
########################################################################


# requirements
# Python 3.x (written on Python 3.4)
import sys

# external dependencies
from bs4 import BeautifulSoup
import requests

# A portal for all US government XML data:
# https://www.gpo.gov/fdsys/bulkdata/

# this URL scheme from 2006 onwards is more readable in a browser
# https://www.gpo.gov/fdsys/pkg/CFR-{year}-title3-vol1/xml/CFR-{year}-title3-vol1-chapI.xml


def print_as_wiki_hybrid_table(rows, table_header):
    """
    Format proclamations in a table format that is a hybrid between
    print_as_wiki_table and the print_as_single_line.
    This is similar to the format used for the 2003 proclamations.

    ==== Example output ====
    {| style="valign:top;"
    ! Proc.&nbsp;No.
    ! &nbsp;
    ! align="left" | Subject
    ! <small>Signature Date</small>
    ! align="right" |&nbsp;&nbsp;<small>81 FR Page</small>
    |-
    | •&nbsp;[[Proclamation&nbsp;9388]]
    | align="center" | −
    | To Take Certain Actions Under the African Growth and Opportunity Act
    | align="right" | Jan. 11
    | align="right" | 1851
    |-
    | •&nbsp;[[Proclamation&nbsp;9389]]
    | align="center" | −
    | Religious Freedom Day, 2016
    | align="right" | Jan. 15
    | align="right" | 3689
    |-

    """

    # Print as Wiki Table
    print('{| style="valign:top;"')

    h_num, h_signature_date, h_subject, h_fedreg_page = table_header

    header = """! Proc.&nbsp;No.
! &nbsp;
! align="left" | Subject
! <small>Signature Date</small>
! align="right" |&nbsp;&nbsp;<small>{h_fedreg_page}</small>"""

    print(header.format(h_fedreg_page=h_fedreg_page))
    for row in rows:
        row_elements = [r.text.strip() for r in row.find_all('ENT')]
        # skip incomplete rows
        if len(row_elements) < 4:
            continue

        proc_num, signature_date, subject, fedreg_page = row_elements

        proc_row_format = """|-
| •&nbsp;[[Proclamation&nbsp;{proc_num}]]
| align="center" | −
| {subject}
| align="right" | {signature_date}
| align="right" | {fedreg_page}"""

        print(proc_row_format.format(proc_num=proc_num, subject=subject,
                                     signature_date=signature_date,
                                     fedreg_page=fedreg_page))

    print('|}')


def print_as_wiki_table(rows, table_header):
    """
    Format proclamations in a table format.

    ==== Example output ====
    {|
    ! No.
    ! Signature Date
    ! Subject
    ! 81 FR Page
    |-
    |-
    | [[Proclamation 9388|9388]]
    | Jan. 11
    | To Take Certain Actions Under the African Growth and Opportunity Act
    | 1851
    |-
    | [[Proclamation 9389|9389]]
    | Jan. 15
    | Religious Freedom Day, 2016
    | 3689
    |-
    """

    # Print as Wiki Table
    print('{|')

    for elm in table_header:
        print('! {}'.format(elm))

    for row in rows:
        # new table row
        print('|-')

        row_elements = tuple(row.stripped_strings)

        # skip incomplete rows
        if len(row_elements) < 4:
            continue

        proc_num, signature_date, subject, fedreg_page = row_elements

        print('| [[Proclamation {}|{}]]'.format(proc_num, proc_num))

        for elm in (signature_date, subject, fedreg_page):
            print('| {}'.format(elm))

    print('|}')


def print_as_single_line(rows):
    """
    Format proclamations in a single line format.

    ==== Example output ====
    *[[Proclamation 9388]] − To Take Certain Actions Under the African Growth and Opportunity Act (Jan. 11)
    *[[Proclamation 9389]] − Religious Freedom Day, 2016 (Jan. 15)
    *[[Proclamation 9390]] − Martin Luther King, Jr., Federal Holiday, 2016 (Jan. 15)
    *[[Proclamation 9391]] − American Heart Month, 2016 (Jan. 29)
    ...
    """
    for row in rows:
        row_elements = tuple(row.stripped_strings)

        # skip incomplete rows
        if len(row_elements) < 4:
            continue

        proc_num, signature_date, subject, fedreg_page = row_elements
        subject = subject.strip()

        print('*[[Proclamation {}]] − {} ({})'.format(proc_num, subject,
                                                      signature_date))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write("""
Usage:
    > python3 proc-cfrxml-to-wikisource.py [CFR-year] > wiki_output.txt\n\n""")
        sys.exit(1)

    year = int(sys.argv[1])

    if year < 2001:
        raise ValueError("CFR year must be atleast 2001.")

    url = 'https://www.gpo.gov/fdsys/bulkdata/CFR/{year}/title-3/CFR-{year}-title3-vol1.xml'.format(year=year)

    sys.stderr.write('Downloading from URL: {url}\n'.format(url=url))
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'xml')
    tables = soup.find_all('FAIDTABL')

    # find the table(s) for PROCLAMATIONS
    for table in tables:
        if 'PROCLAMATIONS' in table.TABLHED.string:
            proc_tables = table.find_all('GPOTABLE')
            break

    if not proc_tables:
        raise IOError("Could not find PROCLAMATIONS in file")

    for proc_table in proc_tables:
        table_header = [s for s in proc_table.BOXHD.stripped_strings]

        rows = proc_table.find_all('ROW')

        # === CHOOSE ONE of the below style on how to print the output =========
        # print_as_wiki_table(rows, table_header)
        # print_as_single_line(rows)
        print_as_wiki_hybrid_table(rows, table_header)

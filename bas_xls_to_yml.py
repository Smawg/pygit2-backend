#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""A script for converting BAS excel spreadsheets to yaml.
"""

from __future__ import print_function
import os
import sys
import argparse
from xlrd import open_workbook, XL_CELL_NUMBER
import yaml
import unicodedata


def main(arguments):
    parser = argparse.ArgumentParser(description=__doc__,
            formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('indir', help="Directory with input files")
    parser.add_argument('-o', '--outdir', help="Output directory", default='')

    args = parser.parse_args(arguments)
    parse_file(os.path.join(args.indir, 'Kontoplan_K1_2016_ver1.xls'),
               os.path.join(args.outdir, 'Kontoplan_K1_2016_ver1.yml'),
               [1, 4])
    parse_file(os.path.join(args.indir, 'Kontoplan_Normal_2016_ver1.xls'),
               os.path.join(args.outdir, 'Kontoplan_Normal_2016_ver1.yml'),
               [2, 5])

def parse_file(infile_path, outfile_path, col_indices):
    outfile = open(outfile_path, 'w')
    wb = open_workbook(filename=infile_path)
    sheet = wb.sheet_by_index(0)
    accounts = []
    for row_index in xrange(0, sheet.nrows):
        for col_index in col_indices:
            if sheet.cell(row_index, col_index).ctype == XL_CELL_NUMBER:
                iden = sheet.cell(row_index, col_index).value
                desc = sheet.cell(row_index, col_index+1).value
                if iden >= 1000:
                    accounts.append(
                            {
                                'id': int(iden),
                                'description': unicodedata.normalize('NFC',desc.strip()),
                                'type':account_number_to_type(iden)
                            })

    outfile.write(yaml.safe_dump({'accounts': accounts}, default_flow_style=False, allow_unicode=True, explicit_start=True))


def account_number_to_type(number):
    if number < 2000:
        return 'asset'
    if number < 3000:
        return 'liability'
    if number < 4000:
        return 'revenue'
    return 'expense'
    #if number < 8000:
    #    return 'expense'
    #if number < 8000:
    #    return 'financial'
    #if number < 9000:
    #    return 'contra'


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))


#!/usr/bin/env python3

import os
import json
import gspread
from dotenv import load_dotenv
from functools import reduce

load_dotenv()

SPREADSHEET_ID = os.environ.get('SPREADSHEET_ID', 'YOUR_ID')
WORKSHEET_INDEX = int(os.environ.get('WORKSHEET_INDEX', 0))
LOCALES_PATH = os.environ.get('LOCALES_PATH', './locales')


def fetch_worksheet(spreadsheet_id: str, worksheet_index: int) -> gspread.Worksheet:
    '''fetch worksheet from google spreadsheet'''
    gc = gspread.service_account(filename='./creds.json', scopes=gspread.auth.READONLY_SCOPES)
    sh = gc.open_by_key(spreadsheet_id)
    return sh.get_worksheet(worksheet_index)


def fetch_locales(worksheet: gspread.Worksheet) -> list:
    '''fetch locale names from worksheet, skip key column'''
    return worksheet.row_values(1)[1:]


def update_dict_from_keys(d, keys, val):
    '''build a nested dict

    e.g. for the given key `message.hello.world` with value `Hello World`,

    the result will be `{'message': {'hello': {'world': 'Hello World'}}}`
    '''
    reduce(
        lambda d, k: d.setdefault(k, {}),
        keys[:-1], d
    )[keys[-1]] = val


def build_i18n_dict(locale: str, worksheet: gspread.Worksheet) -> dict:
    '''generate json from worksheet'''
    D = {}
    for i, row in enumerate(worksheet.get_all_records()):
        print(f'build row: {i}, {row}')
        if not row:
            break

        keystr = row['key']
        valstr = row[locale]

        keys = keystr.split('.')
        update_dict_from_keys(D, keys, valstr)
    return D


def save_locales(locale: str, data: dict):
    '''save locales to file'''
    if not os.path.exists(LOCALES_PATH):
        os.makedirs(LOCALES_PATH)

    path = f'{LOCALES_PATH}/{locale}.json'
    print(f'save locale[{locale}] to : {path}')
    with open(path, 'w') as f:
        json.dump(data, f, indent=4)


def main():
    worksheet = fetch_worksheet(SPREADSHEET_ID, WORKSHEET_INDEX)
    locales = fetch_locales(worksheet)
    i18n_data = {}
    for locale in locales:
        print(f'build locale: {locale}')
        data = build_i18n_dict(locale, worksheet)
        i18n_data[locale] = data
        print(f'i18n done for {locale}')

    for locale, data in i18n_data.items():
        save_locales(locale, data)


if __name__ == '__main__':
    main()

# gspread-i18n-example

this repository is for generating vue-i18n json file using gspread

# Prerequisites

- Python3.8+

# Setup

- [Enable API Access for a project](https://docs.gspread.org/en/latest/oauth2.html#enable-api-access-for-a-project)
- [Create service account and download creds as JSON](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account)

After setup you would,

- replace [creds.json](./creds.json) with your own one.
- create a google spreadsheet document

## Spreadsheet Format

| key         | en          | kr         | jp             | #comments            |
| ----------- | ----------- | ---------- | -------------- | -------------------- |
| hello.world | hello world | 안녕하세요 | こんにちは世界 | this will be ignored |

- first row is locales, column name with `#` will be ignored
- you can use `.` for generating hierarchical key.

```
e.g. for the given key `message.hello.world` with value `Hello World`,
the result will be `{'message': {'hello': {'world': {'value': 'Hello World'}}}}`
```

# Installation

install dependencies

```bash
$ pip install -r requirements.txt
```

update `SPREADSHEET_ID` with your own one at [envs/env](./envs/env) and copy it to project root as `.env`

```bash
$ cp envs/env .env
```

# Usage

```
.
├── LICENSE
├── README.md
├── creds.json
├── envs
│   └── env
├── i18n.py
└── requirements.txt

1 directory, 6 files
```

run python script

```bash
$ python i18n.py

build locale: en
2/1000
3/1000
4/1000
5/1000
6/1000
7/1000
8/1000
save locale to : ./locales/en.json
build locale: id
2/1000
3/1000
4/1000
5/1000
6/1000
7/1000
8/1000
save locale to : ./locales/id.json
```

# Troubleshoot

## The caller does not have permission" when using server key

- [invite service account to the docuemnt](https://stackoverflow.com/questions/38949318/google-sheets-api-returns-the-caller-does-not-have-permission-when-using-serve)

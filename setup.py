import os
from setuptools import setup

VERSION = os.environ['VERSION']
APP = ['quiet.py']
DATA_FILES = [("modules/google_calendar", ["modules/google_calendar/client_secrets.json", "modules/google_calendar/cacerts.txt"])]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
        'CFBundleShortVersionString': VERSION,
        'CFBundleVersion': VERSION,
    },
#    'packages': ['rumps'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

from setuptools import setup

APP = ['quiet.py']
#DATA_FILES = []
DATA_FILES = [("modules/google_calendar", ["modules/google_calendar/client_secrets.json", "modules/google_calendar/cacerts.txt"])]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'LSUIElement': True,
    },
#    'packages': ['rumps'],
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

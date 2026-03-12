from setuptools import setup

APP = ['NoteForge.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'iconfile': 'icon.icns',
    'packages': ['customtkinter', 'darkdetect', 'typing_extensions'],
    'plist': {
        'CFBundleName': "NoteForge",
        'CFBundleDisplayName': "NoteForge",
        'CFBundleIdentifier': "com.yusuf.noteforge",
        'CFBundleVersion': "1.0.0",
        'LSMinimumSystemVersion': '11.0',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
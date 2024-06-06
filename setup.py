import sys
sys.setrecursionlimit(10000)

from setuptools import setup

APP = ['main.py']  # 你的脚本文件名
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['PIL', 'tkinter'],
    'plist': {
        'NSAppleEventsUsageDescription': "This application needs access to your files.",
    },
    'excludes': [
        'IPython', 'PyQt6', 'PyQt6.QtCore', 'PyQt6.QtGui', 'PySide6', 'PySide6.QtCore', 'PySide6.QtGui',
        '_overlapped', 'itertools.batched', 'itertools.pairwise', 'jnius',
        'pkg_resources._vendor.platformdirs.android', 'pkg_resources._vendor.packaging._manylinux',
        'platformdirs', 'cffi', 'cffi.FFI', 'defusedxml', 'importlib.metadata', 'olefile', 'zipp', 'importlib_metadata',
        'typing_extensions', 'IPython.display', 'typing_extensions.TypeGuard', 'Image', 'numpy'
    ]
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)

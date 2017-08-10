import sys
from cx_Freeze import setup, Executable

executables = [
    Executable('main.py')
]

setup(name='xls2pdf',
      version='0.1',
      description='convert XLSX file to PDF',
      executables=executables
      )
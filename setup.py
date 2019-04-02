import json
from setuptools import setup

__version__ = '0.0.6'

with open('./Pipfile.lock') as f:
    install_requires = []
    for k, v in json.load(f).items():
        if k == 'default':
            for l, d in v.items():
                install_requires.append(l+d['version'])

setup(
    name='dotfilesenv',
    version=__version__,
    py_modules=['dotfilesenv'],
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        dotfilesenv=dotfilesenv:main
    ''',
)

import json
import dotfilesenv

from setuptools import setup

with open('./Pipfile.lock') as f:
    install_requires = []
    for k, v in json.load(f).items():
        if k == 'default':
            for l, d in v.items():
                install_requires.append(l+d['version'])

setup(
    name='dotfilesenv',
    version=dotfilesenv.__version__,
    py_modules=['dotfilesenv'],
    install_requires=install_requires,
    entry_points='''
        [console_scripts]
        dotfilesenv=dotfilesenv:main
    ''',
)

from setuptools import setup

setup(
    name='dotfilesenv',
    version='0.0.2',
    py_modules=['dotfilesenv'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        dotfilesenv=dotfilesenv:main
    ''',
)
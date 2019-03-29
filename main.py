import os
import sys
import json
import shutil

import click

from typing import Dict

# setting information
DOTFILESENV_PATH = os.path.join(os.environ.get('HOME'), '.dotfilesenv')
SETTING = 'setting.json'

# color set
RED = '\033[31m'
END = '\033[0m'
GREEN = '\033[32m'


def get_setting() -> Dict:
    setting = os.path.join(DOTFILESENV_PATH, SETTING)
    if not os.path.exists(setting):
        return {}
    with open(os.path.join(DOTFILESENV_PATH, SETTING)) as f:
        return json.load(f)


def put_setting(setting) -> None:
    with open(os.path.join(DOTFILESENV_PATH, SETTING), 'w') as f:
        json.dump(setting, f)


@click.group(invoke_without_command=True)
@click.pass_context
def cmd(ctx):
    if ctx.invoked_subcommand is None:
        print(ctx.get_help())
    else:
        ctx.invoked_subcommand


@cmd.command(help='create a new setting and link')
@click.argument('name', required=True)
@click.argument('path', required=True)
def create(name, path):
    setting = get_setting()

    # check whether directory exists
    if name in setting:
        sys.stderr.write(f'{RED}Already exists!{END}\n')
        exit(1)
    if os.path.exists(os.path.join(DOTFILESENV_PATH, name)):
        sys.stderr.write(f'{RED}{name} exists in {DOTFILESENV_PATH}!{END}\n')
        exit(1)
    elif os.path.exists(os.path.join(DOTFILESENV_PATH, name, os.path.basename(path))):
        sys.stderr.write(f'{RED}{name}/{os.path.basename(path)} exists in {DOTFILESENV_PATH}!{END}\n')
        exit(1)

    # move setting to DOTFILESENV_PATH
    os.makedirs(os.path.join(DOTFILESENV_PATH, name))
    shutil.move(path, os.path.join(DOTFILESENV_PATH, name)+'/')

    # create symbolic link
    os.symlink(
        os.path.join(
            DOTFILESENV_PATH,
            name,
            os.path.basename(path)
        ),
        path,
        target_is_directory=os.path.isdir(path)
    )

    # save setting info
    path.replace(os.environ.get('HOME'), '~')
    setting[name] = path
    put_setting(setting)

    print(f'{GREEN}Success!{END}')


@cmd.command(help='delete a setting')
@click.argument('name', required=True)
def delete(name):
    print(f'{GREEN}{name}{END}')
    sys.stderr.write(f'{RED}Sorry! This API has not been implemented yet!{END}\n')


@cmd.command(help='link settings')
@click.argument('name', required=False)
def link(name):
    print(f'{GREEN}{name}{END}')
    sys.stderr.write(f'{RED}Sorry! This API has not been implemented yet!{END}\n')


if __name__ == '__main__':
    if not os.path.exists(DOTFILESENV_PATH):
        sys.stderr.write(f'{RED}{DOTFILESENV_PATH} directory is not found!\n')
        sys.stderr.write(f'Create it? [y/n]: {END}')
        ans = input()
        if ans == 'y':
            os.makedirs(DOTFILESENV_PATH)
            print(f'{GREEN}Created !{END}')
        else:
            sys.stderr.write(f'{RED}bye{END}\n')
            exit(1)
    cmd()

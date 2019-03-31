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
        json.dump(setting, f, indent=4)


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
def link(name, path):
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
# FIXME because built-in method is rewritten
def list():
    setting = get_setting()
    setting_list = []
    for k in setting:
        setting_list.append([k, setting[k]])

    setting_list.sort()
    setting_list = [['Name', 'Path']] + setting_list

    for v in setting_list:
        print(GREEN+'\t'.join(v)+END)


@cmd.command(help='delete a setting')
@click.argument('name', required=True)
def delete(name):
    setting = get_setting()
    path: str = setting.get(name)

    # validation
    if path is None:
        sys.stderr.write(f'{RED}No such setting: {name}{END}\n')
        exit(1)
    path = path.replace('~', os.environ.get('HOME'))

    if not os.path.islink(path):
        sys.stderr.write(f'{RED}{path} is not symbolic link!{END}\n')
        exit(1)

    # remove symlink
    os.remove(path)

    # move file
    shutil.move(os.path.join(DOTFILESENV_PATH, name, os.path.basename(path)), path)

    # remove setting dir
    os.rmdir(os.path.join(DOTFILESENV_PATH, name))

    del setting[name]
    put_setting(setting)

    print(f'{GREEN}Success!{END}')


@cmd.command(help='restore settings from .dotfilesenv')
@click.argument('name', required=False)
def restore(name):
    print(f'{GREEN}{name}{END}')
    sys.stderr.write(f'{RED}Sorry! This API has not been implemented yet!{END}\n')


def main():
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


if __name__ == '__main__':
    main()

import os
import sys
import json
import shutil
import datetime
import subprocess

import prettytable
import click

from typing import Dict

from . import __version__

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
@click.option('--version', '-v', is_flag=True, help='show version')
@click.pass_context
def cmd(ctx, version):
    if version:
        print(f'dotfilesenv version {__version__}')
    elif ctx.invoked_subcommand is None:
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
    src_path = os.path.join(
        DOTFILESENV_PATH,
        name,
        os.path.basename(path)
    )
    os.symlink(
        src_path,
        path,
        target_is_directory=os.path.isdir(src_path)
    )

    # save setting info
    path = path.replace(os.environ.get('HOME'), '~')
    setting[name] = path
    put_setting(setting)

    print(f'{GREEN}Success!{END}')


@cmd.command(help='show settings')
@click.option('--values', '-v', is_flag=True, help='for _values completion function',)
# FIXME because built-in method is rewritten
def list(values):
    setting = get_setting()
    if values:
        for k in setting:
            sys.stdout.write(f"{k}[{setting[k]}] ")
        return
    table = prettytable.PrettyTable(['Name', 'Path'], sortby='Name')
    table.align = 'l'
    for k in setting:
        table.add_row([k, setting[k]])
    print(table)


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


def _restore(setting_name, path, src_path, cache_path):
    print(f'Linking {src_path} to {path} ...')
    if os.path.exists(path):
        if os.path.islink(path):
            os.remove(path)
        else:
            t_cache_path = os.path.join(cache_path, setting_name)
            os.makedirs(t_cache_path, exist_ok=True)
            shutil.move(path, t_cache_path)

    os.symlink(src_path, path, target_is_directory=os.path.isdir(src_path))


@cmd.command(help='restore settings from .dotfilesenv')
@click.argument('name', required=False)
@click.option('--command', '-c', is_flag=True, help='ln command for creating symbolic link')
def restore(name, command):
    setting = get_setting()

    if name is not None and setting.get(name) is None:
        sys.stderr.write(f'{RED}No such setting: {name}{END}')
        exit(1)

    cache_path = DOTFILESENV_PATH + '.cache/' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + '/'

    for n in setting:
        path = setting[n].replace('~', os.environ.get('HOME'))
        src_path = os.path.join(
            DOTFILESENV_PATH,
            n,
            os.path.basename(path)
        )
        if name is None or name == n:
            if command:
                print(f'ln -s {src_path.replace(os.environ.get("HOME"), "~")} {path.replace(os.environ.get("HOME"), "~")}')
                continue
            _restore(n, path, src_path, cache_path)

    if not command:
        print(f'{GREEN}Success!{END}')


@cmd.command(help='git command alias for ~/.dotfilesenv directory')
@click.argument('args', nargs=-1)
def git(args):
    subprocess.run(
        f'git -C {DOTFILESENV_PATH} {" ".join(args)}',
        shell=True,
    )


@cmd.command(help='view ~/.dotfilesenv by specified command (e.g. dotfilesenv view code -> code ~/.dotfilesenv)')
@click.argument('cmd', required=True)
def view(cmd):
    subprocess.run(
        f'{cmd} {DOTFILESENV_PATH}',
        shell=True,
    )


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

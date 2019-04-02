def bump_up_version(file_path: str):
    file_content = ''
    with open(file_path) as f:
        for l in f:
            l = l.rstrip()
            if len(l) >= len('__version__') and l[:len('__version__')] == '__version__':
                t = eval(l.split(' = ')[1])
                t = t.split('.')
                t[-1] = str(int(t[-1]) + 1)
                t = f"'{'.'.join(t)}'"
                l = ' = '.join(['__version__', t])
            file_content += l + '\n'
    with open(file_path, 'w') as f:
        f.write(file_content)


bump_up_version('dotfilesenv.py')
bump_up_version('setup.py')

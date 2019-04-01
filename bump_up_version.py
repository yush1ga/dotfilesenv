FILE_PATH = 'dotfilesenv.py'

file_content = ''

with open(FILE_PATH) as f:
    for l in f:
        l = l.rstrip()
        if len(l) >= len('__version__') and l[:len('__version__')] == '__version__':
            t = eval(l.split(' = ')[1])
            t = t.split('.')
            t[-1] = str(int(t[-1]) + 1)
            t = f"'{'.'.join(t)}'"
            l = ' = '.join(['__version__', t])
        file_content += l + '\n'
with open(FILE_PATH, 'w') as f:
    f.write(file_content)

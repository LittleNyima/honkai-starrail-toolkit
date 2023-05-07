import re

if __name__ == '__main__':
    dictionary_path = 'starrail/utils/babelfish/dictionary.py'
    babelfish_path = 'starrail/utils/babelfish/__init__.py'
    with open(dictionary_path, encoding='utf-8') as d:
        content = d.read()

    pattern = re.compile(r'(\w+)\s+=\s+_MS')
    matches = re.findall(pattern, content)
    matches.sort()

    with open(babelfish_path, 'w') as f:
        f.write('import starrail.utils.babelfish.dictionary as dictionary\n')
        f.write('from starrail.utils.babelfish.translate import translate\n')
        f.write('\nfrom . import constants\n\n')
        for match in matches:
            f.write(f'{match} = dictionary.{match}\n')
        f.write("\n__all__ = ['constants', 'translate']\n")

    print(f'written to {babelfish_path}')

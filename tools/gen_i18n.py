import re


def find_pair_bracket(content: str, left: int) -> int:
    """
    Find the index of the matching closing bracket for a given opening one.

    Args:
        content (str): The content string containing brackets.
        left (int): The index of the opening bracket in the content.

    Returns:
        int: The index of the closing bracket, or -1 if not found.
    """

    depth = 0
    for idx in range(left, len(content)):
        if content[idx] == '(':
            depth += 1
        elif content[idx] == ')':
            depth -= 1
        if depth == 0:
            return idx
    return -1


def check_duplicate(vocabularies):
    """
    Check for duplicate entries in the given vocabularies list and print a
    warning if found.

    Args:
        vocabularies (List[str]): A list of vocabulary entries.
    """

    contains = set()
    for voc in vocabularies:
        name = voc.split('=')[0].strip()
        if name not in contains:
            contains.add(name)
        else:
            print(f'[WARNING] {name} is duplicate')


def sort_dictionary(dictionary_path):
    """
    Sort the dictionary file according to the vocabulary names and check for
    duplicates.

    Args:
        dictionary_path (str): The path to the dictionary file.
    """

    with open(dictionary_path, encoding='utf-8') as d:
        content = d.read()

    pattern = re.compile(r'(\w+)\s+=\s+_MS')
    leftmost, rightmost = len(content), 0
    vocabularies = []

    for find in re.finditer(pattern, content):
        left = find.start()
        right = find_pair_bracket(content, find.end())
        leftmost = min(leftmost, left)
        rightmost = max(rightmost, right)
        vocabularies.append(content[left:right+1].strip())

    vocabularies.sort()
    new_content = content[:leftmost].strip() + '\n\n'
    new_content += '\n'.join(vocabularies) + '\n\n'
    new_content += content[rightmost+1:].strip() + '\n'

    check_duplicate(vocabularies)

    with open(dictionary_path, 'w', encoding='utf-8') as d:
        d.write(new_content)

    print(f'written to {dictionary_path}')


def generate_babelfish(dictionary_path, babelfish_path):
    """
    Generate a babelfish file based on the sorted dictionary content.

    Args:
        dictionary_path (str): The path to the dictionary file.
        babelfish_path (str): The path to the output babelfish file.
    """

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


def main(dictionary_path, babelfish_path):
    """
    Sort the dictionary and generate a babelfish file.

    Args:
        dictionary_path (str): The path to the dictionary file.
        babelfish_path (str): The path to the output babelfish file.
    """

    sort_dictionary(dictionary_path)
    generate_babelfish(dictionary_path, babelfish_path)


if __name__ == '__main__':
    dictionary_path = 'starrail/utils/babelfish/dictionary.py'
    babelfish_path = 'starrail/utils/babelfish/__init__.py'

    main(dictionary_path, babelfish_path)

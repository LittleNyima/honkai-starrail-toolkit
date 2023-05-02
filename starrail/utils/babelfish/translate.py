from starrail.utils.babelfish.dictionary import lookup_table


def translate(text):
    if text in lookup_table:
        return lookup_table[text]()
    return text

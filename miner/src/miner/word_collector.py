import re


class WordCollector:
    def __init__(self):
        self.words = {}

    def extract_words_from(self, func_name):
        """
        Extract words from `string` according to the python naming conventions (e.g., snake case) and store them in
        `self.words` dictionary as key and values as number of occurences (considering also previous extracted words.)
        :param func_name: function or method names
        :return: None
        """
        # print('func_name: {}'.format(func_name))
        names_separated = re.split('_', func_name)
        for name in names_separated:
            matches_str_lst = re.findall(r'[a-z]+|[A-Z]+[a-z]*', name)
            for match_str in matches_str_lst:
                lower_case = match_str.lower()
                # print(lower_case)
                if lower_case in self.words.keys():
                    self.words[lower_case] += 1
                else:
                    self.words[lower_case] = 1


if __name__ == '__main__':
    wc = WordCollector()
    wc.extract_words_from('camel32_12CaseCamelCase_hello_myFriend_my')
    print(wc.words)

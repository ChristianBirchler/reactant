import re


class WordCollector:
    def __init__(self):
        self.words = {}
        self.digit_chars = [str(x) for x in range(10)]

    def extract_words_from(self, func_name):
        """
        Extract words from `string` according to the python naming conventions (e.g., snake case) and store them in
        `self.words` dictionary as key and values as number of occurences (considering also previous extracted words.)
        :param func_name: function or method names
        :return: None
        """
        print('func_name: {}'.format(func_name))
        # TODO: Fix the regex pattern!
        separated_name_segments = re.split(r'_+', func_name)
        for segment in separated_name_segments:
            for i in range(len(segment)):
                if segment[i] in self.digit_chars:
                    print('is number')


if __name__ == '__main__':
    wc = WordCollector()
    wc.extract_words_from('camel_12CaseCamelCase')

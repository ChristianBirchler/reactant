from word_collector import WordCollector
import os
import javalang
from javalang.tree import CompilationUnit


class JavaMiner:
    def __init__(self):
        self.git_repo = None
        self.word_collector = WordCollector()
        self.local_git_repo = None

    def __iterate_ast(self, tree: CompilationUnit):
        for _, node in tree.filter(javalang.tree.MethodDeclaration):
            self.word_collector.extract_words_from(node.name)

    def mine(self):
        """
        Collect names of functions and methods in java files.
        :return: None
        """
        print('* mining ...')

        for root, dirs, files in os.walk(self.local_git_repo):
            for file in files:
                if file.endswith('.java'):
                    filename = os.path.join(root, file)
                    # filename = os.path.join(os.getcwd(), 'main.py')
                    print(filename)
                    try:
                        with open(filename, 'r') as fp:
                            tree = javalang.parse.parse(fp.read())
                            self.__iterate_ast(tree)
                    except Exception:
                        # TODO: logging
                        pass


if __name__ == '__main__':
    pass

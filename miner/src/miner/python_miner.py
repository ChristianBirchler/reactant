import ast
import os

from word_collector import WordCollector


class MyNodeVisitor(ast.NodeVisitor):
    def __init__(self, word_collector_):
        ast.NodeVisitor.__init__(self)
        self.word_collector = word_collector_

    def visit_FunctionDef(self, node_: ast.FunctionDef):
        self.word_collector.extract_words_from(node_.name)


class PythonMiner:
    def __init__(self):
        self.git_repo = None
        self.word_collector = WordCollector()
        self.visitor = MyNodeVisitor(self.word_collector)
        self.local_git_repo = None

    def mine(self):
        """
        Collect names of functions and methods in python files.
        :return: None
        """
        print('* mining ...')

        for root, dirs, files in os.walk(self.local_git_repo):
            for file in files:
                if file.endswith('.py'):
                    filename = os.path.join(root, file)
                    # filename = os.path.join(os.getcwd(), 'main.py')
                    print(filename)
                    try:
                        with open(filename, 'r') as fp:
                            node = ast.parse(fp.read())
                            self.visitor.visit(node)
                    except Exception:
                        # TODO: logging
                        pass


if __name__ == '__main__':
    pass

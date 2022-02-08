import ast
import os

from word_collector import WordCollector


class PythonMiner:
    def __init__(self, git_repo_):
        self.git_repo = git_repo_
        self.word_collector = WordCollector()

    def mine(self):
        """
        Collect names of functions and methods in python files.
        :return: None
        """
        class MyNodeVisitor(ast.NodeVisitor):
            def __init__(self, word_collector_):
                self.word_collector = word_collector_

            def visit_FunctionDef(self, node_: ast.FunctionDef):
                self.word_collector.extract_words_from(node_.name)

        my_node_visitor = MyNodeVisitor(self.word_collector)

        for root, dirs, files in os.walk('repo'):
            for file in files:
                if file.endswith('.py'):
                    filename = os.path.join(root, file)
                    # filename = os.path.join(os.getcwd(), 'main.py')
                    print(filename)
                    try:
                        with open(filename, 'r') as fp:
                            node = ast.parse(fp.read())
                    except Exception:
                        pass

                    my_node_visitor.visit(node)


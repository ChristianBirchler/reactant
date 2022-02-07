import time
import git
import os
import shutil
import ast
import re
from github import Github


class WordCollector:
    def __init__(self):
        self.words = {}

    def extract_words_from(self, string):
        """
        Extract words from `string` according to the python naming conventions (e.g., snake case) and store them in
        `self.words` dictionary as key and values as number of occurences (considering also previous extracted words.)
        :param string: function or method names
        :return: None
        """

        # TODO: Fix the regex pattern!
        pattern = r'^(\w+)_*(\w+)\Z'
        match = re.match(pattern, string)
        if match:
            print(match.groups())


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
                    with open(filename, 'r') as fp:
                        node = ast.parse(fp.read())

                    my_node_visitor.visit(node)


if __name__ == '__main__':
    print('* start miner ...')

    g = Github('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')

    repositories = g.search_repositories(query='language:Python', sort='stars', order='desc')

    if os.path.exists(os.path.join(os.getcwd(), 'repo')):
        shutil.rmtree(os.path.join(os.getcwd(), 'repo'))
    for repo in repositories:
        os.mkdir(os.path.join(os.getcwd(), 'repo'))
        print('{} stars: {}'.format(repo.name, repo.stargazers_count))
        print(repo.clone_url)

        git_repo = git.Repo.clone_from(repo.clone_url, os.path.join(os.getcwd(), 'repo'))
        python_miner = PythonMiner(git_repo)
        python_miner.mine()

        print('git_repo: {}'.format(git_repo))
        shutil.rmtree(os.path.join(os.getcwd(), 'repo'))
        time.sleep(2)


import time
import git
import os
import shutil
from github import Github

from python_miner import PythonMiner


if __name__ == '__main__':
    print('* start miner ...')

    g = Github('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')

    python_repositories = g.search_repositories(query='language:Python', sort='stars', order='desc')
    java_repositories = g.search_repositories(query='language:Java', sort='stars', order='desc')

    python_tmp_repo_dir = 'python-repo'
    java_tmp_repo_dir = 'java-repo'

    if os.path.exists(os.path.join(os.getcwd(), python_tmp_repo_dir)):
        shutil.rmtree(os.path.join(os.getcwd(), python_tmp_repo_dir))

    python_miner = PythonMiner()
    python_miner.local_git_repo = python_tmp_repo_dir

    for repo in python_repositories:
        os.mkdir(os.path.join(os.getcwd(), python_tmp_repo_dir))
        print('{} stars: {}'.format(repo.name, repo.stargazers_count))
        print(repo.clone_url)

        git_repo = git.Repo.clone_from(repo.clone_url, os.path.join(os.getcwd(), python_tmp_repo_dir))

        python_miner.git_repo = git_repo
        python_miner.mine()
        print(python_miner.word_collector.words)

        shutil.rmtree(os.path.join(os.getcwd(), python_tmp_repo_dir))
        # time.sleep(2)


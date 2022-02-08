import time
import git
import os
import shutil
from github import Github

from python_miner import PythonMiner


if __name__ == '__main__':
    print('* start miner ...')

    g = Github('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')

    repositories = g.search_repositories(query='language:Python', sort='stars', order='desc')

    if os.path.exists(os.path.join(os.getcwd(), 'repo')):
        shutil.rmtree(os.path.join(os.getcwd(), 'repo'))

    python_miner = PythonMiner()

    for repo in repositories:
        os.mkdir(os.path.join(os.getcwd(), 'repo'))
        print('{} stars: {}'.format(repo.name, repo.stargazers_count))
        print(repo.clone_url)

        git_repo = git.Repo.clone_from(repo.clone_url, os.path.join(os.getcwd(), 'repo'))

        python_miner.git_repo = git_repo
        python_miner.mine()

        print('git_repo: {}'.format(git_repo))
        shutil.rmtree(os.path.join(os.getcwd(), 'repo'))
        time.sleep(2)


import git
import os
import shutil
from github import Github
from multiprocessing.managers import BaseManager

from python_miner import PythonMiner
from java_miner import JavaMiner
from threading import Thread


class QueueManager(BaseManager):
    pass


def python_thread_activity():
    for repo in python_repositories:
        os.mkdir(os.path.join(os.getcwd(), python_tmp_repo_dir))
        print('{} stars: {}'.format(repo.name, repo.stargazers_count))
        print(repo.clone_url)

        git_repo = git.Repo.clone_from(repo.clone_url, os.path.join(os.getcwd(), python_tmp_repo_dir))

        python_miner.git_repo = git_repo
        python_miner.mine()
        print(python_miner.word_collector.words)

        python_queue.put(python_miner.word_collector.words)

        shutil.rmtree(os.path.join(os.getcwd(), python_tmp_repo_dir))


def java_thread_activity():
    for repo in java_repositories:
        os.mkdir(os.path.join(os.getcwd(), java_tmp_repo_dir))
        print('{} stars: {}'.format(repo.name, repo.stargazers_count))
        print(repo.clone_url)

        git_repo = git.Repo.clone_from(repo.clone_url, os.path.join(os.getcwd(), java_tmp_repo_dir))

        java_miner.git_repo = git_repo
        java_miner.mine()

        java_queue.put(java_miner.word_collector.words)
        # print(java_miner.word_collector.words)

        shutil.rmtree(os.path.join(os.getcwd(), java_tmp_repo_dir))


if __name__ == '__main__':

    QueueManager.register('get_python_queue')
    QueueManager.register('get_java_queue')

    if os.getenv('VISUALIZER') != 'visualizer':
        address = ''
    else:
        address = 'visualizer'
    queue_manager = QueueManager(address=(address, 50000), authkey=b'abracadabra')
    queue_manager.connect()

    python_queue = queue_manager.get_python_queue()
    java_queue = queue_manager.get_java_queue()

    print('* start miner ...')

    g = Github('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')

    python_repositories = g.search_repositories(query='language:Python', sort='stars', order='desc')
    java_repositories = g.search_repositories(query='language:Java', sort='stars', order='desc')

    python_tmp_repo_dir = 'python-repo'
    java_tmp_repo_dir = 'java-repo'

    if os.path.exists(os.path.join(os.getcwd(), python_tmp_repo_dir)):
        shutil.rmtree(os.path.join(os.getcwd(), python_tmp_repo_dir))

    if os.path.exists(os.path.join(os.getcwd(), java_tmp_repo_dir)):
        shutil.rmtree(os.path.join(os.getcwd(), java_tmp_repo_dir))

    python_miner = PythonMiner()
    java_miner = JavaMiner()

    python_miner.local_git_repo = python_tmp_repo_dir
    java_miner.local_git_repo = java_tmp_repo_dir

    python_thread = Thread(target=python_thread_activity)
    java_thread = Thread(target=java_thread_activity)

    python_thread.start()
    java_thread.start()

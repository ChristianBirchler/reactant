from github import Github

if __name__ == '__main__':
    print('* start miner ...')

    g = Github('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')

    repositories = g.search_repositories(query='language:Python', sort='stars', order='desc')
    for repo in repositories:
        print('{} stars: {}'.format(repo.name, repo.stargazers_count))

from github import Github
g = Github()

for repo in g.get_organization("apache").get_repos():
    print(repo.full_name)
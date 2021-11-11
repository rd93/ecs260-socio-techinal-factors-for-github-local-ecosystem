import time
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import github

g = github.Github()

client = MongoClient('localhost', 27017)
db = client.githubEcosystem
collection = db.repos

# repos = [line.rstrip() for line in open("repos.txt")]

for repo_obj in g.get_organization("apache").get_repos():
    repo = repo_obj.full_name
    url = 'https://github.com/' + repo + '/network/dependents'
    if collection.find_one({"repo_name": repo}):
        print("Found repo in DB, skipping: " + repo)
        continue
    dependents = []
    while 1:
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        box_elems = soup.findAll("div", {"class": "Box-row"})

        if box_elems is None or len(box_elems) == 0:
            break
        for elem in box_elems:
            dependents.append(elem.find('a', {"data-repository-hovercards-enabled": ""}).text + '/' + elem.find('a', {
                "data-hovercard-type": "repository"}).text)

        nextButton = soup.find("div", {"class": "paginate-container"}).find('a')
        if nextButton and nextButton.text == 'Next':
            url = nextButton["href"]
        else:
            break
        time.sleep(5)

    if len(dependents) > 10:
        print("Inserting repo: " + repo + ", dependencies: " + str(len(dependents)))
        collection.insert_one({"repo_name": repo, "dependencies": dependents})
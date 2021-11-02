import requests
from bs4 import BeautifulSoup

repos = ["apache/superset"]

for repo in repos:
    url = 'https://github.com/' + repo + '/network/dependents'
    dependents = []
    while 1:
        print(url)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        for elem in soup.findAll("div", {"class": "Box-row"}):
            dependents.append(elem.find('a', {"data-repository-hovercards-enabled": ""}).text + '/' + elem.find('a', {
                "data-hovercard-type": "repository"}).text)

        nextButton = soup.find("div", {"class": "paginate-container"}).find('a')
        if nextButton and nextButton.text == 'Next':
            url = nextButton["href"]
        else:
            break
    print(len(dependents))
from pymongo import MongoClient
import csv

client = MongoClient('localhost', 27017)
db = client.githubEcosystem
repo_collection = db.repos
metric_collection = db.metrics

with open('op.csv', 'w') as f:
    wtr = csv.writer(f)
    wtr.writerow(["Repo Name", "Is Source?"])
    for db_obj in metric_collection.find():
        for repo_obj in db_obj['repos']:
            wtr.writerow([repo_obj['repo_name'], repo_obj['is_src']])
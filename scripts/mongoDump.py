from pymongo import MongoClient
from bson.json_util import dumps
import csv

client = MongoClient('localhost', 27017)
db = client.githubEcosystem
repo_collection = db.repos
metric_collection = db.metrics
# cursor = metric_collection.find({})

# with open('op.csv', 'w') as f:
#     wtr = csv.writer(f)
#     wtr.writerow(["Repo Name", "Is Source?"])
repo_count = 0
dep_count = 0
for db_obj in metric_collection.find():
    repo_count += 1
    for repo_obj in db_obj['repos']:
        dep_count += 1
        # wtr.writerow([repo_obj['repo_name'], repo_obj['is_src']])
print(repo_count)
print(dep_count)


# with open('op.json', 'w') as file:
#     file.write('{data:[":')
#     for document in cursor:
#         file.write(dumps(document))
#         file.write(',')
#     file.write(']}')
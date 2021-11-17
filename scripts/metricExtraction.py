from github import Github
from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.githubEcosystem
repo_collection = db.repos
metric_collection = db.metrics

g = Github('')


def extract_metrics(repo_name, is_src):
    repo = g.get_repo(repo_name)
    count = 0
    total_latency = None
    total_comments = 0

    for pr in repo.get_pulls(state='closed'):
        # Stopping at 100 PRs
        if count > 100:
            break
        created_time = pr.created_at
        closed_time = pr.closed_at
        latency = closed_time - created_time
        total_comments += pr.comments

        if total_latency is None:
            total_latency = latency
        else:
            total_latency += latency
        count += 1

    # avg_latency = total_latency / count
    # avg_comments = total_comments / count
    if total_latency is not None:
        total_latency = total_latency.seconds

    feature_list = {'repo_name': repo_name,
                    'is_src': is_src,
                    'contributors': repo.get_contributors().totalCount,
                    'release_count': repo.get_releases().totalCount,
                    'commit_count': repo.get_commits().totalCount,
                    # 'average_pr_latency': avg_latency.seconds,
                    # 'average_comments': avg_comments,
                    'pr_count': count,
                    'total_latency': total_latency,
                    'total_comments': total_comments
                    }

    return feature_list


i = 1
for db_obj in repo_collection.find():
    repo_name = db_obj['repo_name']
    print("Extracting for repo " + str(i) + ": ", repo_name)
    i += 1

    # if db_obj['is_active'] is False:
    #     print("Inactive entry, skipping...")
    #     continue

    # if len(db_obj['dependencies']) > 60:
    #     print("Skipping because of dependency size: " + str(len(db_obj['dependencies'])))
    #     continue

    if metric_collection.find_one({"src_repo_name": repo_name}):
        print("Found repo in DB, skipping...")
        continue

    metrics_obj = {'src_repo_name': repo_name, 'repos': []}
    metrics_obj['repos'].append(extract_metrics(repo_name, True))

    try:
        for dependency in db_obj['dependencies']:
            metrics_obj['repos'].append(extract_metrics(dependency, False))
    except Exception as e:
        print(e)

    total_dependencies = len(db_obj['dependencies'])
    if len(metrics_obj['repos']) >= (total_dependencies / 2):
        metric_collection.insert_one(metrics_obj)

import json
import csv


import os

curr_file = os.path.dirname(os.path.abspath(__file__))
average_delay_file = curr_file + "/data/average_delay_in_release.csv"
# num_email_file = curr_file + "/data/no_of_emails.csv"
# metric_json_file = curr_file + "/repo_metrics.json"

new_data_file = curr_file + "/data/mongo_dump.json"

# print(metric_json_file)

def extract_data_from_csv():
    result = {}
    with open(average_delay_file) as file:
        csvreader = csv.reader(file)
        for id, row in enumerate(csvreader):
            if id == 0:
                continue
            result[row[1]] = row[2]
            # print(row)
    return result

# def extract_data_from_csv_delay():
#     result = {}
#     with open(num_email_file) as file:
#         csvreader = csv.reader(file)
#         for id, row in enumerate(csvreader):
#             if id == 0:
#                 continue
#             name = row[1].split(".")
#             name = name[0]
#             result[name] = row[2]
#             # print(row)
#     return result




def create_csv_from_metric_json():

    with open(curr_file + '/data/repo_data.csv','w') as w:
        wtr = csv.writer(w)
        wtr.writerow(["Repo Name","Release Count", "Commit Count", "PR Count", "Average Latency", "Average Comments", "Contributors"])
        # num_of_emails_data = extract_data_from_csv()
        # average_delay_data = extract_data_from_csv_delay()
        # print(num_of_emails_data)
        # print(average_delay_data)

        # for k, val in num_of_emails_data.items():
        #     if k in average_delay_data:
        #         print(k)
        # exit()
        with open(new_data_file, 'r') as j:
            data = json.load(j)
            for el in data["data"]:
                release_count = 0
                commit_count = 0
                pr_count = 0
                total_latency = 0
                total_comments = 0
                contributors = 0
                avg_latency = 0
                avg_comments = 0
                num_of_emails_in_repo = 0
                average_delay = 0
                src_name = el["src_repo_name"].split("/")
                src_name = src_name[-1]

                # if src_name in num_of_emails_data and src_name in average_delay_data:
                #     num_of_emails_in_repo = num_of_emails_data[src_name]
                #     average_delay = average_delay_data[src_name]
                # else:
                #     continue
                for repo in el['repos']:
                    release_count += repo['release_count']
                    commit_count += repo['commit_count']
                    pr_count += repo['pr_count']
                    if repo['total_latency'] is None:
                        continue
                    total_latency += repo['total_latency']
                    total_comments += repo['total_comments']
                    contributors += repo['contributors']
                if pr_count != 0:
                    avg_latency = total_latency / pr_count
                    avg_comments = total_comments / pr_count
                wtr.writerow([src_name, release_count, commit_count, pr_count, avg_latency, avg_comments, contributors ])

if "__main__" == __name__:
    create_csv_from_metric_json()
    # print(extract_data_from_csv())
    # extract_data_from_csv_delay()

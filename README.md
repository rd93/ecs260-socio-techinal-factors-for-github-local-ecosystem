# ECS 260: Impact of socio-technical factors on the effectiveness of a local ecosystem on GitHub

To install the libraries required for running the extraction scripts, run:

```
pip install -r requirements.txt
```

All the extraction scripts are located in the folder 'scripts'. A brief description about all the scripts:
1. regression_analysis.R - Contains all the code for regression analysis in R.
2. dependencyExtraction.py - Extracts all the GitHub repos from Apache Software Foundation with dependents > 10. Also extracts all the dependent repos for the source projects that fulfil the criteria. (See extracted_repositories.csv for data)
3. metricExtraction.py - Extracts all the metrics like contributor count, commit count etc. using PyGithub 
4. create_combined_csv.py - Combines the data obtained from metricExtraction.py and the data extracted for emails and average delay in releases into one CSV - phase1_data.csv
5. mongoDump.py - Extracts all the data in the mongo collection to mongo_dump.json
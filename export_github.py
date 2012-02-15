import os
import csv
from github2.client import Github
import httplib2

httplib2.Http(disable_ssl_certificate_validation=True)

# api settings for github
git_username = os.environ['GIT_USERNAME'] 
git_api_token = os.environ['GIT_API_TOKEN'] 
git_repo = os.environ['GIT_REPO'] # of form user/repo

# csv name
csv_name = "git_hub_issues.csv"

def run_csv():
    """
    Export github issues into a csv format
    """
    output_csv = csv.writer(open(csv_name, 'wb'), delimiter=',')
    github = Github(git_username, git_api_token)

    # csv headers
    headers = [
        'id',
        'title',
        'body',
        'state',
        'creator',
        'labels',
        'created_at',
        'updated_at',
        'closed_at',
    ]

    # write header rows
    output_csv.writerow(headers)

    # get the git issues and write the rows to the csv
    git_issues = github.issues.list(git_repo)
    for git_issue in git_issues:
        print git_issue.title
        labels = ' '.join(git_issue.labels)

        # alot of these are blank because they are not really 
        # needed but if you need them just fill them out
        issue = [
            git_issue.number,
            git_issue.title.encode('utf8'),
            git_issue.body.encode('utf8'),
            git_issue.state, 
            git_issue.user, 
            labels,
            git_issue.created_at,
            git_issue.updated_at,
            git_issue.closed_at,
        ]
        output_csv.writerow(issue)

if __name__ == '__main__':
    run_csv()

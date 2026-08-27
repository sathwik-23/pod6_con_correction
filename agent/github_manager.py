import time
import json

from github import Github
from github.GithubException import GithubException


class GithubManager:

    def __init__(self, github_token, repo_name):

        self.github = Github(github_token)
        self.repository = self.github.get_repo(repo_name)

    def create_branch(self, incident_id):

        source_branch = self.repository.get_branch(
            "main"
        )

        branch_name = (
            f"remediation-"
            f"{incident_id}-"
            f"{int(time.time())}"
        )

        self.repository.create_git_ref(
            ref=f"refs/heads/{branch_name}",
            sha=source_branch.commit.sha
        )

        print(f"Created Branch: {branch_name}")

        return branch_name

    def update_file_in_branch(
        self,
        branch_name,
        file_path,
        content
    ):

        file = self.repository.get_contents(
            file_path,
            ref=branch_name
        )

        self.repository.update_file(
            path=file_path,
            message=f"Configuration remediation in {branch_name}",
            content=json.dumps(content, indent=4),
            sha=file.sha,
            branch=branch_name
        )

        print(
            f"Updated file: {file_path}"
        )

    def create_pull_request(
        self,
        branch_name,
        title,
        body,
        base_branch="main"
    ):

        try:

            pr = self.repository.create_pull(
                title=title,
                body=body,
                head=branch_name,
                base=base_branch
            )

            print(
                f"PR Created: {pr.html_url}"
            )

            return pr.html_url

        except GithubException as e:

            print(f"PR Creation Error: {e}")

            return None
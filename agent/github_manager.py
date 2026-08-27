import os

from github import Github
from git import Repo


class GithubManager:

    def __init__(self):

        self.token = os.getenv("GITHUB_TOKEN")
        self.repository_name = os.getenv("GITHUB_REPOSITORY")

    def create_branch(self, repo_path, branch_name):

        repo = Repo(repo_path)

        try:
            repo.git.checkout("-b", branch_name)

        except Exception:
            repo.git.checkout(branch_name)

        return repo

    def commit_changes(self, repo, message):

        repo.git.add(A=True)

        repo.index.commit(message)

    def push_branch(self, repo, branch):

        origin = repo.remote(name="origin")

        origin.push(branch)

    def create_pull_request(
        self,
        branch,
        title,
        body
    ):

        github = Github(self.token)

        repository = github.get_repo(
            self.repository_name
        )

        pr = repository.create_pull(
            title=title,
            body=body,
            head=branch,
            base="main"
        )

        return pr.html_url
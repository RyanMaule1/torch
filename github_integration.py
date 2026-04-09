from __future__ import annotations

from github import Github
from github.GithubException import GithubException


class GitHubIntegration:
    """Minimal GitHub integration wrapper for v0 automation hooks."""

    def __init__(self, token: str, repository: str) -> None:
        self.client = Github(token)
        self.repo = self.client.get_repo(repository)

    def create_branch(self, new_branch: str, source_branch: str = "main") -> None:
        src = self.repo.get_branch(source_branch)
        self.repo.create_git_ref(ref=f"refs/heads/{new_branch}", sha=src.commit.sha)

    def commit_files(self, branch: str, files: dict[str, str], message: str) -> None:
        for path, content in files.items():
            try:
                existing = self.repo.get_contents(path, ref=branch)
                self.repo.update_file(
                    path=path,
                    message=message,
                    content=content,
                    sha=existing.sha,
                    branch=branch,
                )
            except GithubException:
                self.repo.create_file(path=path, message=message, content=content, branch=branch)

    def create_pull_request(self, title: str, body: str, head: str, base: str = "main") -> str:
        pr = self.repo.create_pull(title=title, body=body, head=head, base=base)
        return pr.html_url

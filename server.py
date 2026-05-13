import os
from github import Github
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("GitHub MCP Server")
gh = Github(os.getenv("GITHUB_TOKEN"))


@mcp.tool()
def create_branch(repo_name: str, branch_name: str, from_branch: str = "main") -> str:
    """Create a new branch in a GitHub repository."""
    repo = gh.get_repo(repo_name)
    source = repo.get_branch(from_branch)
    repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
    return f"Branch '{branch_name}' created from '{from_branch}' in {repo_name}"


@mcp.tool()
def push_file(repo_name: str, branch: str, file_path: str, content: str, commit_message: str) -> str:
    """Create or update a file in a repository (push)."""
    repo = gh.get_repo(repo_name)
    try:
        existing = repo.get_contents(file_path, ref=branch)
        repo.update_file(file_path, commit_message, content, existing.sha, branch=branch)
        return f"Updated '{file_path}' on branch '{branch}'"
    except Exception:
        repo.create_file(file_path, commit_message, content, branch=branch)
        return f"Created '{file_path}' on branch '{branch}'"


@mcp.tool()
def create_pull_request(repo_name: str, title: str, head: str, base: str = "main", body: str = "") -> str:
    """Open a pull request."""
    repo = gh.get_repo(repo_name)
    pr = repo.create_pull(title=title, body=body, head=head, base=base)
    return f"PR #{pr.number} created: {pr.html_url}"


@mcp.tool()
def merge_pull_request(repo_name: str, pr_number: int, commit_message: str = "Merged via MCP") -> str:
    """Merge an open pull request."""
    repo = gh.get_repo(repo_name)
    pr = repo.get_pull(pr_number)
    result = pr.merge(commit_message=commit_message)
    return f"PR #{pr_number} merged: {result.merged}"


if __name__ == "__main__":
    mcp.run()

import os
from github import Github, GithubException
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
if not GITHUB_TOKEN:
    raise EnvironmentError("GITHUB_TOKEN is not set in .env")

mcp = FastMCP("GitHub MCP Server")
gh = Github(GITHUB_TOKEN)


@mcp.tool()
def list_branches(repo_name: str) -> str:
    """List all branches in a GitHub repository."""
    try:
        repo = gh.get_repo(repo_name)
        branches = [b.name for b in repo.get_branches()]
        return f"Branches in {repo_name}: {', '.join(branches)}"
    except GithubException as e:
        return f"Error: {e.data.get('message', str(e))}"


@mcp.tool()
def create_branch(repo_name: str, branch_name: str, from_branch: str = "main") -> str:
    """Create a new branch in a GitHub repository."""
    try:
        repo = gh.get_repo(repo_name)
        source = repo.get_branch(from_branch)
        repo.create_git_ref(ref=f"refs/heads/{branch_name}", sha=source.commit.sha)
        return f"Branch '{branch_name}' created from '{from_branch}' in {repo_name}"
    except GithubException as e:
        return f"Error: {e.data.get('message', str(e))}"


@mcp.tool()
def push_file(repo_name: str, branch: str, file_path: str, content: str, commit_message: str) -> str:
    """Create or update a file in a repository (push)."""
    try:
        repo = gh.get_repo(repo_name)
        try:
            existing = repo.get_contents(file_path, ref=branch)
            repo.update_file(file_path, commit_message, content, existing.sha, branch=branch)
            return f"Updated '{file_path}' on branch '{branch}'"
        except GithubException:
            repo.create_file(file_path, commit_message, content, branch=branch)
            return f"Created '{file_path}' on branch '{branch}'"
    except GithubException as e:
        return f"Error: {e.data.get('message', str(e))}"


@mcp.tool()
def list_pull_requests(repo_name: str, state: str = "open") -> str:
    """List pull requests in a repository. State: open, closed, all."""
    try:
        repo = gh.get_repo(repo_name)
        prs = repo.get_pulls(state=state)
        result = [f"#{pr.number} '{pr.title}' ({pr.head.ref} -> {pr.base.ref})" for pr in prs]
        return "\n".join(result) if result else f"No {state} PRs found."
    except GithubException as e:
        return f"Error: {e.data.get('message', str(e))}"


@mcp.tool()
def create_pull_request(repo_name: str, title: str, head: str, base: str = "main", body: str = "") -> str:
    """Open a pull request."""
    try:
        repo = gh.get_repo(repo_name)
        pr = repo.create_pull(title=title, body=body, head=head, base=base)
        return f"PR #{pr.number} created: {pr.html_url}"
    except GithubException as e:
        return f"Error: {e.data.get('message', str(e))}"


@mcp.tool()
def merge_pull_request(repo_name: str, pr_number: int, commit_message: str = "Merged via MCP") -> str:
    """Merge an open pull request."""
    try:
        repo = gh.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        if not pr.mergeable:
            return f"PR #{pr_number} is not mergeable (conflicts or checks failing)."
        result = pr.merge(commit_message=commit_message)
        return f"PR #{pr_number} merged: {result.merged}"
    except GithubException as e:
        return f"Error: {e.data.get('message', str(e))}"


if __name__ == "__main__":
    mcp.run()

"""
Demo Workflow: branch → push file → open PR → merge PR
Run: python workflows/demo_workflow.py
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from server import create_branch, push_file, create_pull_request, merge_pull_request, list_branches

REPO = "maheshjagzap123/MCP-Server"
BRANCH = "feature/demo-workflow"

def run():
    print("=== GitHub MCP Demo Workflow ===\n")

    # Step 1: List existing branches
    print("[1] Listing branches...")
    print(list_branches(REPO))

    # Step 2: Create a new branch
    print("\n[2] Creating branch...")
    print(create_branch(REPO, BRANCH, from_branch="main"))

    # Step 3: Push a file to the new branch
    print("\n[3] Pushing file...")
    print(push_file(REPO, BRANCH, "demo/hello.txt", "Hello from MCP workflow!", "add demo file"))

    # Step 4: Open a PR
    print("\n[4] Creating pull request...")
    result = create_pull_request(REPO, "Demo: MCP Workflow PR", head=BRANCH, base="main", body="Auto-created by MCP demo workflow.")
    print(result)

    # Step 5: Merge the PR (extract PR number from result string)
    pr_number = int(result.split("#")[1].split(" ")[0])
    print(f"\n[5] Merging PR #{pr_number}...")
    print(merge_pull_request(REPO, pr_number))

    print("\n=== Workflow Complete ===")

if __name__ == "__main__":
    run()

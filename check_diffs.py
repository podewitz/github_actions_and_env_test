import os

from git import Repo
from github import Auth, Github


# repo = Repo(".")

# changed_files = [diff.a_path for diff in repo.head.commit.diff(None)]
# # for diff in repo.head.commit.diff(None):
# #     print(diff.a_path)

# print(f"__DEBUG0: {[diff.a_path for diff in repo.head.commit.diff(None)]}")
# print(f"__DEBUG1: {[diff.a_path for diff in repo.head.commit.diff("main")]}")
# print(f"__DEBUG2: {[diff.a_path for diff in repo.head.commit.diff("origin/main")]}")

with open("__diffs.txt", "r") as f:
    changed_files = [line.strip() for line in f.readlines() if line.strip()]

tables_to_check = {}
for changed_file in changed_files:
    print(f"Changed file: {changed_file}")
    # 1. Extract output table name(s)
    # 2. Get last access time of table for "normal" users using "ODBC Cluster"
    # 3. Add to list if applicable
    tables_to_check[changed_file] = []

# 3. Check if any table was changed that could affect users and raise Exception if so
# if tables_to_check:
#     formated_tables = [f"{table}: {users}" for table, users in tables_to_check.items()]
#     raise Exception(
#         "The following tables were changed that may affect users:"
#         + "\n  * ".join(formated_tables)
#     )

token = os.getenv("GITHUB_TOKEN")
print(f"Using token: {token=}")

# Public Web Github
g = Github(auth=Auth.Token(token))

full_repo_name = os.getenv("GITHUB_REPO")
print(f"Using repo: {full_repo_name=}")
repo = g.get_repo(full_repo_name)

pull_number = int(os.getenv("GITHUB_PR_NUMBER"))
print(f"Using pull number: {pull_number=}")
pull_request = repo.get_pull(number=pull_number)

last_commit = repo.get_commit(pull_request.head.sha)
print(f"{type(last_commit)=}")
print(f"{last_commit=}")

# TODO: We need a separate token for the bot to comment on PRs
for file, users in tables_to_check.items():
    print(f"File: {file}, Users: {users}")
    pull_request.create_review_comment(
        body=f"This is a test for {file} with {users}",
        commit=last_commit,
        path=file,
        subject_type="file",
    )

# To close connections after use
g.close()

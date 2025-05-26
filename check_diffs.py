from git import Repo


repo = Repo(".")

for diff in repo.head.commit.diff("main"):
    print(diff.a_path)

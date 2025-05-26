from git import Repo


repo = Repo(".")

changed_files = [diff.a_path for diff in repo.head.commit.diff(None)]
# for diff in repo.head.commit.diff(None):
#     print(diff.a_path)

tables_to_check = {}
for changed_file in changed_files:
    print(f"Changed file: {changed_file}")
    # 1. Extract output table name(s)
    # 2. Get last access time of table for "normal" users using "ODBC Cluster"
    # 3. Add to list if applicable

# 3. Check if any table was changed that could affect users and raise Exception if so
if tables_to_check:
    formated_tables = [f"{table}: {users}" for table, users in tables_to_check.items()]
    raise Exception(
        "The following tables were changed that may affect users:"
        + "\n  * ".join(formated_tables)
    )

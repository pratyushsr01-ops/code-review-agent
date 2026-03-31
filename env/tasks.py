from .models import PRFile

TASKS = {
    "task_1_easy_obvious_bug": {
        "pr_title": "Fix user pagination",
        "pr_description": "Updated the pagination loop to include the final page.",
        "files": [PRFile(
            filename="pagination.py",
            content_with_lines=(
                "1: def get_pages(total_items, page_size):\n"
                "2:     pages = total_items // page_size\n"
                "3:     for i in range(1, pages):\n"
                "4:         yield i\n"
                "5:     return"
            )
        )],
        "expected_findings": [
            {
                "line": 3,
                "category": "bug",
                "keywords": ["range", "off by one", "off-by-one", "pages + 1",
                             "missing", "last page", "final page"]
            }
        ]
    },

    "task_2_medium_multi_issue": {
        "pr_title": "Add user search feature",
        "pr_description": "Implemented a quick search endpoint for the admin dashboard.",
        "files": [PRFile(
            filename="search.py",
            content_with_lines=(
                "1: import sys\n"
                "2: def search_users(db_cursor, username):\n"
                "3:     query = f\"SELECT * FROM users WHERE name = '{username}'\"\n"
                "4:     db_cursor.execute(query)\n"
                "5:     results = db_cursor.fetchall()\n"
                "6:     if results == None:\n"
                "7:         return []\n"
                "8:     return results"
            )
        )],
        "expected_findings": [
            {
                "line": 1,
                "category": "style",
                "keywords": ["unused", "import", "sys"]
            },
            {
                "line": 3,
                "category": "security",
                "keywords": ["injection", "sql", "parameteriz", "sanitiz",
                             "f-string", "format", "unsafe"]
            },
            {
                "line": 6,
                "category": "bug",
                "keywords": ["none", "is none", "comparison",
                             "not results", "equality"]
            }
        ]
    },

    "task_3_hard_architecture": {
        "pr_title": "Load dashboard data for all users",
        "pr_description": "Fetches posts for every active user to render the admin dashboard.",
        "files": [PRFile(
            filename="dashboard.py",
            content_with_lines=(
                "1:  def load_dashboard(session):\n"
                "2:      users = session.query(User).filter_by(active=True).all()\n"
                "3:      result = []\n"
                "4:      for user in users:\n"
                "5:          posts = session.query(Post).filter_by(user_id=user.id).all()\n"
                "6:          result.append({'user': user.name, 'posts': len(posts)})\n"
                "7:      return result\n"
                "8:\n"
                "9:  def update_user_status(session, user_id, status):\n"
                "10:     user = session.query(User).filter_by(id=user_id).first()\n"
                "11:     session.commit()\n"
                "12:     user.status = status\n"
                "13:     session.commit()"
            )
        )],
        "expected_findings": [
            {
                "line": 5,
                "category": "performance",
                "keywords": ["n+1", "n plus 1", "query", "loop",
                             "joinedload", "eager", "batch"]
            },
            {
                "line": 11,
                "category": "bug",
                "keywords": ["commit", "order", "before", "after",
                             "race", "status", "wrong order"]
            }
        ]
    }
}
MEDIUM_TASKS = [
    {
        "id": "med_1",
        "code": "def get_user(db, username):\n    query = \"SELECT * FROM users WHERE name = '%s'\" % username\n    db.execute(query)\n    return db.fetchone()\n",
        "is_vulnerable": True,
        "vulnerable_lines": [2]
    },
    {
        "id": "med_2",
        "code": "def get_user_safe(db, username):\n    query = \"SELECT * FROM users WHERE name = ?\"\n    db.execute(query, (username,))\n    return db.fetchone()\n",
        "is_vulnerable": False,
        "vulnerable_lines": []
    },
    {
        "id": "med_3",
        "code": "def search(db, term):\n    db.execute(f\"SELECT * FROM items WHERE description LIKE '%{term}%'\")\n    return db.fetchall()\n",
        "is_vulnerable": True,
        "vulnerable_lines": [2]
    },
    {
        "id": "med_4",
        "code": "def update_profile(db, user_id, bio):\n    q = \"UPDATE profiles SET bio = :bio WHERE id = :id\"\n    db.execute(q, {\"bio\": bio, \"id\": user_id})\n    db.commit()\n",
        "is_vulnerable": False,
        "vulnerable_lines": []
    },
    {
        "id": "med_5",
        "code": "def delete_user(db, user_id):\n    q = \"DELETE FROM users WHERE id = \" + str(user_id)\n    db.execute(q)\n    db.commit()\n",
        "is_vulnerable": True,
        "vulnerable_lines": [2]
    },
    {
        "id": "med_6",
        "code": "def login(db, username, password):\n    q = \"SELECT id FROM users WHERE uname='{}' AND pwd='{}'\".format(username, password)\n    db.execute(q)\n    return db.fetchone()\n",
        "is_vulnerable": True,
        "vulnerable_lines": [2]
    },
    {
        "id": "med_7",
        "code": "def get_items(db, category):\n    if not category.isalnum(): return []\n    q = f\"SELECT * FROM {category}_items\"\n    db.execute(q)\n    return db.fetchall()\n",
        "is_vulnerable": False, # Validated before format
        "vulnerable_lines": []
    },
    {
        "id": "med_8",
        "code": "def fetch_admin(db):\n    db.execute(\"SELECT * FROM users WHERE role = 'admin' LIMIT 1\")\n    return db.fetchone()\n",
        "is_vulnerable": False,
        "vulnerable_lines": [] # No inputs
    }
]

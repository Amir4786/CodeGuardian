HARD_TASKS = [
    {
        "id": "hard_1",
        "instruction": "The following function is vulnerable to SQL injection. Rewrite it to be secure, preserving its functionality.",
        "code": "def authenticate(db, username, password):\n    query = \"SELECT * FROM admins WHERE username='%s' AND password='%s'\" % (username, password)\n    db.execute(query)\n    return db.fetchone()\n",
        "expected_fixes": ["?", "execute", "db.execute(query,"] # Expected to use parameterized queries
    },
    {
        "id": "hard_2",
        "instruction": "This function hardcodes a secret API token. Rewrite it so that the token is loaded from an environment variable named 'STRIPE_API_KEY'.",
        "code": "def init_payment():\n    stripe_token = 'sk_test_4eC39HqLyjWDarjtT1zdp7dc'\n    stripe.api_key = stripe_token\n    return True\n",
        "expected_fixes": ["os.environ", "STRIPE_API_KEY", "getenv", "environ.get"] # Looking for environment variable usage
    }
]

EASY_TASKS = [
    {
        "id": "easy_1",
        "code": "def connect():\n    api_key = 'sk-live-1234567890abcdef'\n    print('connecting...')\n",
        "has_secret": True,
        "secret_lines": [2]
    },
    {
        "id": "easy_2",
        "code": "def greet(name):\n    print(f'Hello {name}')\n    return True\n",
        "has_secret": False,
        "secret_lines": []
    },
    {
        "id": "easy_3",
        "code": "import requests\ndef fetch():\n    headers = {'Authorization': 'Bearer abc123def456'}\n    return requests.get('https://api.example.com', headers=headers)\n",
        "has_secret": True,
        "secret_lines": [3]
    },
    {
        "id": "easy_4",
        "code": "import os\ndef get_token():\n    return os.environ.get('API_TOKEN', 'default_token')\n",
        "has_secret": False,
        "secret_lines": []
    },
    {
        "id": "easy_5",
        "code": "class Config:\n    DEBUG = True\n    PASSWORD = 'super_secret_password_123!'\n    PORT = 8080\n",
        "has_secret": True,
        "secret_lines": [3]
    }
]

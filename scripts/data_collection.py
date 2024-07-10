import requests
import os
from dotenv import load_dotenv
import json

# Load environment variables from .env file
load_dotenv()

def fetch_repos(query, num_repos):
    url = f'https://api.github.com/search/repositories?q={query}&sort=stars&order=desc'
    response = requests.get(url, headers={'Authorization': f'token {os.getenv("GITHUB_API_TOKEN")}'})
    data = response.json()
    return data['items'][:num_repos]

def save_repos_to_file(repos, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(repos, f, indent=4)

repos = fetch_repos('language:HTML+language:CSS+language:JavaScript', 100)
save_repos_to_file(repos, './data/raw/repos.json')

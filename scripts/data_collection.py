import requests
import os
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def fetch_repos(query, num_repos):
    url = f'https://api.github.com/search/repositories?q={query}&sort=stars&order=desc'
    token = os.getenv("GITHUB_API_TOKEN")
    
    if not token:
        print("Error: GITHUB_API_TOKEN environment variable is not set.")
        return []

    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Error: Failed to fetch repositories. Status code: {response.status_code}")
        print(response.json())
        return []
    
    data = response.json()
    return data.get('items', [])[:num_repos]

def save_repos_to_file(repos, filepath):
    # Ensure the directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    # Save the repository data to a JSON file
    with open(filepath, 'w') as f:
        json.dump(repos, f, indent=4)

# Fetch repositories
repos = fetch_repos('language:HTML+language:CSS+language:JavaScript', 100)

# Debugging: Print the number of repositories fetched
print(f"Fetched {len(repos)} repositories")

# Save repository data to a JSON file in the data/raw directory
save_repos_to_file(repos, 'data/raw/repos.json')

# Debugging: Verify if the file was created and contains data
if os.path.exists('data/raw/repos.json'):
    print("repos.json created successfully")
    with open('data/raw/repos.json', 'r') as f:
        data = json.load(f)
        print(f"Number of repositories saved: {len(data)}")
else:
    print("Error: repos.json was not created")

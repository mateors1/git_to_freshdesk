import argparse
import os
import requests

GITHUB_API_BASE_URL = 'https://api.github.com'
FRESHDESK_API_BASE_URL = 'https://{subdomain}.freshdesk.com/api/v2'

# Retrieve GitHub user information
def get_github_user(username):
    url = f'{GITHUB_API_BASE_URL}/users/{username}'
    headers = {'Authorization': f'token {os.environ.get("GITHUB_TOKEN")}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f'Failed to retrieve GitHub user information: {response.text}')

# Create or update Freshdesk contact
def create_or_update_freshdesk_contact(subdomain, contact):
    url = f'{FRESHDESK_API_BASE_URL.format(subdomain=subdomain)}/contacts'
    headers = {'Content-Type': 'application/json'}
    headers['Authorization'] = f'Token token={os.environ.get("FRESHDESK_TOKEN")}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        contacts = response.json()
        existing_contact = next((c for c in contacts if c['email'] == contact['email']), None)
        if existing_contact:
            contact_id = existing_contact['id']
            url = f'{FRESHDESK_API_BASE_URL.format(subdomain=subdomain)}/contacts/{contact_id}'
            response = requests.put(url, headers=headers, json=contact)
        else:
            response = requests.post(url, headers=headers, json=contact)
        if response.status_code == 201 or response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'Failed to create/update Freshdesk contact: {response.text}')
    else:
        raise Exception(f'Failed to retrieve Freshdesk contacts: {response.text}')

def main():
    parser = argparse.ArgumentParser(description='GitHub to Freshdesk Contact Sync')
    parser.add_argument('github_username', type=str, help='GitHub username')
    parser.add_argument('freshdesk_subdomain', type=str, help='Freshdesk subdomain')
    args = parser.parse_args()

    github_username = args.github_username
    freshdesk_subdomain = args.freshdesk_subdomain

    github_user = get_github_user(github_username)

    # Transfer compatible fields from GitHub to Freshdesk
    freshdesk_contact = {
        'name': github_user['name'],
        'email': github_user['email'],
        'phone': github_user['phone'],
        # Add more fields as needed
    }

    result = create_or_update_freshdesk_contact(freshdesk_subdomain, freshdesk_contact)
    print(f'Contact created/updated in Freshdesk. Contact ID: {result["id"]}')

if __name__ == '__main__':
    main()


# GitHub and Freshdesk Contact Sync

This command line Python program retrieves information from a GitHub user and creates or updates a contact in Freshdesk using their respective APIs.

## Requirements

- Python 3.x
- Requests library (install with `pip install requests`)

## Usage

1. Set the following environment variables before running the program:
   - `GITHUB_TOKEN`: GitHub personal access token
   - `FRESHDESK_TOKEN`: Freshdesk API key

   These environment variables are necessary for authentication with the respective APIs. Make sure to replace `<github_token>` and `<freshdesk_token>` with the actual tokens.

   For example, on Linux/macOS, you can set the environment variables using the following commands:
      export GITHUB_TOKEN=<github_token>
      export FRESHDESK_TOKEN=<freshdesk_token>



On Windows, you can set the environment variables using the following commands:
      set GITHUB_TOKEN=<github_token>
      set FRESHDESK_TOKEN=<freshdesk_token>


2. Run the program using the following command:
python github_freshdesk_sync.py <github_username> <freshdesk_subdomain>


Replace `<github_username>` with the GitHub username and `<freshdesk_subdomain>` with your Freshdesk subdomain.

## Running the Tests

To run the unit tests, execute the following command:

python -m unittest test_github_to_freshdesk.py



The tests will validate the functionality of retrieving GitHub user information and creating/updating a contact in Freshdesk.


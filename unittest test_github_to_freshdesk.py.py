import unittest
from unittest.mock import patch
from github_freshdesk_sync import get_github_user, create_or_update_freshdesk_contact

class GitHubFreshdeskSyncTest(unittest.TestCase):
    @patch('github_freshdesk_sync.requests.get')
    def test_get_github_user_success(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1 123-456-7890',
            # Add more fields as needed
        }
        result = get_github_user('johndoe')
        self.assertEqual(result['name'], 'John Doe')

    @patch('github_freshdesk_sync.requests.get')
    def test_get_github_user_failure(self, mock_get):
        mock_get.return_value.status_code = 404
        with self.assertRaises(Exception):
            get_github_user('johndoe')

    @patch('github_freshdesk_sync.requests.get')
    @patch('github_freshdesk_sync.requests.post')
    def test_create_freshdesk_contact_success(self, mock_post, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [
            {
                'id': 1,
                'name': 'John Doe',
                'email': 'john.doe@example.com',
                'phone': '+1 123-456-7890',
                # Add more fields as needed
            }
        ]
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {'id': 1}
        contact = {
            'name': 'John Doe',
            'email': 'john.doe@example.com',
            'phone': '+1 123-456-7890',
            # Add more fields as needed
        }
        result = create_or_update_freshdesk_contact('example', contact)
        self.assertEqual(result['id'], 1)

    @patch('github_freshdesk_sync.requests.get')
    @patch('github_freshdesk_sync.requests.post')
    def test_create_freshdesk_contact_failure(self, mock_post, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        mock_post.return_value.status_code = 400
        with self.assertRaises(Exception):
            create_or_update_freshdesk_contact('example', {})

if __name__ == '__main__':
    unittest.main()

import json
import unittest
import os
import json

def verify_json(file_path):
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return True

    try:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
    except json.JSONDecodeError:
        print(f"File {file_path} is not a valid JSON file.")
        return True

    if 'PolicyDocument' not in data:
        print(f"File {file_path} does not have a PolicyDocument key.")
        return True

    if 'Statement' not in data['PolicyDocument']:
        print(f"File {file_path} does not have a Statement key.")
        return True

    statements = data.get('PolicyDocument', {}).get('Statement', [])
    for statement in statements:
        if 'Resource' not in statement:
            print(f"File {file_path} does not have a Resource key in one of the statements.")
            return True
        if statement.get('Resource') == '*':
            return False

    return True


class TestVerifyJson(unittest.TestCase):
    def test_verify_json_false(self):
        self.assertEqual(verify_json('test1.json'), False)

    def test_verify_json_true(self):
        self.assertEqual(verify_json('test2.json'), True)

    def test_file_not_exists(self):
        self.assertEqual(verify_json('nonexistent.json'), True)

    def test_invalid_json(self):
        self.assertEqual(verify_json('test4.json'), True)

    def test_no_policy_document(self):
        self.assertEqual(verify_json('test5.json'), True)

    def test_no_statement(self):
        self.assertEqual(verify_json('test6.json'), True)

    def test_no_resource(self):
        self.assertEqual(verify_json('test7.json'), True)

if __name__ == '__main__':
    unittest.main()
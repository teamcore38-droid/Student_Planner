import unittest
import os
import json
from src.models.auth import AuthService
from src.models.task import Task
from src.models.persistence import PersistenceService

class TestAuthService(unittest.TestCase):
    """Verifies that registration, credentials hashing, and session management are robust."""
    def setUp(self):
        self.auth = AuthService()
        self.mock_users = {}

    def test_hash_consistency(self):
        salt = "a1b2c3d4e5f67890"
        p1 = "secure_password"
        h1 = self.auth.hash_password(p1, salt)
        h2 = self.auth.hash_password(p1, salt)
        self.assertEqual(h1, h2)
        # Unique salt should produce different hashes for same password
        salt2 = "9876543210fedcba"
        h3 = self.auth.hash_password(p1, salt2)
        self.assertNotEqual(h1, h3)

    def test_registration_validation(self):
        # Enforce minimum password length
        success, msg = self.auth.register_user(self.mock_users, "student1", "123")
        self.assertFalse(success)
        self.assertIn("at least 6 characters", msg)

        # Enforce non-empty username
        success, msg = self.auth.register_user(self.mock_users, "  ", "password123")
        self.assertFalse(success)
        
        # Enforce successful registration
        success, msg = self.auth.register_user(self.mock_users, "student1", "password123")
        self.assertTrue(success)
        self.assertIn("student1", self.mock_users)
        self.assertIsNotNone(self.mock_users["student1"].get("salt"))
        self.assertIsNotNone(self.mock_users["student1"].get("password_hash"))

        # Enforce duplicate prevention
        success2, msg2 = self.auth.register_user(self.mock_users, "STUDENT1", "password456")
        self.assertFalse(success2)

    def test_login_verification(self):
        # Register test profile
        self.auth.register_user(self.mock_users, "alex", "my_secret_code")
        
        # Test incorrect username
        success, msg = self.auth.verify_login(self.mock_users, "wrong_user", "my_secret_code")
        self.assertFalse(success)
        self.assertIsNone(self.auth.get_active_user())
        
        # Test incorrect password
        success, msg = self.auth.verify_login(self.mock_users, "alex", "wrong_code")
        self.assertFalse(success)
        self.assertIsNone(self.auth.get_active_user())
        
        # Test success login
        success, msg = self.auth.verify_login(self.mock_users, "alex", "my_secret_code")
        self.assertTrue(success)
        self.assertEqual(self.auth.get_active_user(), "alex")
        
        # Test logout session termination
        self.auth.logout()
        self.assertIsNone(self.auth.get_active_user())


class TestTask(unittest.TestCase):
    """Verifies that the task data structures serialize and deserialize with complete integrity."""
    def test_task_serialization(self):
        task = Task(
            title="Complete Portfolio Draft",
            module="LDC6004M",
            due_date="2026-06-11",
            priority="High",
            notes="Requires 2000 words narrative",
            username="student_user"
        )
        task_dict = task.to_dict()
        
        self.assertEqual(task_dict["title"], "Complete Portfolio Draft")
        self.assertEqual(task_dict["module"], "LDC6004M")
        self.assertEqual(task_dict["priority"], "High")
        self.assertEqual(task_dict["completed"], False)
        self.assertEqual(task_dict["username"], "student_user")
        self.assertIsNotNone(task_dict["task_id"])

        # Reconstruction
        reconstructed = Task.from_dict(task_dict)
        self.assertEqual(reconstructed.task_id, task.task_id)
        self.assertEqual(reconstructed.title, task.title)
        self.assertEqual(reconstructed.due_date, task.due_date)
        self.assertEqual(reconstructed.completed, task.completed)


class TestPersistenceService(unittest.TestCase):
    """Verifies atomic write safety, schema compliance, and auto-backup recovery."""
    def setUp(self):
        self.test_file = "test_db.json"
        self.test_backup = self.test_file + ".bak"
        self.test_temp = self.test_file + ".tmp"
        self.persistence = PersistenceService(self.test_file)

    def tearDown(self):
        # Cleanup test filesystem footprints
        for path in [self.test_file, self.test_backup, self.test_temp, self.test_file + ".corrupt"]:
            if os.path.exists(path):
                os.remove(path)

    def test_store_initialization(self):
        self.assertTrue(os.path.exists(self.test_file))
        data = self.persistence.load_data()
        self.assertIn("users", data)
        self.assertIn("tasks", data)
        self.assertEqual(len(data["tasks"]), 0)

    def test_atomic_transaction_save(self):
        mock_users = {"sarah": {"password_hash": "abc", "salt": "123"}}
        mock_tasks = [{"task_id": "1", "title": "Check Code", "completed": True}]
        
        success, msg = self.persistence.save_data(mock_users, mock_tasks)
        self.assertTrue(success)
        
        # Verify saved data structure
        loaded = self.persistence.load_data()
        self.assertEqual(loaded["users"]["sarah"]["password_hash"], "abc")
        self.assertEqual(len(loaded["tasks"]), 1)
        self.assertEqual(loaded["tasks"][0]["title"], "Check Code")
        
        # Verify that backup file was also created
        self.assertTrue(os.path.exists(self.test_backup))

    def test_corruption_recovery(self):
        # Step 1: Save state twice so it rolls into the backup file
        self.persistence.save_data(
            {"valid_user": {}}, 
            [{"task_id": "99", "title": "Secure Draft"}]
        )
        self.persistence.save_data(
            {"valid_user": {}}, 
            [{"task_id": "99", "title": "Secure Draft"}]
        )
        
        # Step 2: Intentionally corrupt the primary database file
        with open(self.test_file, 'w', encoding='utf-8') as f:
            f.write("{ broken json state ... ")
            
        # Step 3: Trigger load, which should detect corruption and auto-restore from backup
        loaded = self.persistence.load_data()
        self.assertIn("valid_user", loaded["users"])
        self.assertEqual(loaded["tasks"][0]["title"], "Secure Draft")
        
        # Check that the broken primary was moved to a .corrupt path for analysis
        self.assertTrue(os.path.exists(self.test_file + ".corrupt"))


if __name__ == "__main__":
    unittest.main()

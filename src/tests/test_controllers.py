import unittest
import os
from datetime import datetime, timedelta
from src.controllers.validation import InputValidator
from src.controllers.main_controller import MainController

class TestInputValidator(unittest.TestCase):
    """Verifies that all text forms and academic date restrictions are thoroughly validated."""
    def test_title_validation(self):
        # Empty title rejected
        success, msg = InputValidator.validate_task_inputs(
            "", "LDC6004M", "2026-06-11", "Medium"
        )
        self.assertFalse(success)
        self.assertIn("title is required", msg)

        # Excessively long title rejected
        success, msg = InputValidator.validate_task_inputs(
            "A" * 61, "LDC6004M", "2026-06-11", "Medium"
        )
        self.assertFalse(success)

    def test_module_validation(self):
        # Empty module rejected
        success, msg = InputValidator.validate_task_inputs(
            "Task 1", "", "2026-06-11", "Medium"
        )
        self.assertFalse(success)
        self.assertIn("module is required", msg)

    def test_due_date_validation(self):
        # Invalid format rejected
        success, msg = InputValidator.validate_task_inputs(
            "Task 1", "LDC6004M", "11/06/2026", "Medium"
        )
        self.assertFalse(success)
        self.assertIn("YYYY-MM-DD format", msg)

        # Invalid calendar date rejected
        success, msg = InputValidator.validate_task_inputs(
            "Task 1", "LDC6004M", "2026-02-31", "Medium"
        )
        self.assertFalse(success)
        self.assertIn("Invalid calendar date", msg)

        # Date in the past rejected
        yesterday_str = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        success, msg = InputValidator.validate_task_inputs(
            "Task 1", "LDC6004M", yesterday_str, "Medium"
        )
        self.assertFalse(success)
        self.assertIn("cannot be in the past", msg)

        # Today or future date accepted
        today_str = datetime.now().strftime("%Y-%m-%d")
        success, msg = InputValidator.validate_task_inputs(
            "Task 1", "LDC6004M", today_str, "Medium"
        )
        self.assertTrue(success)

    def test_priority_validation(self):
        # Invalid priority rejected
        success, msg = InputValidator.validate_task_inputs(
            "Task 1", "LDC6004M", "2026-06-11", "Critical"
        )
        self.assertFalse(success)


class TestMainController(unittest.TestCase):
    """Verifies student isolation scoping, database metrics, and search algorithms."""
    def setUp(self):
        self.test_file = "test_controller_db.json"
        self.controller = MainController(self.test_file)
        
        # Register and login primary student
        self.controller.register("sarah", "password123")
        self.controller.login("sarah", "password123")

    def tearDown(self):
        # Cleanup file impacts
        for path in [self.test_file, self.test_file + ".bak", self.test_file + ".tmp", self.test_file + ".corrupt"]:
            if os.path.exists(path):
                os.remove(path)

    def test_user_scoping(self):
        # Sarah adds a task
        success, msg = self.controller.add_task(
            "Sarah's Task", "LDC6004M", "2026-06-11", "High", "Dissertation milestone"
        )
        self.assertTrue(success)
        
        sarah_tasks = self.controller.get_user_tasks()
        self.assertEqual(len(sarah_tasks), 1)
        self.assertEqual(sarah_tasks[0].title, "Sarah's Task")

        # Login another student (David)
        self.controller.register("david", "securePass456")
        self.controller.login("david", "securePass456")
        
        # David should see exactly zero tasks
        david_tasks = self.controller.get_user_tasks()
        self.assertEqual(len(david_tasks), 0)

        # David adds his own task
        self.controller.add_task(
            "David's Task", "LDC6001M", "2026-06-12", "Medium"
        )
        david_tasks = self.controller.get_user_tasks()
        self.assertEqual(len(david_tasks), 1)
        self.assertEqual(david_tasks[0].title, "David's Task")

        # Switching back to Sarah
        self.controller.login("sarah", "password123")
        sarah_tasks = self.controller.get_user_tasks()
        self.assertEqual(len(sarah_tasks), 1)
        self.assertEqual(sarah_tasks[0].title, "Sarah's Task")

    def test_task_operations_crud(self):
        # Add task
        self.controller.add_task("Core UI Draft", "LDC6004M", "2026-06-11", "High")
        task = self.controller.get_user_tasks()[0]
        task_id = task.task_id
        
        # Toggle completion
        self.controller.toggle_task_completion(task_id)
        self.assertTrue(self.controller.get_user_tasks()[0].completed)
        
        # Edit task properties
        self.controller.edit_task(task_id, "Core UI Finished", "LDC6004M", "2026-06-15", "Low", "Fully verified")
        updated = self.controller.get_user_tasks()[0]
        self.assertEqual(updated.title, "Core UI Finished")
        self.assertEqual(updated.priority, "Low")
        self.assertEqual(updated.notes, "Fully verified")
        
        # Delete task
        self.controller.delete_task(task_id)
        self.assertEqual(len(self.controller.get_user_tasks()), 0)

    def test_search_and_filtering(self):
        self.controller.add_task("Write Dissertation Proposal", "Dissertation", "2026-06-15", "High", "Submit to portal")
        self.controller.add_task("Code Navigation GUI", "LDC6004M", "2026-06-16", "Medium")
        self.controller.add_task("Read AI syllabus", "LDC6002M", "2026-06-17", "Low", "Focus on Deep Learning")

        # Search by title keyword (case-insensitive)
        matches = self.controller.search_tasks("dissertation")
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].title, "Write Dissertation Proposal")

        # Search by priority chip filter
        high_matches = self.controller.search_tasks("", "High")
        self.assertEqual(len(high_matches), 1)
        self.assertEqual(high_matches[0].title, "Write Dissertation Proposal")
        
        # Search by priority combined with text keyword
        combined = self.controller.search_tasks("navigation", "Medium")
        self.assertEqual(len(combined), 1)
        self.assertEqual(combined[0].title, "Code Navigation GUI")

    def test_upcoming_impending_deadlines(self):
        # 1. Add a task due in 24 hours (impending)
        tmw_str = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.controller.add_task("Due tomorrow", "LDC6004M", tmw_str, "High")

        # 2. Add a task due in 5 days (far future)
        future_str = (datetime.now() + timedelta(days=5)).strftime("%Y-%m-%d")
        self.controller.add_task("Due next week", "LDC6004M", future_str, "Low")

        # Fetch upcoming tasks within 48h limit
        upcoming = self.controller.get_upcoming_tasks(48)
        self.assertEqual(len(upcoming), 1)
        self.assertEqual(upcoming[0].title, "Due tomorrow")

    def test_dashboard_metrics_compilation(self):
        # Empty list check
        metrics = self.controller.get_dashboard_metrics()
        self.assertEqual(metrics["total"], 0)
        self.assertEqual(metrics["ratio"], 0)

        # Add active tasks
        self.controller.add_task("T1", "M1", "2026-06-11", "High")
        self.controller.add_task("T2", "M1", "2026-06-11", "Medium")
        self.controller.add_task("T3", "M2", "2026-06-11", "Low")
        
        metrics = self.controller.get_dashboard_metrics()
        self.assertEqual(metrics["total"], 3)
        self.assertEqual(metrics["pending"], 3)
        self.assertEqual(metrics["completed"], 0)
        self.assertEqual(metrics["ratio"], 0)
        self.assertEqual(metrics["high_priority_pending"], 1)

        # Complete T1
        t1_id = self.controller.get_user_tasks()[0].task_id
        self.controller.toggle_task_completion(t1_id)
        
        metrics = self.controller.get_dashboard_metrics()
        self.assertEqual(metrics["completed"], 1)
        self.assertEqual(metrics["pending"], 2)
        # 1 out of 3 completed is 33% completion score
        self.assertEqual(metrics["ratio"], 33)
        self.assertEqual(metrics["high_priority_pending"], 0)


if __name__ == "__main__":
    unittest.main()

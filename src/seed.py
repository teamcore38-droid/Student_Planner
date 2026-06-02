import sys
import os
from datetime import datetime, timedelta

# Ensure project root is in sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.controllers.main_controller import MainController

def seed_database():
    print("[START] Initializing database seeding process...")
    
    # Path to database file
    db_path = "storage.json"
    
    # Instantiate MainController (creates/loads DB file)
    controller = MainController(db_path)
    
    # 1. Register a sample student
    username = "student"
    password = "password123"
    
    # Check if student already exists
    if username in controller.db["users"]:
        print(f"[INFO] User '{username}' already exists. Re-seeding tasks for this user...")
    else:
        success, msg = controller.register(username, password)
        if success:
            print(f"[SUCCESS] Registered profile: '{username}' with password: '{password}'")
        else:
            print(f"[ERROR] Registration failed: {msg}")
            return
            
    # Force login session context
    controller.login(username, password)
    print(f"[AUTH] Logged in as session user: '{username}'")

    # 2. Clear old tasks for 'student' if re-seeding
    controller.tasks_cache = [t for t in controller.tasks_cache if t.username != username]

    # Calculate relative dates to ensure the dashboard's upcoming panel shows active items
    today = datetime.now()
    tomorrow_str = (today + timedelta(days=1)).strftime("%Y-%m-%d")
    in_3_days_str = (today + timedelta(days=3)).strftime("%Y-%m-%d")
    in_4_days_str = (today + timedelta(days=4)).strftime("%Y-%m-%d")
    in_6_days_str = (today + timedelta(days=6)).strftime("%Y-%m-%d")
    in_8_days_str = (today + timedelta(days=8)).strftime("%Y-%m-%d")

    # 3. Add Coursework tasks across multiple university modules
    
    # Module: LDC6004M (Mobile Application Development)
    controller.add_task(
        title="Complete Kivy GUI implementation",
        module="LDC6004M",
        due_date=tomorrow_str,
        priority="High",
        notes="Connect LoginScreen, Dashboard, TaskList, TaskForm, and Settings views to MainController."
    )
    
    controller.add_task(
        title="Draft Reflective Narrative report",
        module="LDC6004M",
        due_date=in_4_days_str,
        priority="High",
        notes="Reflect on Kivy frameworks selection, MVC SoC testability, and Transactional Atomic json saves. Word count: 1750."
    )

    # Module: LDC6003M (Dissertation)
    controller.add_task(
        title="Complete Literature Review Chapter",
        module="LDC6003M",
        due_date=in_6_days_str,
        priority="High",
        notes="Submit chapter outline to dissertation tutor portal. Reference cognitive models and study methodologies."
    )

    # Module: LDC6002M (Artificial Intelligence)
    controller.add_task(
        title="Run neural network benchmarks",
        module="LDC6002M",
        due_date=in_8_days_str,
        priority="Medium",
        notes="Compare regression loss ratios against epoch sets and learning rates."
    )

    # Module: LDC6001M (Software Engineering Principles)
    controller.add_task(
        title="Read syllabus literature (Clean Code)",
        module="LDC6001M",
        due_date=in_3_days_str,
        priority="Low",
        notes="Focus on solid software architecture conventions and separation of concerns."
    )
    
    # Mark the Low Priority task as completed so we have a nice progress percentage visual on boot!
    user_tasks = controller.get_user_tasks()
    for t in user_tasks:
        if "Clean Code" in t.title:
            controller.toggle_task_completion(t.task_id)
            print("[UPDATE] Marked 'Read syllabus literature (Clean Code)' as COMPLETED.")
            break

    print("[SAVE] Committing tasks to storage.json atomically...")
    controller.sync_save()
    
    print("[FINISHED] Seeding completed successfully!")
    print(f"-> Login username: '{username}'")
    print(f"-> Login password: '{password}'")

if __name__ == "__main__":
    seed_database()

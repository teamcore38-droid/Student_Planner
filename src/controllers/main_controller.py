from datetime import datetime, timedelta
from src.models.auth import AuthService
from src.models.task import Task
from src.models.persistence import PersistenceService
from src.controllers.validation import InputValidator

class MainController:
    """
    Controller Layer: The central hub managing session flow, in-memory states,
    academic metrics calculations, and synchronizing View interactions with Model persistence.
    """
    def __init__(self, storage_path: str = "storage.json"):
        self.persistence = PersistenceService(storage_path)
        self.auth = AuthService()
        
        # In-memory database cache
        self.db = {"users": {}, "tasks": []}
        self.tasks_cache: list[Task] = []
        
        # Load database initial state
        self.sync_load()

    def sync_load(self) -> None:
        """Loads data from local persistence and populates the in-memory Task objects cache."""
        self.db = self.persistence.load_data()
        self.tasks_cache = [Task.from_dict(t) for t in self.db.get("tasks", [])]

    def sync_save(self) -> tuple[bool, str]:
        """Serializes the in-memory Task objects and saves the entire store to disk atomically."""
        serialized_tasks = [t.to_dict() for t in self.tasks_cache]
        return self.persistence.save_data(self.db["users"], serialized_tasks)

    # --- Authentication Interfaces ---

    def register(self, username: str, password: str) -> tuple[bool, str]:
        """
        Registers a new student and commits credentials to secure storage.
        """
        success, msg = self.auth.register_user(self.db["users"], username, password)
        if success:
            self.sync_save()
        return success, msg

    def login(self, username: str, password: str) -> tuple[bool, str]:
        """
        Authenticates a student and caches their active session context.
        """
        success, msg = self.auth.verify_login(self.db["users"], username, password)
        return success, msg

    def logout(self) -> None:
        """Terminates active session."""
        self.auth.logout()

    def get_logged_in_user(self) -> str | None:
        """Gets active session username."""
        return self.auth.get_active_user()

    # --- Task CRUD Operations (Isolated to the logged-in student) ---

    def get_user_tasks(self) -> list[Task]:
        """
        Gets only the tasks belonging to the active user.
        
        Returns:
            list[Task]: List of Task instances owned by the student.
        """
        user = self.get_logged_in_user()
        if not user:
            return []
        return [t for t in self.tasks_cache if t.username == user]

    def add_task(
        self,
        title: str,
        module: str,
        due_date: str,
        priority: str,
        notes: str = ""
    ) -> tuple[bool, str]:
        """
        Creates and saves a new task after running sanitization checks.
        """
        user = self.get_logged_in_user()
        if not user:
            return False, "Session expired or inactive. Please log in."

        # Run validation
        is_valid, err_msg = InputValidator.validate_task_inputs(
            title, module, due_date, priority, notes
        )
        if not is_valid:
            return False, err_msg

        # Instantiate task bound to the active user
        new_task = Task(
            title=title,
            module=module,
            due_date=due_date,
            priority=priority,
            notes=notes,
            username=user
        )
        self.tasks_cache.append(new_task)
        
        # Save atomically
        success, save_msg = self.sync_save()
        if success:
            return True, "Task added successfully!"
        return False, save_msg

    def edit_task(
        self,
        task_id: str,
        title: str,
        module: str,
        due_date: str,
        priority: str,
        notes: str = ""
    ) -> tuple[bool, str]:
        """
        Updates properties of an existing task and commits to disk.
        """
        user = self.get_logged_in_user()
        if not user:
            return False, "Session expired. Please log in."

        # Run validation
        is_valid, err_msg = InputValidator.validate_task_inputs(
            title, module, due_date, priority, notes
        )
        if not is_valid:
            return False, err_msg

        # Find target task
        target_task = None
        for t in self.tasks_cache:
            if t.task_id == task_id and t.username == user:
                target_task = t
                break
                
        if not target_task:
            return False, "Task not found or access denied."

        # Update properties
        target_task.title = title.strip()
        target_task.module = module.strip()
        target_task.due_date = due_date.strip()
        target_task.priority = priority.strip()
        target_task.notes = notes.strip()

        # Save atomically
        success, save_msg = self.sync_save()
        if success:
            return True, "Task updated successfully!"
        return False, save_msg

    def delete_task(self, task_id: str) -> tuple[bool, str]:
        """
        Removes a task from in-memory cache and commits.
        """
        user = self.get_logged_in_user()
        if not user:
            return False, "Session expired."

        # Find task index
        target_index = -1
        for idx, t in enumerate(self.tasks_cache):
            if t.task_id == task_id and t.username == user:
                target_index = idx
                break
                
        if target_index == -1:
            return False, "Task not found."

        # Remove from list
        self.tasks_cache.pop(target_index)
        
        # Save atomically
        success, save_msg = self.sync_save()
        if success:
            return True, "Task deleted successfully."
        return False, save_msg

    def toggle_task_completion(self, task_id: str) -> tuple[bool, str]:
        """
        Toggles the completion status of a task.
        """
        user = self.get_logged_in_user()
        if not user:
            return False, "Session expired."

        # Find task
        target_task = None
        for t in self.tasks_cache:
            if t.task_id == task_id and t.username == user:
                target_task = t
                break
                
        if not target_task:
            return False, "Task not found."

        # Toggle status
        target_task.completed = not target_task.completed
        
        success, save_msg = self.sync_save()
        if success:
            return True, "Task status updated."
        return False, save_msg

    # --- Advanced Filter & Search Controllers ---

    def search_tasks(self, keyword: str, priority_filter: str = "All") -> list[Task]:
        """
        Performs responsive live filtering by matching keywords against 
        titles, modules, or notes, combined with priority filters.
        
        Args:
            keyword (str): The search phrase.
            priority_filter (str): 'All', 'High', 'Medium', or 'Low'.
            
        Returns:
            list[Task]: Matching tasks belonging to the active user.
        """
        user_tasks = self.get_user_tasks()
        keyword = keyword.strip().lower() if keyword else ""
        priority_filter = priority_filter.strip()
        
        filtered = []
        for t in user_tasks:
            # 1. Apply Priority Filter
            if priority_filter != "All" and t.priority != priority_filter:
                continue
                
            # 2. Apply Text Matching Filter
            if keyword:
                match_title = keyword in t.title.lower()
                match_module = keyword in t.module.lower()
                match_notes = keyword in t.notes.lower()
                if not (match_title or match_module or match_notes):
                    continue
                    
            filtered.append(t)
            
        return filtered

    def get_upcoming_tasks(self, hours_threshold: int = 48) -> list[Task]:
        """
        Identifies tasks that are uncompleted and due within the specified 
        hours threshold to display as alerts on the Dashboard.
        
        Args:
            hours_threshold (int): Maximum hours remaining (default 48).
            
        Returns:
            list[Task]: List of impending tasks.
        """
        user_tasks = self.get_user_tasks()
        now = datetime.now()
        limit_time = now + timedelta(hours=hours_threshold)
        
        upcoming = []
        for t in user_tasks:
            if t.completed:
                continue
            try:
                due_date = datetime.strptime(t.due_date, "%Y-%m-%d")
                # Treat task as due at end of the target day (23:59:59)
                due_datetime = due_date.replace(hour=23, minute=59, second=59)
                
                # Check if it falls inside the timeline window
                if now <= due_datetime <= limit_time:
                    upcoming.append(t)
            except ValueError:
                pass
                
        # Sort by urgency (earliest first)
        upcoming.sort(key=lambda t: t.due_date)
        return upcoming

    def get_dashboard_metrics(self) -> dict:
        """
        Computes progress metrics and urgency breakdowns.
        
        Returns:
            dict: Summary metrics containing count values.
        """
        user_tasks = self.get_user_tasks()
        total = len(user_tasks)
        completed = sum(1 for t in user_tasks if t.completed)
        pending = total - completed
        
        high_priority = sum(1 for t in user_tasks if t.priority == "High" and not t.completed)
        med_priority = sum(1 for t in user_tasks if t.priority == "Medium" and not t.completed)
        low_priority = sum(1 for t in user_tasks if t.priority == "Low" and not t.completed)
        
        # Calculate completion percentage
        ratio = int((completed / total) * 100) if total > 0 else 0
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "ratio": ratio,
            "high_priority_pending": high_priority,
            "medium_priority_pending": med_priority,
            "low_priority_pending": low_priority
        }

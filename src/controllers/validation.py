import re
from datetime import datetime

class InputValidator:
    """
    Controller Layer: Enforces strict data sanitization and validation 
    for academic task attributes, returning user-friendly error messages.
    """
    @staticmethod
    def validate_task_inputs(
        title: str,
        module: str,
        due_date_str: str,
        priority: str,
        notes: str = ""
    ) -> tuple[bool, str]:
        """
        Validates all inputs required to create or edit a task.
        
        Args:
            title (str): Title of the task.
            module (str): Module code/title.
            due_date_str (str): Target due date (expected 'YYYY-MM-DD').
            priority (str): Priority enum value ('High', 'Medium', 'Low').
            notes (str): Detailed text notes (optional).
            
        Returns:
            tuple[bool, str]: (Is Valid status, Error or success message)
        """
        # 1. Validate Title
        title = title.strip() if title else ""
        if not title:
            return False, "Task title is required and cannot be empty."
        if len(title) > 60:
            return False, "Task title cannot exceed 60 characters."

        # 2. Validate Module
        module = module.strip() if module else ""
        if not module:
            return False, "Academic module is required. Please select or enter one."
        if len(module) > 30:
            return False, "Module name/code cannot exceed 30 characters."

        # 3. Validate Due Date
        due_date_str = due_date_str.strip() if due_date_str else ""
        if not due_date_str:
            return False, "Due date is required."
            
        # Match YYYY-MM-DD pattern
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(date_pattern, due_date_str):
            return False, "Due date must be in YYYY-MM-DD format."
            
        try:
            due_date = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        except ValueError:
            return False, "Invalid calendar date. Please check the month and day."

        # Enforce that due date is not in the past (allow today)
        today = datetime.now().date()
        if due_date < today:
            return False, "Due date cannot be in the past."

        # 4. Validate Priority
        priority = priority.strip() if priority else ""
        if priority not in ["High", "Medium", "Low"]:
            return False, "Priority must be one of: High, Medium, Low."

        # 5. Validate Notes (length constraint to prevent buffer overflows)
        notes = notes.strip() if notes else ""
        if len(notes) > 500:
            return False, "Notes cannot exceed 500 characters."

        return True, "Inputs validated successfully."

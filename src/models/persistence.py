import json
import os
import shutil

class PersistenceService:
    """
    Model Layer: Handles robust local data storage with file backup recoveries 
    and transaction-safe atomic writes to prevent data corruption.
    """
    def __init__(self, filepath: str = "storage.json"):
        self.filepath = filepath
        self.backup_path = filepath + ".bak"
        self.temp_path = filepath + ".tmp"
        self._initialize_empty_store()

    def _initialize_empty_store(self) -> None:
        """Creates an empty structure if no storage exists."""
        if not os.path.exists(self.filepath):
            # If a backup exists, try to recover from it first
            if os.path.exists(self.backup_path):
                try:
                    shutil.copy2(self.backup_path, self.filepath)
                    return
                except IOError:
                    pass
            
            # Write initial empty state
            self.write_raw({"users": {}, "tasks": []})

    def write_raw(self, data: dict) -> bool:
        """
        Force-writes raw data directly (helper method).
        """
        try:
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            return True
        except IOError:
            return False

    def load_data(self) -> dict:
        """
        Loads the database structure. Recovers automatically from backups 
        if the primary file is corrupted.
        
        Returns:
            dict: The dictionary holding 'users' and 'tasks' lists.
        """
        try:
            if not os.path.exists(self.filepath):
                self._initialize_empty_store()

            with open(self.filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Verify basic structure integrity
            if "users" not in data or "tasks" not in data:
                raise ValueError("Corrupt file schema.")
                
            return data
            
        except (json.JSONDecodeError, ValueError, IOError) as e:
            # Save the corrupted file to '.corrupt' for safety and analysis
            if os.path.exists(self.filepath):
                try:
                    corrupt_path = self.filepath + ".corrupt"
                    if os.path.exists(corrupt_path):
                        os.remove(corrupt_path)
                    shutil.move(self.filepath, corrupt_path)
                except IOError:
                    pass

            # Corruption detected, try to restore from backup
            if os.path.exists(self.backup_path):
                try:
                    with open(self.backup_path, 'r', encoding='utf-8') as f_bak:
                        data_bak = json.load(f_bak)
                    if "users" in data_bak and "tasks" in data_bak:
                        # Restore backup as primary
                        shutil.copy2(self.backup_path, self.filepath)
                        return data_bak
                except (json.JSONDecodeError, IOError):
                    pass
            
            empty_state = {"users": {}, "tasks": []}
            self.write_raw(empty_state)
            return empty_state

    def save_data(self, users: dict, tasks_list: list[dict]) -> tuple[bool, str]:
        """
        Saves user credentials and task arrays securely using a 
        Transactional Atomic Write Pattern.
        
        Args:
            users (dict): Hashed credentials collection.
            tasks_list (list[dict]): Serialized task list.
            
        Returns:
            tuple[bool, str]: (Success status, feedback message)
        """
        payload = {
            "users": users,
            "tasks": tasks_list
        }
        
        try:
            # Step 1: Write serialized JSON to temporary file
            with open(self.temp_path, 'w', encoding='utf-8') as f_temp:
                json.dump(payload, f_temp, indent=4)
                f_temp.flush()
                os.fsync(f_temp.fileno())  # Force OS write buffer to hardware disk
            
            # Step 2: Create a backup of the current stable primary database
            if os.path.exists(self.filepath):
                shutil.copy2(self.filepath, self.backup_path)
            
            # Step 3: Atomic rename (Atomic on NTFS / Ext4 OS layers)
            if os.path.exists(self.filepath):
                os.replace(self.temp_path, self.filepath)
            else:
                os.rename(self.temp_path, self.filepath)
                
            return True, "Data persisted securely."
            
        except (IOError, OSError) as e:
            # Rollback: Clean up temporary file if write fails
            if os.path.exists(self.temp_path):
                try:
                    os.remove(self.temp_path)
                except OSError:
                    pass
            return False, f"Persistence error: {str(e)}"

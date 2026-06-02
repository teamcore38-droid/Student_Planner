import hashlib
import os

class AuthService:
    """
    Model Layer: Handles secure user authentication, registration, 
    credential hashing (SHA-256 with unique salting), and active session state.
    """
    def __init__(self):
        self.active_user = None

    def hash_password(self, password: str, salt: str) -> str:
        """
        Hashes a password using SHA-256 and a unique salt.
        
        Args:
            password (str): Raw password input.
            salt (str): Hex representation of a unique user salt.
            
        Returns:
            str: Hashed password string in hexadecimal.
        """
        salted = password.encode('utf-8') + bytes.fromhex(salt)
        return hashlib.sha256(salted).hexdigest()

    def register_user(self, users_db: dict, username: str, password: str) -> tuple[bool, str]:
        """
        Registers a new user in the credentials dictionary.
        
        Args:
            users_db (dict): The reference users dictionary from persistence.
            username (str): Target username.
            password (str): Target password (min 6 characters).
            
        Returns:
            tuple[bool, str]: (Success status, feedback message)
        """
        # Enforce basic validation
        username = username.strip()
        if not username:
            return False, "Username cannot be empty."
        if len(password) < 6:
            return False, "Password must be at least 6 characters long."
        
        # Check uniqueness
        if username.lower() in [u.lower() for u in users_db]:
            return False, "Username already exists."
        
        # Generate 16-byte random salt
        salt = os.urandom(16).hex()
        password_hash = self.hash_password(password, salt)
        
        # Save to reference database
        users_db[username] = {
            "password_hash": password_hash,
            "salt": salt
        }
        return True, "User registered successfully."

    def verify_login(self, users_db: dict, username: str, password: str) -> tuple[bool, str]:
        """
        Verifies login credentials and sets active user state upon success.
        
        Args:
            users_db (dict): The reference users dictionary.
            username (str): Entered username.
            password (str): Entered password.
            
        Returns:
            tuple[bool, str]: (Success status, feedback message)
        """
        username = username.strip()
        if not username or not password:
            return False, "Username and password are required."
        
        # Find exact user profile case-sensitively
        user_record = users_db.get(username)
        if not user_record:
            return False, "Invalid username or password."
        
        # Extract records
        salt = user_record.get("salt")
        stored_hash = user_record.get("password_hash")
        
        if not salt or not stored_hash:
            return False, "User record is corrupted."
            
        # Re-hash and compare
        computed_hash = self.hash_password(password, salt)
        if computed_hash == stored_hash:
            self.active_user = username
            return True, f"Welcome back, {username}!"
            
        return False, "Invalid username or password."

    def logout(self) -> None:
        """Clears the active session state."""
        self.active_user = None

    def get_active_user(self) -> str | None:
        """Returns the currently logged-in username, or None."""
        return self.active_user

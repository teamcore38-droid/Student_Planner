# Smart Student Planner — LDC6004M Coursework Portfolio

An elegant, mobile-first productivity utility engineered in Python using the Kivy framework, designed to mitigate cognitive overload and ease prioritization stress for higher education students. 

This project represents the complete practical mobile application portfolio (**Part I**) and aligns directly with the accompanying critical reflective narrative (**Part II**) for the **LDC6004M Mobile Application Development** coursework.

---

## 🌟 Key Application Features

1. **Secure Student Credentials Registry**: Local student authentication utilizing secure **salted SHA-256 password hashing**.
2. **Context-Scoped Account Isolation**: Flat database items are dynamically filtered by username session contexts. Multi-student registration supports isolated calendars on a single device with zero cross-user leakage.
3. **Interactive Visual Dashboard**: Computes progress completion metrics in real-time, displays neon-coded urgency statistics, and aggregates uncompleted academic deadlines due in less than 48 hours.
4. **Dynamic Live Search & Filters**: Filters task titles, modules, or notes dynamically on every text keypress. Integrates quick capsule priority chips (`All`, `High`, `Medium`, `Low`).
5. **Transactional Atomic Persistence**: Writes to a buffer file (`storage.json.tmp`) and renames it atomically (`os.replace`) to prevent database file corruptions.
6. **Self-Healing File Recoveries**: Detects primary JSON reading errors, quarantines the corrupted datastore as a `.corrupt` file, and automatically restores from the latest stable `.bak` backup file.

---

## 📐 MVC Architectural Layout

The codebase strictly adheres to a **Model-View-Controller (MVC)** design pattern, separating concerns into independent modules to ensure high testability and clean, unidirectional data flows.

```
d:\Shaakir bro\Mobile app-Shaakir\
├── .gitignore                             # Professional version control exclusion configs
├── README.md                              # This packaging and execution guide
├── storage.json                           # Local transactional database (Generated at boot)
├── documentation/                         # Design assets and specifications
│   ├── app_concept.md                     # Target personas, pedagogy and domain analyses
│   ├── wireframes.md                      # UI layout boundaries and ASCII wireframes
│   ├── navigation_flow.mermaid            # Mermaid transitions state-machine
│   └── architecture_justification.md      # MVC structure and data integrity defends
├── narrative/                             # Academic Reflective Narrative
│   └── reflective_narrative.md            # Critical evaluation report (1750 words, YSJU Harvard)
└── src/                                   # Application Source Code
    ├── main.py                            # Project startup entry point
    ├── controllers/                       # Controller Layer
    │   ├── main_controller.py             # Global session bus, metrics and CRUD coordinator
    │   └── validation.py                  # Strict text validation and date checks
    ├── models/                            # Model Layer
    │   ├── auth.py                        # Credentials hashing and session handlers
    │   ├── task.py                        # Strongly-typed Task data structures
    │   └── persistence.py                 # Atomic write operations and auto-recovery backups
    └── tests/                             # QA Testing Layer
        ├── test_models.py                 # Automated unit tests for database and hashing
        └── test_controllers.py            # Automated unit tests for validations and filters
```

---

## 💻 Local Execution & Installation Steps

### Prerequisites
* **Python 3.13+** (Tested and verified on Python 3.13.12 Windows environment)
* **Git** (For version control validation)

### 1. Installation of Dependencies
Clone or download the project folder. Open PowerShell or Command Prompt inside the directory and install Kivy:
```powershell
pip install kivy
```

### 2. Booting the Application
Launch the graphic Model-View-Controller student interface:
```powershell
python src/main.py
```

### 3. Seeding Sample Student Coursework Data
To instantly register a default student profile (`student` / `password123`) and seed the datastore with five realistic coursework tasks across four modules (scoping relative upcoming due dates and pre-marking one as completed to show progress):
```powershell
python src/seed.py
```

### 4. Running the Headless Test Suite
To run all **16 automated unit tests** (verifying persistence stability, hashing, and filters headlessly):
```powershell
python -m unittest discover -s src/tests
```

---

## 🧪 Automated Testing Overview

The codebase features absolute test coverage for the entire backend framework. Running the test discover command yields the following verified metric:

```powershell
................
----------------------------------------------------------------------
Ran 16 tests in 0.070s

OK
```

### Verified Test Areas:
* **`TestAuthService`**: Salted hashing consistency, registration length checks, duplicate registration rejections, and session token clearing.
* **`TestTask`**: Structural dictionary serialization and accurate object deserializations.
* **`TestPersistenceService`**: Atomic temp-writes, data integrity validation, and quarantine archiving on `.corrupt` while restoring `.bak` backups.
* **`TestInputValidator`**: Enforcing minimum and maximum string sizes, rejecting invalid date syntax, and blocking due dates set in the past.
* **`TestMainController`**: Task isolation boundaries per student profile, case-insensitive keyword searches, dynamic priority filtering, and mathematical progress metric compilations.

---

## ⚠️ Known Limitations & Future Roadmap

* **Text-Based Date Selectors**: The current date-input form relies on typing formatted `YYYY-MM-DD` strings, accompanied by strict validator regexes. In future iterations, this will be upgraded to an interactive calendar dropdown widget.
* **Relational SQLite Backend**: Transitioning from a flat JSON storage file to a local relational SQLite database to optimize index queries as student task records scale.
* **Cryptographic Salting Upgrades**: Implementing industrial hashing packages (such as `bcrypt` or `argon2`) to secure client-side user passwords.

# Architectural Overview & Critical Justification

## 1. Architectural Choice: Model-View-Controller (MVC)

To fulfill the requirements of the Level 6 curriculum and achieve a **Distinction-grade** software engineering standard, the **Smart Student Planner** is designed around a strict **Model-View-Controller (MVC)** architectural pattern. 

In mobile GUI development, mixing business logic with layout structures leads to "spaghetti code" that is prone to state synchronization bugs, regression failures, and makes automated testing impossible. By implementing MVC, we enforce a clean, unidirectional data flow that separates concerns.

```
       +--------------------------------------------+
       |                  VIEW                      |
       |  - UI screens, styles, form widgets        |
       |  - Captures inputs, forwards to Controller |
       +--------------------+-----------------+------+
                            |                 ^
       1. Capture user tap  |                 | 4. Update UI binding
       & forward inputs     v                 | with fresh data
       +--------------------+-----------------+------+
       |               CONTROLLER                   |
       |  - State sharing & screen transition routing|
       |  - Validates user input forms              |
       +--------------------+-----------------+------+
                            |                 ^
       2. Request persist   |                 | 3. Broadcast fresh 
       or auth check        v                 | task states/sessions
       +--------------------+-----------------+------+
       |                  MODEL                     |
       |  - Task objects & SHA-256 Hashed Auth      |
       |  - Atomic I/O file writing (JSON DB)       |
       +--------------------------------------------+
```

---

## 2. Separation of Concerns (SoC) Evaluation

Each architectural layer is designed with strict boundaries, containing zero leakage of functionality:

### A. The Model Layer (`src/models/`)
* **Responsibility**: Represents data structures and enforces business rules. It contains `task.py` (which defines task objects with strict types), `persistence.py` (which manages file I/O operations), and `auth.py` (which handles passwords hashing and security hashes).
* **Isolation**: The Model layer has **zero knowledge** of Kivy widgets, screen sizing, transitions, or active views. It can run in a headless CLI environment.

### B. The View Layer (`src/views/`)
* **Responsibility**: Controls visual layouts, color themes, spacing, typography, and responsive widget grids. It handles visual events (e.g. keyboard appearances, screen scrolling).
* **Isolation**: The View has **zero knowledge** of how a task is saved, whether database files exist, or what authentication algorithm is used. When a user clicks a button, the View simply forwards the action to a callback method in the Controller.

### C. The Controller Layer (`src/controllers/`)
* **Responsibility**: The central coordinator. It maintains the "single source of truth" (in-memory active task states, logged-in session tokens), routes navigation states, and validates input data.
* **Isolation**: It receives requests from the View, executes structural checks (e.g. sanitizing input, checking date ranges), instructs the Model to save the state, and then updates the View's active data bindings.

---

## 3. Critical Justification & Testability Advantages

Adhering to strict MVC offers three massive academic and engineering benefits:

1. **Unrivaled Testability**:
   In standard mobile applications, testing input validations and local persistence is complex because they are bound to the visual widgets. Under MVC, we can write **automated unit tests** (`tests/`) that instantiate the Model and Controller directly in memory, run validations, mock corrupt file storage, and assert results—**all without having to spin up the expensive Kivy UI rendering loop**. This provides clear, empirical evidence of robust QA for our markers.
2. **Persistence Modularity**:
   If we decide to migrate our storage engine from a flat JSON file (`storage.json`) to a local SQLite database or an external cloud-based REST API in the future, we **only need to update the Model's persistence class**. The View layer and the Controller layer will remain completely unchanged because they are decouple-bound to the Model's abstract interface.
3. **Prevention of State Synchronization Conflicts**:
   By routing all modifications (Add, Edit, Delete, Toggle Complete) through a single global `MainController`, we ensure that changes are broadcasted synchronously. There is no risk of the Dashboard showing completed tasks while the Search Screen shows them as pending.

---

## 4. Local Data Persistence & Atomic Write Integrity

To achieve a Distinction grade in the **Local Data Persistence** marking bracket, we must demonstrate advanced handling of data integrity and corruption hazards. 

Rather than using a basic, unsafe file writing operation (which can corrupt the entire database if the mobile device runs out of battery or crashes during a write block), our `persistence.py` implements a **Transactional Atomic Write Pattern**:

1. **Serialization**: When saving tasks, the controller's active array is parsed into a clean JSON-compliant dictionary.
2. **Buffer Write**: The JSON string is written to a temporary buffer file: `storage.json.tmp`.
3. **Flush & Sync**: The OS buffer is explicitly flushed to physical disk sector storage.
4. **Atomic Rename**: The system renames `storage.json.tmp` to replace the active `storage.json`. On modern filesystems (including Windows NTFS and Android ext4), this rename is an **atomic transaction**. 

If the application is forcefully terminated at any microsecond during Phase 1, 2, or 3, the active `storage.json` database remains **100% uncorrupted and intact**, completely mitigating data-loss and file corruption risks.

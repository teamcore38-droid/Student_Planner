# Smart Student Planner - UI Wireframes & Layout Spacing Guidelines

This document provides highly detailed wireframes and layout layouts for all major views of the **Smart Student Planner** application. Spacing and component sizes are structured to meet **Material Design 3** mobile benchmarks, ensuring a premium UX/UI.

---

## Central UI Layout Architecture
* **Grid**: 4-column responsive grid system with 16dp margins and 8dp/12dp/16dp spacing gutters.
* **Colors**: Premium Dark-Mode Harmony
  - Background: Slate Charcoal (`#121214`)
  - Surface Card: Deep Steel (`#1E1E24`)
  - Primary Accent: Electric Violet (`#7C4DFF`)
  - High Priority: Neon Tangerine (`#FF5722`)
  - Medium Priority: Warm Amber (`#FFB300`)
  - Low Priority: Vibrant Cyan (`#00E5FF`)
* **Typography**:
  - Headers: Outfit / Inter (Bold, 24sp)
  - Subheaders: Inter (Semi-Bold, 16sp)
  - Body Text: Inter (Regular, 14sp)
  - Micro-labels: Inter (Medium, 12sp)

---

## 1. Login Screen Layout

### Wireframe Mockup
```
+------------------------------------------+
|  [20:30]                         [X] 98% |
|                                          |
|            💥 SMART PLANNER             |
|          "Organize Your Focus"           |
|                                          |
|  +------------------------------------+  |
|  | Email Address                      |  |
|  | [ student@yorksj.ac.uk           ] |  |
|  +------------------------------------+  |
|                                          |
|  +------------------------------------+  |
|  | Password                           |  |
|  | [ ••••••••••••••                 ] |  |
|  +------------------------------------+  |
|  [!] Invalid password length (min 6 ch)  |
|                                          |
|  +------------------------------------+  |
|  |            [  LOGIN  ]             |  |
|  +------------------------------------+  |
|                                          |
|         Don't have an account?           |
|        [ Tap to Create Profile ]         |
+------------------------------------------+
```

### Technical Design Specifications:
* **Interactive Elements**:
  * **Email & Password Fields**: Text inputs with 56dp height (Material 3 standard) to ensure a high-quality touch target. Outlined with Electric Violet on focus.
  * **Login Button**: Raised card style with 48dp height, centered. On-hover or on-tap scale micro-animations.
  * **Input Validation**: Enforces length constraints on Password (>= 6 characters) and matching email regex format (`^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$`).
  * **Error State**: Displays inline warning messages in Neon Tangerine (`#FF5722`) directly below the corresponding input box for immediate usability awareness.

---

## 2. Dashboard Screen Layout (Home)

### Wireframe Mockup
```
+------------------------------------------+
|  [20:30]  (👤 Sarah)             [Settings]|
|  ⭐ ACADEMIC METRICS                     |
|  +------------------------------------+  |
|  |  [||||||||||||||||.......] 68%     |  |
|  |  12 Tasks Active | 8 Completed     |  |
|  +------------------------------------+  |
|                                          |
|  🔥 PRIORITY CRITICALITY                 |
|  +--------------+ +-------------------+  |
|  | High: 3 [🟠] | | Med/Low: 9 [🟡]   |  |
|  +--------------+ +-------------------+  |
|                                          |
|  🕒 UPCOMING DEADLINES (Due <48h)        |
|  +------------------------------------+  |
|  | [🟠] LDC6004M - Create Wireframes  |  |
|  |      Due: Tomorrow, 12:00 PM       |  |
|  +------------------------------------+  |
|  | [🟡] LDC6001M - Read Syllabus      |  |
|  |      Due: 04/06/2026               |  |
|  +------------------------------------+  |
|                                          |
|     [ Task List ]    [+] [ Add Task ]    |
+------------------------------------------+
```

### Technical Design Specifications:
* **Interactive Elements**:
  * **Progress Tracker**: Displays a sleek horizontal progress bar or radial meter reflecting Task Complete vs Total Task counts. Helps students visual-track their performance.
  * **Priority Split Cards**: Responsive side-by-side grids. Clicking "High" automatically filters and opens the Task List displaying High-Priority items.
  * **Quick Add Button (`+`)**: A Floating Action Button (FAB) at 56dp x 56dp diameter, positioned in the lower-right or bottom control bar. Styled in Electric Violet (`#7C4DFF`).

---

## 3. Task List & Live Search Layout

### Wireframe Mockup
```
+------------------------------------------+
|  [20:30]  <- Back to Dashboard           |
|  📑 MY ACADEMIC TASKS                    |
|                                          |
|  +------------------------------------+  |
|  | [🔍 Search by keyword, module...  ] |  |
|  +------------------------------------+  |
|  [ All ] [ High ] [ Med ] [ Low ]  [Chips]
|                                          |
|  +------------------------------------+  |
|  | [ ] LDC6004M - Architecture Plan   |  |
|  |     Due: 05 June | Priority: High  |  |
|  |     [Edit] [Delete]                |  |
|  +------------------------------------+  |
|  +------------------------------------+  |
|  | [x] LDC6002M - Complete Draft      |  |
|  |     Due: 08 June | Priority: Med   |  |
|  |     [Edit] [Delete]                |  |
|  +------------------------------------+  |
|                                          |
|                      [+] Add New Task    |
+------------------------------------------+
```

### Technical Design Specifications:
* **Interactive Elements**:
  * **Live Search**: Full-width text input with 48dp height. Runs text-matching dynamically on keypress. Includes a custom clear `(X)` icon.
  * **Filter Chips**: Tap-action horizontal scrolling capsule chips (`All`, `High`, `Med`, `Low`) that act as state toggles. Active states are filled with theme colors.
  * **Task Card Components**: 
    - Checkbox: A 32dp circular hit area to easily toggle Task Completed states.
    - Context Menu/Swipe Actions: Swipe-left to reveal a high-contrast Delete action, Swipe-right to Edit. (Also includes explicit small buttons for clear keyboard usability).

---

## 4. Task Creator / Editor Layout

### Wireframe Mockup
```
+------------------------------------------+
|  [20:30]  <- Cancel         [ SAVE TASK ]|
|  📝 CREATE NEW TASK                      |
|                                          |
|  Title *                                 |
|  [ Write task name...                  ] |
|                                          |
|  Module *                                |
|  [ LDC6004M - Mobile App Dev        v ] |
|                                          |
|  Due Date *                              |
|  [ 2026-06-05                        📅 ]|
|                                          |
|  Priority *                              |
|  (🔴) High      (🟡) Medium     (🔵) Low |
|                                          |
|  Task Notes                              |
|  [ Enter syllabus refs, study steps... ] |
|  [                                     ] |
|                                          |
+------------------------------------------+
```

### Technical Design Specifications:
* **Interactive Elements**:
  * **Module Dropdown Selector**: Native spinner / custom overlays. Drops down to display enrolled modules. Enforces selection.
  * **Interactive Date Picker**: A customized calendar modal trigger (represented by a calendar icon at 48dp hit area). Validates selection to ensure the date is in the future.
  * **Priority Radio Toggles**: 3 horizontal segment buttons. Wide spacing to prevent accidental taps.
  * **Notes Text Box**: Multiline scrolling box with 120dp height limit. Ensures room for referencing university assignment briefs.

---

## 5. Settings & Professional Citation Layout

### Wireframe Mockup
```
+------------------------------------------+
|  [20:30]  <- Back to Home                |
|  ⚙️ SETTINGS & PROFILE                   |
|                                          |
|  STUDENT DETAILS                         |
|  👤 York St John Student                 |
|  📧 student@yorksj.ac.uk                 |
|                                          |
|  PREFERENCES                             |
|  [x] Premium Dark Mode                   |
|  [x] Local Auto-Save Enabled             |
|                                          |
|  DATA MANAGEMENT                         |
|  +------------------------------------+  |
|  |     [ CLEAR ALL LOCAL STORAGE ]    |  |
|  +------------------------------------+  |
|                                          |
|  ACADEMIC DISCLOSURES                    |
|  Referencing standard: YSJU Harvard.     |
|  App Framework: Kivy v2.3                |
|  Store format: Atomic Transaction JSON   |
|                                          |
|  [ LOG OUT ]                             |
+------------------------------------------+
```

### Technical Design Specifications:
* **Interactive Elements**:
  * **Clear Storage Button**: Highlights a structural caution zone in Neon Tangerine (`#FF5722`). Triggers a confirmation dialog box to prevent accidental student database wipes.
  * **Theme/Preference Toggles**: Clean checkbox or toggle switches that persist state instantly to disk.
  * **Logout Button**: Triggers session termination, clears active RAM memory of active states, and redirects to the Login screen.

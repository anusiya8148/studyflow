# StudyFlow 🎓 - Premium Full-Stack Student Productivity SaaS Application

StudyFlow is an AI-inspired, ultra-modern full-stack student productivity workspace built with a high-fidelity SaaS aesthetic. It features a deep-navy sidebar, vibrant purple active states, minimalist metric cards, glassmorphic UI elements, and drop-shadow styling replicated from the reference dashboard layout design.

---

## 🚀 Key Feature Matrix

* **Central Workspace Dashboard:** Displays real-time summary statistics (`Total Notes`, `Active Tasks`, `Completed Logs`, and `Productivity Metrics`), along with a dynamic **Chart.js** doughnut chart visualization, interactive recent note snippets, and automated journal log tracking components.
* **Persistent Text Notes Repository:** A clean, card-based interface with fully parameterized search routing, dynamic modal creation grids, modification drawers, and instant deletion nodes.
* **High-Fidelity Task Matrix Engine:** Organizes milestones with distinct priority indicator tags (`High`, `Medium`, `Low`), interactive checkbox status triggers (`Pending`/`Completed`), and custom target deadlines.
* **Daily Reflective Journal Logs:** Connects your daily schedule with automated mental-state tracking using customizable mood vector selectors.
* **Voice Processing Studio:** Captures hardware mic input line data inside the browser using the native **HTML5 MediaRecorder API**, and uploads chunks to local storage asynchronously via AJAX file streams.
* **Perspective Motivation Module:** A glassmorphism-themed quote generator that pulls structured strings asynchronously from an internal endpoint (`/api/quote`) without needing a page refresh.
* **Secure Multi-User Auth Gateway:** Includes account registration and session validation layers built with salted cryptography (`werkzeug.security.scrypt`).

---

## 📁 System Architecture Directory

```text
studyflow/
│
├── app.py                # Core Python Flask Backend (Data Orchestration & Endpoints)
├── database.db           # Persistent SQLite3 Embedded Relational Storage Target
│
├── templates/            # Jinja2 Dynamic View Layer
│   ├── base.html         # Global View Scaffold (Navigation Frame & Core Header Sets)
│   ├── login.html        # Authentication Secure Portal Node
│   ├── register.html     # Secure Registration Form Profile Provisioning 
│   ├── dashboard.html    # Core Analytical Performance Hub & Live Charts
│   ├── notes.html        # Grid-Based Note Stack Repository
│   ├── tasks.html        # Priority Matrix Milestone Control Table
│   ├── journal.html      # Daily Mental State Logging Matrix
│   ├── voice.html        # Voice Note Audio Processing Canvas
│   ├── motivation.html   # Glassmorphic Random Quote Rotator
│   └── logout.html       # Session Termination Lifecycle Control
│
└── static/               # Client Asset Deliverables
    ├── css/
    │   └── style.css     # Premium Layout Theme Rulesheet (Variables, Responsive Queries)
    └── js/
        └── script.js     # Client Interactions & Media Stream Controllers
🛠️ Environmental Setup & Execution Guide
1. Project Folder Allocation
Ensure all system files are stored accurately within your local target workspace folder tree (e.g., studyFlow_app).

2. Dependency Resolution
Launch your system terminal window, navigate into your root installation workspace block, and execute the package installation line:

Bash
pip install flask werkzeug
(SQLite3, OS, Random, and Datetime are native dependencies within the standard Python Core installation package.)

3. Initialize Server Pipelines
Boot your server routing architecture natively from the root directory path:

Bash
python app.py
Upon successful execution, the terminal display pipeline will output:

Plaintext
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on [http://127.0.0.1:5000](http://127.0.0.1:5000)
4. Client Access Setup
Open your web browser and navigate directly to the following address:

Plaintext
[http://127.0.0.1:5000](http://127.0.0.1:5000)
The application state tracking manager will securely catch your session token and redirect you directly to the Login and Authentication Engine. Simply click Create cloud profile, register a user account, and log in to explore your new StudyFlow environment!

📊 Database Architecture Schema Layout
The platform uses an embedded relational SQL architecture that automatically maps out five synchronized, persistent table arrays on first boot:

users Table: Stores identity names, verified email targets, and scrypt-hashed access strings.

notes Table: Holds text titles, context content, and user ownership keys linked to user accounts.

tasks Table: Tracks task descriptions, deadlines, priority parameters, and status markers (Pending/Completed).

journals Table: Logs historical reflection texts along with selected mood symbols.

voice_notes Table: Stores specific file names (.webm) and audio metadata records.

📱 Adaptive Cross-Device Responsiveness
The presentation layer uses adaptive CSS Grid architectures and media matching triggers. When screen sizes drop below 768px (such as tablets or mobile phone screens):

The primary left navigation pane automatically transitions off-canvas into an overlay drawer.

A hamburger menu icon becomes active in the top navbar area to let users easily toggle the sidebar view.

Data cards and metrics collapse seamlessly from four columns down to single-stack structures, keeping readability clear across all device viewport shapes.

Author
Anusiya R
2 Year cse

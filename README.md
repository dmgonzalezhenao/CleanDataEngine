# 📂 CleanData Engine v1.1  

**CleanData Engine** is a high-performance automation tool built with Python, designed for bulk cleaning and validation of CSV datasets. The system streamlines data workflows by validating emails via Regex and **managing data persistence through a professional SQL architecture.**

---

## 🚀 Key Features

* **SQL Persistence (SQLite3):** Automatically stores clean emails, discarded records (with error reasons), and an audit log for every processed file.
* **Idempotency & State Control:** The engine recognizes completed or interrupted tasks, preventing data duplication and optimizing execution time.
* **Regex Validation:** Advanced filtering logic to ensure legitimate email formats.
* **Real-time Audit Reports:** Interactive CLI menu to query processing history directly from the database.
* **Live Progress Monitoring:** Visual feedback using `█` blocks to track processing status for massive datasets.

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white)
![RegEx](https://img.shields.io/badge/RegEx-42a5f5?style=for-the-badge&logo=regex&logoColor=white)

## 📦 Project Structure

```plaintext
CleanDataEngine/  
├── input/             # Source CSV files to be processed
├── output/            # Resulting cleaned CSV files
├── main.py            # Main Orchestrator & CLI Menu
├── cleaner.py         # Cleaning logic & Regex validation
├── database_manager.py # SQL Table management & Queries
├── clean_data.db      # Local Database (Auto-generated)
├── .gitignore         # Sensitive data protection
└── README.md          # Project documentation
```

## 🔧 How to Use  

Clone the repository: git clone https://github.com/your-username/CleanDataEngine.git

Prepare your data: Place your .csv files inside the /input folder.

Run the system: python main.py

Interactive Menu:

Press 1 to process new files.

Press 2 to view the processing report from the DB.

📈 SQL Report Example (Option 2)

======================================================================
FILE NAME                 ║ ROWS     ║ STATUS          ║ TIMESTAMP
──────────────────────────────────────────────────────────────────────
march_leads.csv           ║ 5000     ║ ✅ DONE         ║ 2026-01-13
test_data_error.csv       ║ 402      ║ ❌ ERROR LINE 403║ 2026-01-13
======================================================================

## 🛡️ Security & Best Practices
Memory Efficiency: Processing is done line-by-line to prevent high RAM consumption on large files.

Data Integrity: The software never modifies the original source; it always generates a clean copy.

Path Safety: Uses pathlib for robust cross-platform file management.

## 🛠️ Future Roadmap (AI DevOps Specialization)
[ ] Containerization (Docker): Create a lightweight image for instant deployment.

[ ] FastAPI Integration: Convert the engine into a REST API for cloud-based services.

[ ] Vector DB & AI: Implement similarity analysis using embeddings for string deduplication.

### 👤 Author
Developed with dedication by Daniel Mitchell González Henao.

LinkedIn: linkedin.com/in/daniel-gonzález-551b22305

Email: dmgh20212022@gmail.com

This project was created as part of a Backend Development learning path, applying CS50 principles and advanced Python logic.

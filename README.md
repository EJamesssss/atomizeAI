# AtomizeAI

## Project Structure

```text
atomizeAI/
├── .venv/                  # Local Python virtual environment; do not commit to GitHub
├── app.py                  # Main Streamlit entry point and homepage
├── pages/                  # Streamlit pages/screens shown in the sidebar
│   └── _View_Results.py   # Page for displaying processed data, summaries, or reports
│
├── services/               # Main app logic such as AI calls, file handling, and reports
│   └── report_service.py   # Handles report generation and data summaries
│
├── utils/                  # Small reusable helper functions used across the app
│   └── text_utils.py       # Text cleaning, formatting, and validation helpers
│
├── data/                   # Sample or test data files only; avoid confidential data
│   └── sample_data.csv     # Example sample data for testing the app
│
├── requirements.txt        # List of Python packages needed to run the project
├── .gitignore              # Files and folders that Git should ignore
└── README.md               # Project guide, setup steps, and developer instructions
```

## Initial Project Setup

Follow these steps to create a virtual environment, activate it, install
dependencies, and update `requirements.txt`.

---

### 1. Create a virtual environment

Run this command inside the project folder:

```bash
cd atomizeAI
python -m venv .venv
```

### 2. Activate the virtual environment

#### For macOS/Linux:

```bash
source .venv/bin/activate
```

#### For Windows Command Prompt:

```bash
.venv\Scripts\activate
```

#### For Windows PowerShell:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Streamlit app

```bash
streamlit run app.py
```

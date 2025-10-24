# Web-app Backend

A minimal Flask backend that scrapes Premier League data and stores it in a SQL database.

Environment
- WEBAPP_DB_CONN: SQLAlchemy connection string. Example for local sqlite: sqlite:///data.db
- FOOTBALL_DATA_TOKEN: (optional) token for football-data.org API

Run locally

1. Create a venv and install requirements

   python -m venv .venv
   .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt

2. Run the app

   $env:WEBAPP_DB_CONN='sqlite:///data.db'; python app.py

Notes
- For production on Azure, provide a proper SQL Server connection string and secure secrets via Key Vault or App Settings.

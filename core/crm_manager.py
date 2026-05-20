import sqlite3
import pandas as pd
from datetime import datetime

class CRMManager:
    def __init__(self, db_path="data/leads_crm.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS leads (email TEXT PRIMARY KEY, name TEXT, company TEXT, status TEXT, last_contact DATE, strategy_id TEXT)")

    def add_leads(self, leads):
        with sqlite3.connect(self.db_path) as conn:
            for lead in leads:
                conn.execute("INSERT OR IGNORE INTO leads (email, name, company, status) VALUES (?, ?, ?, ?)",
                             (lead["email"], lead["name"], lead["company"], "HUNTED"))

    def update_status(self, email, status):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("UPDATE leads SET status = ?, last_contact = ? WHERE email = ?", 
                         (status, datetime.now().date(), email))

    def get_stats(self):
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql_query("SELECT status, count(*) as count FROM leads GROUP BY status", conn)
            return df.to_dict()

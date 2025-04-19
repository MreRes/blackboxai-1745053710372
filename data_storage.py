import sqlite3
from sqlite3 import Error
from logger_config import setup_logger

logger = setup_logger()

class DataStorage:
    def __init__(self, db_file='financial_data.db'):
        self.db_file = db_file
        self.conn = None
        self.connect()
        self.create_tables()

    def connect(self):
        try:
            # Allow SQLite connection to be shared across threads
            self.conn = sqlite3.connect(self.db_file, check_same_thread=False)
            logger.info(f"Connected to database {self.db_file}")
        except Error as e:
            logger.error(f"Error connecting to database: {e}")

    def create_tables(self):
        try:
            cursor = self.conn.cursor()
            # Drop old income and outcome tables (deprecated)
            cursor.execute('DROP TABLE IF EXISTS income')
            cursor.execute('DROP TABLE IF EXISTS outcome')

            # Create transactions table to replace income/outcome
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    type TEXT CHECK(type IN ('income', 'outcome')) NOT NULL,
                    amount REAL NOT NULL,
                    description TEXT,
                    sender_phone TEXT,
                    date TEXT DEFAULT (datetime('now','localtime'))
                )
            ''')
            # Create contacts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone_number TEXT UNIQUE NOT NULL,
                    display_name TEXT
                )
            ''')

            # Create budgets table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS budgets (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    category TEXT NOT NULL,
                    amount REAL NOT NULL,
                    period TEXT NOT NULL, -- e.g. 'monthly', 'weekly'
                    start_date TEXT,
                    end_date TEXT
                )
            ''')

            # Create goals table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS goals (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    target_amount REAL NOT NULL,
                    current_amount REAL DEFAULT 0,
                    deadline TEXT
                )
            ''')

            self.conn.commit()
            logger.info("Database tables created or verified.")
        except Error as e:
            logger.error(f"Error creating tables: {e}")

    def add_transaction(self, type_: str, amount: float, description: str = '', sender_phone: str = None, date: str = None):
        try:
            cursor = self.conn.cursor()
            if date:
                cursor.execute('INSERT INTO transactions (type, amount, description, sender_phone, date) VALUES (?, ?, ?, ?, ?)',
                               (type_, amount, description, sender_phone, date))
            else:
                cursor.execute('INSERT INTO transactions (type, amount, description, sender_phone) VALUES (?, ?, ?, ?)',
                               (type_, amount, description, sender_phone))
            self.conn.commit()
            logger.info(f"Transaction added: {type_}, {amount}, {description}, {sender_phone}, {date}")
        except Error as e:
            logger.error(f"Error adding transaction: {e}")

    def get_report(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='income'")
            total_income = cursor.fetchone()[0] or 0
            cursor.execute("SELECT SUM(amount) FROM transactions WHERE type='outcome'")
            total_outcome = cursor.fetchone()[0] or 0
            balance = total_income - total_outcome
            logger.info(f"Report generated: Income={total_income}, Outcome={total_outcome}, Balance={balance}")
            return {
                'total_income': total_income,
                'total_outcome': total_outcome,
                'balance': balance
            }
        except Error as e:
            logger.error(f"Error generating report: {e}")
            return None

    def get_transactions(self, start_date: str = None, end_date: str = None, type_: str = None):
        try:
            cursor = self.conn.cursor()
            query = "SELECT t.id, t.type, t.amount, t.description, t.date, t.sender_phone, c.display_name FROM transactions t LEFT JOIN contacts c ON t.sender_phone = c.phone_number WHERE 1=1"
            params = []
            if start_date:
                query += " AND t.date >= ?"
                params.append(start_date)
            if end_date:
                query += " AND t.date <= ?"
                params.append(end_date)
            if type_:
                query += " AND t.type = ?"
                params.append(type_)
            query += " ORDER BY t.date DESC"
            cursor.execute(query, params)
            rows = cursor.fetchall()
            transactions = []
            for row in rows:
                transactions.append({
                    'id': row[0],
                    'type': row[1],
                    'amount': row[2],
                    'description': row[3],
                    'date': row[4],
                    'sender_phone': row[5],
                    'display_name': row[6]
                })
            logger.info(f"Fetched {len(transactions)} transactions")
            return transactions
        except Error as e:
            logger.error(f"Error fetching transactions: {e}")
            return []

    def add_budget(self, category: str, amount: float, period: str, start_date: str = None, end_date: str = None):
        try:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO budgets (category, amount, period, start_date, end_date) VALUES (?, ?, ?, ?, ?)',
                           (category, amount, period, start_date, end_date))
            self.conn.commit()
            logger.info(f"Budget added: {category}, {amount}, {period}")
        except Error as e:
            logger.error(f"Error adding budget: {e}")

    def get_budgets(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, category, amount, period, start_date, end_date FROM budgets')
            rows = cursor.fetchall()
            budgets = []
            for row in rows:
                budgets.append({
                    'id': row[0],
                    'category': row[1],
                    'amount': row[2],
                    'period': row[3],
                    'start_date': row[4],
                    'end_date': row[5]
                })
            logger.info(f"Fetched {len(budgets)} budgets")
            return budgets
        except Error as e:
            logger.error(f"Error fetching budgets: {e}")
            return []

    def add_contact(self, phone_number: str, display_name: str = None):
        try:
            cursor = self.conn.cursor()
            cursor.execute('INSERT OR IGNORE INTO contacts (phone_number, display_name) VALUES (?, ?)', (phone_number, display_name))
            self.conn.commit()
            logger.info(f"Contact added: {phone_number} -> {display_name}")
        except Error as e:
            logger.error(f"Error adding contact: {e}")

    def update_contact_name(self, phone_number: str, display_name: str):
        try:
            cursor = self.conn.cursor()
            cursor.execute('UPDATE contacts SET display_name = ? WHERE phone_number = ?', (display_name, phone_number))
            self.conn.commit()
            logger.info(f"Contact updated: {phone_number} -> {display_name}")
        except Error as e:
            logger.error(f"Error updating contact: {e}")

    def get_contacts(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT phone_number, display_name FROM contacts')
            rows = cursor.fetchall()
            contacts = []
            for row in rows:
                contacts.append({
                    'phone_number': row[0],
                    'display_name': row[1]
                })
            logger.info(f"Fetched {len(contacts)} contacts")
            return contacts
        except Error as e:
            logger.error(f"Error fetching contacts: {e}")
            return []

    def add_goal(self, name: str, target_amount: float, deadline: str = None):
        try:
            cursor = self.conn.cursor()
            cursor.execute('INSERT INTO goals (name, target_amount, deadline) VALUES (?, ?, ?)',
                           (name, target_amount, deadline))
            self.conn.commit()
            logger.info(f"Goal added: {name}, {target_amount}, {deadline}")
        except Error as e:
            logger.error(f"Error adding goal: {e}")

    def update_goal_progress(self, goal_id: int, current_amount: float):
        try:
            cursor = self.conn.cursor()
            cursor.execute('UPDATE goals SET current_amount = ? WHERE id = ?', (current_amount, goal_id))
            self.conn.commit()
            logger.info(f"Goal {goal_id} progress updated to {current_amount}")
        except Error as e:
            logger.error(f"Error updating goal progress: {e}")

    def get_goals(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute('SELECT id, name, target_amount, current_amount, deadline FROM goals')
            rows = cursor.fetchall()
            goals = []
            for row in rows:
                goals.append({
                    'id': row[0],
                    'name': row[1],
                    'target_amount': row[2],
                    'current_amount': row[3],
                    'deadline': row[4]
                })
            logger.info(f"Fetched {len(goals)} goals")
            return goals
        except Error as e:
            logger.error(f"Error fetching goals: {e}")
            return []

    def get_daily_report(self, date: str):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT type, SUM(amount) FROM transactions
                WHERE date(date) = date(?)
                GROUP BY type
            ''', (date,))
            rows = cursor.fetchall()
            report = {'income': 0, 'outcome': 0}
            for row in rows:
                report[row[0]] = row[1]
            report['balance'] = report.get('income', 0) - report.get('outcome', 0)
            logger.info(f"Daily report for {date}: {report}")
            return report
        except Error as e:
            logger.error(f"Error generating daily report: {e}")
            return None

    def get_monthly_report(self, year_month: str):
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT type, SUM(amount) FROM transactions
                WHERE strftime('%Y-%m', date) = ?
                GROUP BY type
            ''', (year_month,))
            rows = cursor.fetchall()
            report = {'income': 0, 'outcome': 0}
            for row in rows:
                report[row[0]] = row[1]
            report['balance'] = report.get('income', 0) - report.get('outcome', 0)
            logger.info(f"Monthly report for {year_month}: {report}")
            return report
        except Error as e:
            logger.error(f"Error generating monthly report: {e}")
            return None

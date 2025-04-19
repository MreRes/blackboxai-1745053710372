from flask import Flask, jsonify, render_template_string, request, redirect, url_for, session
from data_storage import DataStorage
from logger_config import setup_logger
import os

logger = setup_logger()

app = Flask(__name__)
app.secret_key = os.urandom(24)
data_storage = DataStorage()

# Custom Jinja filter to format numbers with thousands separator
@app.template_filter('format_number')
def format_number_filter(value):
    try:
        return "{:,}".format(int(value))
    except (ValueError, TypeError):
        return value

# Simple user credentials for demonstration
USERS = {
    "admin": "password123"
}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username in USERS and USERS[username] == password:
            session['username'] = username
            logger.info(f"User {username} logged in.")
            return redirect(url_for('home'))
        else:
            return render_template_string(LOGIN_HTML, error="Invalid credentials")
    return render_template_string(LOGIN_HTML)

@app.route('/logout')
def logout():
    username = session.pop('username', None)
    logger.info(f"User {username} logged out.")
    return redirect(url_for('login'))

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    report = data_storage.get_report()
    if report is None:
        return "Error generating report", 500
    recent_transactions = data_storage.get_transactions()
    return render_template('dashboard.html',
                           total_income=report['total_income'],
                           total_outcome=report['total_outcome'],
                           balance=report['balance'],
                           recent_transactions=recent_transactions)

@app.route('/api/report')
@login_required
def api_report():
    report = data_storage.get_report()
    if report is None:
        return jsonify({'error': 'Error generating report'}), 500
    logger.info("Serving financial report API.")
    return jsonify(report)

@app.route('/transactions')
@login_required
def transactions():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    type_ = request.args.get('type')
    transactions = data_storage.get_transactions(start_date, end_date, type_)
    return render_template('transactions.html', transactions=transactions)

@app.route('/budgets', methods=['GET', 'POST'])
@login_required
def budgets():
    if request.method == 'POST':
        category = request.form.get('category')
        amount = request.form.get('amount')
        period = request.form.get('period')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        try:
            amount = float(amount)
            data_storage.add_budget(category, amount, period, start_date, end_date)
            return redirect(url_for('budgets'))
        except Exception as e:
            logger.error(f"Error processing budget form: {e}")

    budgets = data_storage.get_budgets()
    return render_template('budgets.html', budgets=budgets)

@app.route('/goals', methods=['GET', 'POST'])
@login_required
def goals():
    if request.method == 'POST':
        name = request.form.get('name')
        target_amount = request.form.get('target_amount')
        deadline = request.form.get('deadline')
        try:
            target_amount = float(target_amount)
            data_storage.add_goal(name, target_amount, deadline)
            return redirect(url_for('goals'))
        except Exception as e:
            logger.error(f"Error processing goal form: {e}")

    goals = data_storage.get_goals()
    return render_template('goals.html', goals=goals)

LOGIN_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Login</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet" />
    <style>
        body { font-family: 'Inter', sans-serif; }
    </style>
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center p-4">
    <div class="bg-white rounded-lg shadow-lg p-8 max-w-md w-full">
        <h1 class="text-2xl font-bold mb-6 text-center">Login</h1>
        {% if error %}
        <p class="text-red-600 mb-4 text-center">{{ error }}</p>
        {% endif %}
        <form method="post" class="space-y-4">
            <div>
                <label for="username" class="block font-semibold mb-1">Username</label>
                <input type="text" id="username" name="username" required class="w-full border border-gray-300 rounded px-3 py-2" />
            </div>
            <div>
                <label for="password" class="block font-semibold mb-1">Password</label>
                <input type="password" id="password" name="password" required class="w-full border border-gray-300 rounded px-3 py-2" />
            </div>
            <button type="submit" class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition">Login</button>
        </form>
    </div>
</body>
</html>
"""

from flask import render_template, request

@app.route('/reports')
@login_required
def reports():
    daily_date = request.args.get('daily_date')
    monthly_date = request.args.get('monthly_date')
    from datetime import datetime
    if not daily_date:
        daily_date = datetime.now().strftime('%Y-%m-%d')
    if not monthly_date:
        monthly_date = datetime.now().strftime('%Y-%m')
    daily_report = data_storage.get_daily_report(daily_date)
    monthly_report = data_storage.get_monthly_report(monthly_date)
    if daily_report is None or monthly_report is None:
        return "Error generating reports", 500
    return render_template('reports.html',
                           daily_report=daily_report,
                           monthly_report=monthly_report,
                           daily_date=daily_date,
                           monthly_date=monthly_date)

@app.route('/contacts', methods=['GET', 'POST'])
@login_required
def contacts():
    if request.method == 'POST':
        phone_number = request.form.get('phone_number')
        display_name = request.form.get('display_name')
        if phone_number:
            existing_contacts = data_storage.get_contacts()
            existing_phones = [c['phone_number'] for c in existing_contacts]
            if phone_number in existing_phones:
                data_storage.update_contact_name(phone_number, display_name)
            else:
                data_storage.add_contact(phone_number, display_name)
        return redirect(url_for('contacts'))
    contacts = data_storage.get_contacts()
    return render_template('contacts.html', contacts=contacts)

if __name__ == '__main__':
    app.run(debug=True)

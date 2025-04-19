from flask import Flask, render_template_string, request, redirect, url_for, session
from data_storage import DataStorage
from logger_config import setup_logger
import os

logger = setup_logger()
app = Flask(__name__)
app.secret_key = os.urandom(24)
data_storage = DataStorage()

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/reports/daily')
@login_required
def daily_report():
    date = request.args.get('date')
    if not date:
        from datetime import datetime
        date = datetime.now().strftime('%Y-%m-%d')
    report = data_storage.get_daily_report(date)
    if report is None:
        return "Error generating daily report", 500
    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Daily Report</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet" />
        <style>body {{ font-family: 'Inter', sans-serif; }}</style>
    </head>
    <body class="bg-gray-100 min-h-screen flex flex-col items-center p-4">
        <nav class="bg-white shadow w-full max-w-4xl rounded mb-6 p-4 flex justify-between items-center">
            <div class="space-x-4">
                <a href="{{ url_for('home') }}" class="text-blue-600 hover:underline font-semibold">Home</a>
                <a href="{{ url_for('transactions') }}" class="text-blue-600 hover:underline font-semibold">Transactions</a>
                <a href="{{ url_for('budgets') }}" class="text-blue-600 hover:underline font-semibold">Budgets</a>
                <a href="{{ url_for('goals') }}" class="text-blue-600 hover:underline font-semibold">Goals</a>
                <a href="{{ url_for('daily_report') }}" class="text-blue-600 hover:underline font-semibold">Daily Report</a>
                <a href="{{ url_for('monthly_report') }}" class="text-blue-600 hover:underline font-semibold">Monthly Report</a>
            </div>
            <div>
                <a href="{{ url_for('logout') }}" class="text-red-600 hover:underline font-semibold">Logout</a>
            </div>
        </nav>
        <main class="bg-white rounded-lg shadow-lg p-8 max-w-4xl w-full">
            <h1 class="text-2xl font-bold mb-6 text-center">Laporan Harian - {date}</h1>
            <div class="space-y-4 max-w-md mx-auto">
                <div class="flex justify-between">
                    <span class="font-semibold">Pemasukan:</span>
                    <span class="text-green-600 font-semibold">Rp {report.get('income', 0):,}</span>
                </div>
                <div class="flex justify-between">
                    <span class="font-semibold">Pengeluaran:</span>
                    <span class="text-red-600 font-semibold">Rp {report.get('outcome', 0):,}</span>
                </div>
                <div class="flex justify-between border-t pt-4 mt-4 font-bold text-lg">
                    <span>Saldo:</span>
                    <span>Rp {report.get('balance', 0):,}</span>
                </div>
            </div>
        </main>
    </body>
    </html>
    """
    logger.info("Serving daily report page.")
    return render_template_string(html)

@app.route('/reports/monthly')
@login_required
def monthly_report():
    year_month = request.args.get('year_month')
    if not year_month:
        from datetime import datetime
        year_month = datetime.now().strftime('%Y-%m')
    report = data_storage.get_monthly_report(year_month)
    if report is None:
        return "Error generating monthly report", 500
    html = f"""
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Monthly Report</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <link href="https://fonts.googleapis.com/css2?family=Inter&display=swap" rel="stylesheet" />
        <style>body {{ font-family: 'Inter', sans-serif; }}</style>
    </head>
    <body class="bg-gray-100 min-h-screen flex flex-col items-center p-4">
        <nav class="bg-white shadow w-full max-w-4xl rounded mb-6 p-4 flex justify-between items-center">
            <div class="space-x-4">
                <a href="{{ url_for('home') }}" class="text-blue-600 hover:underline font-semibold">Home</a>
                <a href="{{ url_for('transactions') }}" class="text-blue-600 hover:underline font-semibold">Transactions</a>
                <a href="{{ url_for('budgets') }}" class="text-blue-600 hover:underline font-semibold">Budgets</a>
                <a href="{{ url_for('goals') }}" class="text-blue-600 hover:underline font-semibold">Goals</a>
                <a href="{{ url_for('daily_report') }}" class="text-blue-600 hover:underline font-semibold">Daily Report</a>
                <a href="{{ url_for('monthly_report') }}" class="text-blue-600 hover:underline font-semibold">Monthly Report</a>
            </div>
            <div>
                <a href="{{ url_for('logout') }}" class="text-red-600 hover:underline font-semibold">Logout</a>
            </div>
        </nav>
        <main class="bg-white rounded-lg shadow-lg p-8 max-w-4xl w-full">
            <h1 class="text-2xl font-bold mb-6 text-center">Laporan Bulanan - {year_month}</h1>
            <div class="space-y-4 max-w-md mx-auto">
                <div class="flex justify-between">
                    <span class="font-semibold">Pemasukan:</span>
                    <span class="text-green-600 font-semibold">Rp {report.get('income', 0):,}</span>
                </div>
                <div class="flex justify-between">
                    <span class="font-semibold">Pengeluaran:</span>
                    <span class="text-red-600 font-semibold">Rp {report.get('outcome', 0):,}</span>
                </div>
                <div class="flex justify-between border-t pt-4 mt-4 font-bold text-lg">
                    <span>Saldo:</span>
                    <span>Rp {report.get('balance', 0):,}</span>
                </div>
            </div>
        </main>
    </body>
    </html>
    """
    logger.info("Serving monthly report page.")
    return render_template_string(html)

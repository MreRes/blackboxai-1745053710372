import unittest
from data_storage import DataStorage

class TestWhatsAppBot(unittest.TestCase):

    def setUp(self):
        self.storage = DataStorage(':memory:')  # Use in-memory DB for testing

    def test_add_transaction_income(self):
        initial_report = self.storage.get_report()
        initial_income = initial_report['total_income']

        self.storage.add_transaction('income', 1000, 'Test income')
        updated_report = self.storage.get_report()
        self.assertEqual(updated_report['total_income'], initial_income + 1000)

    def test_add_transaction_outcome(self):
        initial_report = self.storage.get_report()
        initial_outcome = initial_report['total_outcome']

        self.storage.add_transaction('outcome', 500, 'Test outcome')
        updated_report = self.storage.get_report()
        self.assertEqual(updated_report['total_outcome'], initial_outcome + 500)

    def test_add_budget_and_get(self):
        self.storage.add_budget('TestCategory', 2000, 'monthly')
        budgets = self.storage.get_budgets()
        self.assertTrue(any(b['category'] == 'TestCategory' and b['amount'] == 2000 for b in budgets))

    def test_add_goal_and_get(self):
        self.storage.add_goal('TestGoal', 5000)
        goals = self.storage.get_goals()
        self.assertTrue(any(g['name'] == 'TestGoal' and g['target_amount'] == 5000 for g in goals))

    def test_update_goal_progress(self):
        self.storage.add_goal('ProgressGoal', 10000)
        goals = self.storage.get_goals()
        goal = next((g for g in goals if g['name'] == 'ProgressGoal'), None)
        self.assertIsNotNone(goal)
        self.storage.update_goal_progress(goal['id'], 3000)
        updated_goals = self.storage.get_goals()
        updated_goal = next((g for g in updated_goals if g['id'] == goal['id']), None)
        self.assertEqual(updated_goal['current_amount'], 3000)

    def test_get_daily_report(self):
        from datetime import datetime
        today = datetime.now().strftime('%Y-%m-%d')
        report = self.storage.get_daily_report(today)
        self.assertIn('income', report)
        self.assertIn('outcome', report)
        self.assertIn('balance', report)

    def test_get_monthly_report(self):
        from datetime import datetime
        month = datetime.now().strftime('%Y-%m')
        report = self.storage.get_monthly_report(month)
        self.assertIn('income', report)
        self.assertIn('outcome', report)
        self.assertIn('balance', report)

if __name__ == '__main__':
    unittest.main()

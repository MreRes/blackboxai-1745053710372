import unittest
from data_storage import DataStorage

class TestDataStorage(unittest.TestCase):

    def setUp(self):
        self.storage = DataStorage(':memory:')

    def test_add_and_get_budget(self):
        user_id = 1
        self.storage.add_budget(user_id, 'Food', 1000, 'monthly', '2024-01-01', '2024-01-31')
        budgets = self.storage.get_budgets(user_id)
        self.assertTrue(any(b['category'] == 'Food' and b['amount'] == 1000 for b in budgets))

    def test_add_and_get_goal(self):
        user_id = 1
        self.storage.add_goal(user_id, 'Vacation', 5000)
        goals = self.storage.get_goals(user_id)
        self.assertTrue(any(g['name'] == 'Vacation' and g['target_amount'] == 5000 for g in goals))

    def test_notifications_empty(self):
        user_id = 1
        notifications = self.storage.get_notifications(user_id)
        self.assertIsInstance(notifications, list)

if __name__ == '__main__':
    unittest.main()
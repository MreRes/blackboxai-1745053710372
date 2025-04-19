import pytest
from data_storage import DataStorage

@pytest.fixture(scope="module")
def storage():
    ds = DataStorage(':memory:')
    yield ds

def test_add_and_get_budget(storage):
    user_id = 1
    storage.add_budget(user_id, 'Food', 1000, 'monthly', '2024-01-01', '2024-01-31')
    budgets = storage.get_budgets(user_id)
    assert len(budgets) == 1
    assert budgets[0]['category'] == 'Food'
    assert budgets[0]['amount'] == 1000

def test_add_and_get_goal(storage):
    user_id = 1
    storage.add_goal(user_id, 'Vacation', 5000, '2024-12-31')
    goals = storage.get_goals(user_id)
    assert len(goals) == 1
    assert goals[0]['name'] == 'Vacation'
    assert goals[0]['target_amount'] == 5000

def test_notifications_empty(storage):
    user_id = 1
    notifications = storage.get_notifications(user_id)
    assert isinstance(notifications, list)

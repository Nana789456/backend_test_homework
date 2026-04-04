import pytest
from unittest.mock import patch, Mock


# ---- Тесты для save_report ----
@patch("sqlite3.connect")
def test_save_report_with_mock(mock_connect):
    """Тест с моком sqlite3.connect"""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    report = {"user_id": 1, "days": 10, "aggregated": "{}", "tariff": "free"}
    save_report(report)

    mock_connect.assert_called_once_with("reports.db")
    mock_cursor.execute.assert_any_call(
        "CREATE TABLE IF NOT EXISTS reports (\n            user_id INTEGER,\n            days INTEGER,\n            aggregated TEXT,\n            tariff TEXT\n        )"
    )
    mock_cursor.execute.assert_any_call(
        "INSERT INTO reports VALUES (?, ?, ?, ?)",
        (1, 10, "{}", "free")
    )
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

# ---- (Дополнительно) тест эндпоинта с моком всех зависимостей ----
@patch("main.save_report")
@patch("main.get_user_tariff")
@patch("main.aggregate_data")
def test_generate_report_endpoint_with_mocks(mock_aggregate, mock_get_tariff, mock_save_report):
    """Интеграционный тест эндпоинта с моками всех внешних зависимостей"""
    mock_aggregate.return_value = {"total": 500, "avg": 50}
    mock_get_tariff.return_value = "premium"

    from fastapi.testclient import TestClient
    client = TestClient(app)

    response = client.post("/report?user_id=2&days=5")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "report": {
            "user_id": 2,
            "days": 5,
            "aggregated": {"total": 500, "avg": 50},
            "tariff": "premium"
        }
    }
    mock_aggregate.assert_called_once_with(5)
    mock_get_tariff.assert_called_once_with(2)
    mock_save_report.assert_called_once_with({
        "user_id": 2,
        "days": 5,
        "aggregated": {"total": 500, "avg": 50},
        "tariff": "premium"
    })
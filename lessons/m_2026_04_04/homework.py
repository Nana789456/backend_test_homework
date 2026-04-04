"""
#дз
- Повторить проейденный материал
- Повторить что такое моки
- Повторить мокирование запросов
- Разобраться как работает код в данном файле:
-- Перенести тест в директорию tests
-- Запустить в дебагере
- Изучить что такое Авторизация и попробовать реализовать
- Подготовить вопросы
"""

# main.py
"""
Единый файл для демонстрации моков на занятии.
Содержит микросервис аналитики и тесты к нему.
Запуск приложения: uvicorn main:app --reload
Запуск тестов: pytest main.py -v
"""

import time
import sqlite3
import requests
from fastapi import FastAPI

# ==================== Компоненты сервиса ====================

def aggregate_data(days: int) -> dict:
    """Имитация тяжёлых вычислений"""
    time.sleep(2)
    return {"total": days * 100, "avg": 50}

def get_user_tier(user_id: int) -> str:
    """Запрос к внешнему API для получения тарифа пользователя"""
    response = requests.get(
        "https://httpbin.org/delay/1",
        params={"user_id": user_id}
    )
    response.raise_for_status()
    return "premium" if user_id % 2 == 0 else "free"

def save_report(report: dict) -> None:
    """Сохранение отчёта в SQLite БД"""
    conn = sqlite3.connect("reports.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            user_id INTEGER,
            days INTEGER,
            aggregated TEXT,
            tier TEXT
        )
    """)
    cursor.execute(
        "INSERT INTO reports VALUES (?, ?, ?, ?)",
        (report["user_id"], report["days"], str(report["aggregated"]), report["tier"])
    )
    conn.commit()
    conn.close()

# ==================== FastAPI приложение ====================

app = FastAPI()

@app.post("/report")
def generate_report(user_id: int, days: int):
    aggregated = aggregate_data(days)
    tier = get_user_tier(user_id)
    report = {
        "user_id": user_id,
        "days": days,
        "aggregated": aggregated,
        "tier": tier
    }
    save_report(report)
    return {"status": "ok", "report": report}

# ==================== Тесты (pytest) ====================

import pytest
from unittest.mock import patch, Mock

# ---- Тесты для aggregate_data ----
def test_aggregate_data_without_mock():
    """Медленный тест: реальный вызов с time.sleep"""
    result = aggregate_data(10)
    assert result["total"] == 1000

@patch("main.aggregate_data")
def test_aggregate_data_with_mock(mock_aggregate):
    """Быстрый тест: мок функции aggregate_data"""
    mock_aggregate.return_value = {"total": 100, "avg": 10}

    result = aggregate_data(10)

    assert result["total"] == 100
    mock_aggregate.assert_called_once_with(10)

# ---- Тесты для get_user_tier ----
def test_get_user_tier_without_mock():
    """Тест с реальным запросом к сети"""
    result = get_user_tier(1)
    assert result in ["premium", "free"]

@patch("requests.get")
def test_get_user_tier_with_mock(mock_get):
    """Тест с моком requests.get"""
    mock_response = Mock()
    mock_response.raise_for_status.return_value = None
    mock_response.json.return_value = {}
    mock_get.return_value = mock_response

    result = get_user_tier(1)

    mock_get.assert_called_once_with(
        "https://httpbin.org/delay/1",
        params={"user_id": 1}
    )
    assert result == "free"

# ---- Тесты для save_report ----
@patch("sqlite3.connect")
def test_save_report_with_mock(mock_connect):
    """Тест с моком sqlite3.connect"""
    mock_conn = Mock()
    mock_cursor = Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_connect.return_value = mock_conn

    report = {"user_id": 1, "days": 10, "aggregated": "{}", "tier": "free"}
    save_report(report)

    mock_connect.assert_called_once_with("reports.db")
    mock_cursor.execute.assert_any_call(
        "CREATE TABLE IF NOT EXISTS reports (\n            user_id INTEGER,\n            days INTEGER,\n            aggregated TEXT,\n            tier TEXT\n        )"
    )
    mock_cursor.execute.assert_any_call(
        "INSERT INTO reports VALUES (?, ?, ?, ?)",
        (1, 10, "{}", "free")
    )
    mock_conn.commit.assert_called_once()
    mock_conn.close.assert_called_once()

# ---- (Дополнительно) тест эндпоинта с моком всех зависимостей ----
@patch("main.save_report")
@patch("main.get_user_tier")
@patch("main.aggregate_data")
def test_generate_report_endpoint_with_mocks(mock_aggregate, mock_get_tier, mock_save_report):
    """Интеграционный тест эндпоинта с моками всех внешних зависимостей"""
    mock_aggregate.return_value = {"total": 500, "avg": 50}
    mock_get_tier.return_value = "premium"

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
            "tier": "premium"
        }
    }
    mock_aggregate.assert_called_once_with(5)
    mock_get_tier.assert_called_once_with(2)
    mock_save_report.assert_called_once_with({
        "user_id": 2,
        "days": 5,
        "aggregated": {"total": 500, "avg": 50},
        "tier": "premium"
    })

# ==================== Точки входа ====================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
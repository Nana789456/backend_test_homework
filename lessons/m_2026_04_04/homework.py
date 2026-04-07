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

def aggregate_data(days: int) -> dict: # Имитация тяжёлых вычислений на CPU (процессоре) и GPU (видео карте), т.е векторные вычисление
    """Имитация тяжёлых вычислений"""
    time.sleep(2)
    return {"total": days * 100, "avg": 50}

def get_user_tariff(user_id: int) -> str:
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
            tariff TEXT
        )
    """)
    cursor.execute(
        "INSERT INTO reports VALUES (?, ?, ?, ?)",
        (report["user_id"], report["days"], str(report["aggregated"]), report["tariff"])
    )
    conn.commit()
    conn.close()

# ==================== FastAPI приложение ====================

app = FastAPI()

@app.post("/report")
def generate_report(user_id: int, days: int):
    aggregated = aggregate_data(days)
    tariff = get_user_tariff(user_id)
    report = {
        "user_id": user_id,
        "days": days,
        "aggregated": aggregated,
        "tariff": tariff
    }
    save_report(report)
    return {"status": "ok", "report": report}


def hello():
    return "real"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

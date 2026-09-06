<h1 align="center">CryptoTracker Bot</h1>
<p align="center">
  <b>Telegram-бот для отслеживания цен криптовалют</b><br>
  <i>Python Backend | Django | aiogram | Celery | Docker</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python" />
  <img src="https://img.shields.io/badge/Django-6.1-green?logo=django" />
  <img src="https://img.shields.io/badge/aiogram-3.30.0-blue?logo=telegram" />
  <img src="https://img.shields.io/badge/Docker-Compose-blue?logo=docker" />
  <img src="https://img.shields.io/badge/PostgreSQL-15-blue?logo=postgresql" />
  <img src="https://img.shields.io/badge/Celery-5.6.3-green?logo=celery" />
  <img src="https://img.shields.io/badge/Redis-8.1.0-red?logo=redis" />
</p>

---

## Описание / Overview

Асинхронный Telegram-бот, который позволяет:
- Выбрать криптовалюту и задать целевую цену
- Получать уведомление, когда цена достигнута
- Отслеживать несколько монет одновременно

Фоновая проверка цен реализована через **Celery + Redis**. Данные хранятся в **PostgreSQL** через Django ORM.

---

## Технологический стек / Tech Stack

| Категория | Технологии                       |
|-----------|----------------------------------|
| **Backend** | Python 3.13, Django, Django ORM  |
| **Bot** | aiogram 3.30.0, FSM              |
| **API** | CoinGecko API, aiohttp           |
| **База данных** | PostgreSQL 15                    |
| **Брокер задач** | Redis 8.1.0                      |
| **Фоновые задачи** | Celery 5.6.3, django-celery-beat |
| **DevOps** | Docker, Docker Compose           |

---

## Быстрый старт / Quick Start

```bash
  # 1. Клонировать репозиторий
git clone https://github.com/Stas-W1nt3R/tg_crypto_bot.git
cd tg_crypto_bot

# 2. Создать .env 
cp .env.example .env
# Отредактировать .env (BOT_TOKEN, API_KEY)

# 3. Запустить в Docker
docker-compose up --build
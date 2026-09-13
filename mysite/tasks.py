from celery import shared_task
from celery.schedules import crontab
from TgBot_WB.celery import app
from .models import UserTracking, Cryptocurrency
from django.conf import settings
import requests
from aiogram import Bot
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


@shared_task
def send_notification_to_user(chat_id, tracking_id):
    token = settings.BOT_TOKEN
    track = UserTracking.objects.get(id=tracking_id)

    bot = Bot(token=token)
    try:
        async_to_sync(bot.send_message)(
            chat_id=chat_id,
            text=f"Цена {track.cryptocurrency.name} достигла цели в {track.target_price}$")
    finally:
        async_to_sync(bot.session.close())

@shared_task
def check_all_price():
    trackings = UserTracking.objects.filter(is_active=True)
    url = ("https://api.coingecko.com/api/v3/simple/price?vs_currencies=usd&ids=")
    coin_names = set()

    for tracking in trackings:
        coin_names.add(tracking.cryptocurrency.coin_id)

    if not coin_names:
        return

    url += ",".join(coin_names)
    key = settings.API_KEY
    url += f"&x_cg_demo_api_key={key}"

    response = requests.get(url, timeout=10)
    data = response.json()

    if not data:
        return

    for tracking in trackings:
        try:
            coin_id = tracking.cryptocurrency.coin_id
            if coin_id not in data:
                continue

            current_price = data[tracking.cryptocurrency.coin_id]["usd"]

            if current_price >= tracking.target_price:
                tracking.is_active = False
                tracking.save()
                chat_id = tracking.user.telegram_id
                send_notification_to_user.delay(chat_id, tracking.id)

            channel_layer = get_channel_layer()
            async_to_sync(channel_layer.group_send)('cryptocurrency', {
                'type': 'send_price',
                coin_id: current_price,
            })

        except UserTracking.DoesNotExist:
            continue

        except Exception as e:
            print(f"Ошибка при проверке трекинга {tracking.id}: {e}")
            continue

app.conf.beat_schedule = {
    'check-price': {
        'task': 'mysite.tasks.check_all_price',
        'schedule': crontab(minute='*/1'),
    }
}

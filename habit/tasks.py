from celery import shared_task
from django.utils.timezone import now

from .models import Subscription
from .services import send_telegram_message


@shared_task
def send_due_reminders():
    today = now().date()
    subs = Subscription.objects.select_related("habit", "subscriber").all()
    for sub in subs:
        if not sub.last_reminded or (today - sub.last_reminded).days >= sub.habit.frequency_days:
            chat_id = sub.user.telegram_chat_id
            if chat_id:
                text = f'Время "{sub.habit.action}" в {sub.habit.time} в {sub.habit.place}.'
                send_telegram_message(chat_id, text)
                sub.last_reminded = today
                sub.save()

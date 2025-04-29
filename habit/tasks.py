from datetime import timedelta

from celery import shared_task
from django.utils.timezone import now

from habit.models import Habit
from habit.services import send_tg_message, is_today


@shared_task
def remind_habits():
    date = now().date()
    time = now().time()

    for habit in Habit.objects.all():
        print(f"check {habit.id}")
        habit_time = timedelta(
            hours=habit.time.hour,
            minutes=habit.time.minute,
            seconds=habit.time.second
        ).total_seconds()

        current_time = timedelta(
            hours=time.hour,
            minutes=time.minute,
            seconds=time.second
        ).total_seconds()

        if abs(habit_time - current_time) < 60:
            if is_today(habit.periodicity, habit.user.date_joined.date(), date) and habit.user.tg_chat_id:
                text = f"Напоминание: пора выполнить привычку '{habit.action}' в {habit.place}."
                print(habit.user.tg_chat_id)
                send_tg_message(habit.user.tg_chat_id, text)

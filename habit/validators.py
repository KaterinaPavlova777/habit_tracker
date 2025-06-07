from datetime import timedelta

from rest_framework import serializers


class RelatedOrReward:
    def __call__(self, value):
        if value.get('related') and value.get('reward'):
            raise serializers.ValidationError('Разрешёно только выбрать связанную привычку или вознаграждение')


class LimitLeadTime:
    def __init__(self):
        self.max_duration = timedelta(minutes=2)

    def __call__(self, value):
        lead_time = value.get('lead_time')
        if lead_time and lead_time > self.max_duration:
            raise serializers.ValidationError(f"Время выполнения не должно превышать {self.max_duration}.")


class ValidRelated:
    def __call__(self, value):
        new_obj = value.get('related')
        if new_obj and not new_obj.pleasant:
            raise serializers.ValidationError("Можно связывать только полезные с приятными привычками")

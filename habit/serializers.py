from rest_framework import serializers

from habit.models import Habit
from habit.validators import RelatedOrReward, LimitLeadTime, ValidRelated


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [RelatedOrReward(), LimitLeadTime(), ValidRelated()]

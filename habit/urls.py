from django.urls import path

from habit.apps import HabitConfig
from habit.views import HabitList, HabitCreate, HabitUpdate, HabitDestroy, HabitDetail, HabitOwnList

app_name = HabitConfig.name

urlpatterns = [
    path('', HabitList.as_view(), name='habit-list'),
    path('own/', HabitOwnList.as_view(), name='habit-own'),
    path('create/', HabitCreate.as_view(), name='habit-create'),
    path('update/<int:pk>', HabitUpdate.as_view(), name='habit-update'),
    path('detail/<int:pk>', HabitDetail.as_view(), name='habit-detail'),
    path('delete/<int:pk>', HabitDestroy.as_view(), name='habit-delete'),
]

import random

import factory
from factory import LazyFunction
from factory.django import DjangoModelFactory

from taskstate.tasks.models import Task


class TaskFactory(DjangoModelFactory):
    class Meta:
        model = Task
    title = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('sentence', nb_words=15)
    state = LazyFunction(lambda: random.choice(list(Task.STATES._db_values)))

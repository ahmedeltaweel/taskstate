from django.db import models
from django.utils.translation import ugettext as _
from model_utils.choices import Choices
from model_utils.models import TimeStampedModel


class Task(TimeStampedModel):
    STATES = Choices(
        (0, 'NEW', _('New')),
        (1, 'IN_PROGRESS', _('In Progress')),
        (2, 'DONE', _('Done'))
    )

    title = models.CharField(_('Task Title'), max_length=200, db_index=True)
    description = models.TextField(_('Task Description'))
    state = models.PositiveSmallIntegerField(_('Task State'), choices=STATES, default=STATES.NEW)
    linked_task = models.ForeignKey('self', on_delete=models.SET_NULL,
                                    related_name='linked_tasks', null=True, blank=True)

    def __str__(self):
        return self.title

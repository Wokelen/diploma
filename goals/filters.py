from typing import Dict, Tuple

import django_filters
from django.db import models
from django_filters import rest_framework

from goals.models import Goal


class GoalDateFilter(rest_framework.FilterSet):

    class Meta:

        model: models.Model = Goal
        fields: Dict[str, Tuple[str, ...]] = {
            "due_date": ("lte", "gte"),
            "category": ("exact", "in"),
            "status": ("exact", "in"),
            "priority": ("exact", "in"),
        }

    filter_overrides = {
        models.DateTimeField: {"filter_class": django_filters.IsoDateTimeFilter},
    }

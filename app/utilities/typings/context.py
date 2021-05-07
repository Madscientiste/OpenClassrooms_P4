from typing import TypedDict

from .models import Models
from .views import Views


class Context(TypedDict):
    views: Views
    models: Models

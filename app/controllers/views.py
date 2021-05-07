from app.utilities import typings

from .base import baseController


class Views(baseController):
    def __init__(self, *args, **kwargs):
        self.cache: typings.Views
        super().__init__(search_class="View", *args, **kwargs)

    def __getitem__(self, key: typings.Views):
        return self.get(key)

    def get(self, view_name: str):
        view = self.cache.get(view_name)
        
        return self.reload(view_name, view.__module__)

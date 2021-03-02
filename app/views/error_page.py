from .abc import BaseView


class ErrorView(BaseView):
    def render(self, *args, **kwargs):
        pass
from app.controllers.views import Views


class BaseError(Exception):
    """Base Exception"""

    custom = True
    views = Views(package="app.views")

    error_view = views["error"]
    main_view = views["main"]

    def render(self, *args, **kwargs):
        """Render the main page by default"""

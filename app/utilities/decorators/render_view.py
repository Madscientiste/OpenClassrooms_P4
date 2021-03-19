def render_view(func):
    """Decorator to render a view"""
    
    def wrapper(self, *args, **kwargs):
        output = func(*args, **kwargs)

        self.add_body(output)
        self.set_footer("END")
        self.render_view()

    return wrapper
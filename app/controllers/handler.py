class Handle:
    def __init__(self) -> None:
        pass
    
    @classmethod
    def exceptions(cls, func):
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except KeyboardInterrupt:
                print("Application has been terminated")

            return func

        return wrapper
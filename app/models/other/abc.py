# flake8: noqa

class BaseModel:
    resolvables: dict = {}

    def to_dict(self) -> dict:
        """Convert the current class into a dictionnary"""
        serialized: dict = vars(self)
        serialize = lambda value: value.to_dict() if hasattr(value, "to_dict") else value

        for key, value in serialized.items():
            if type(value) in [tuple, list]:
                serialized[key] = [serialize(x) for x in value]
            else:
                serialized[key] = serialize(value)
        return serialized

    @classmethod
    def resolve(cls, instance: dict):
        """Resolve a dictionnary into an object"""
        instance_type = type(instance)
        if not instance_type == dict:
            return instance

        resolved = {}

        for key, value in instance.items():
            model: cls = cls.resolvables.get(key)

            if model:
                if type(value) in [tuple, list]:
                    resolved[key] = [model.resolve(x) for x in value]
                else:
                    resolved[key] = model(**value) if value else value
            else:
                resolved[key] = value

        return cls(**resolved)

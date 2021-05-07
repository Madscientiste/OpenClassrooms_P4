import re
from pathlib import Path
from tinydb import TinyDB, Query, table

from app.utilities import errors

STORAGE_PATH = Path(__file__).parent / "storage"


class BaseDB:
    database: TinyDB
    resolvables: dict

    def save(self, doc_id=None):
        """Create a new item or update the current one"""
        dictified: dict = self.to_dict()
        item_id: int = dictified["id"] or None

        if item_id and self.database.contains(doc_id=item_id):
            del dictified["id"]
            self.id = self.database.update(dictified, doc_ids=[item_id]).pop(0)
        else:
            del dictified["id"]
            insert = table.Document(dictified, doc_id) if doc_id else dictified
            self.id = self.database.insert(insert)

        return self.resolve(self.to_dict())

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
        """Resolve tinyDB document into an object"""
        instance_type = type(instance) == table.Document
        resolved = {}

        for key, value in instance.items():
            model = cls.resolvables.get(key)

            instance.doc_id if instance_type else None

            if model:
                if type(value) in [tuple, list]:
                    resolved[key] = [model.resolve(x) for x in value]
                else:
                    resolved[key] = model(**value)
            else:
                resolved[key] = value

        return cls(**resolved, **vars(instance) if instance_type else {})

    @classmethod
    def find_one(cls, id):
        """Find one item in the database"""
        instance_name = cls.__name__

        if not id:
            raise errors.GenericError(f"Missing {instance_name}_id")

        if not id.isdigit():
            raise errors.GenericError(f"{instance_name}_id must be a number")

        id = int(id)

        has_id: bool = cls.database.contains(doc_id=id)

        if not has_id:
            return has_id

        return cls.resolve(cls.database.get(doc_id=id))

    @classmethod
    def find_many(cls, key=None, value=None):
        """Find many items in the database"""
        if not key or not value:
            return [cls.resolve(x) for x in cls.database.all()]

        query = Query()
        key = getattr(query, key)

        search_criteria = key == value

        if key in ["first_name", "last_name"]:
            search_criteria = key.matches(value, re.IGNORECASE)

        return [cls.resolve(x) for x in cls.database.search(search_criteria)]
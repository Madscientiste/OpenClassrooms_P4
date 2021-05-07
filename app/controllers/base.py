import sys

import importlib
from importlib import resources


class baseController:
    """Base Controller

    Handle the import of the files, when initialized the file get cached.

    Attributes
    ----------
    blacklist : list
        A list of the files that need to be ignored in the folder, eg `__init__`.
    package : str
        The package which holds the files that need to be cached, eg `app.commands`.
    search_class : str
        The class inside the module that is being loaded, eg `Command` which is inside app.commands.player.
    cache : dict
        Where everything is stored, it will contain a key and an object, eg `player : <player object>`.
    """

    def __init__(self, search_class, package, blacklist: list = ["__init__", "base", "abc"]) -> None:
        self.blacklist = blacklist
        self.package = package

        self.cache: dict = {}
        self.search_class: str = search_class

        files = resources.contents(package)
        files = [file[:-3] for file in files if file.endswith(".py")]
        files = [item for item in files if item not in blacklist]

        for file_name in files:
            module = importlib.import_module(f"{self.package}.{file_name}")
            self.cache[file_name] = getattr(module, self.search_class)()

    def reload(self, name, package) -> dict:
        """Reload a cached module.

        Args:
            name: the name of the cached module.
            package: The package where the module is imported from.

        Returns:
            the reloaded module.

        """
        module = sys.modules[package]
        module = importlib.reload(module)

        self.cache[name] = getattr(module, self.search_class)()
        return self.cache[name]

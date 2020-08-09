import logging
from random import randint
from cyckei.plugins import cyp_base
import os.path

logger = logging.getLogger("cyckei")


class PluginController(cyp_base.BaseController):
    def __init__(self, sources):
        base_path = os.path.join(os.path.dirname(__file__), "..")
        super().__init__("mettler-ag204", base_path)

    def get_sources(self):
        """
        Searches for available sources, and establishes source objects.

        Returns
        -------
        Dictionary of sources in format "name": SourceObject.
        """

        # Sources don't need to be found for this plugin,
        # so we just initialize two randomizers as examples
        sources = {}
        sources["Rand1"] = PluginSource(10)
        sources["Rand2"] = PluginSource(20)

        return sources


class PluginSource(cyp_base.BaseSource):
    def __init__(self, port):
        super().__init__()
        self.range = [0, port]
        self.name = f"Random 0-{port}"

    def read(self):
        return randint(self.range[0], self.range[1])


if __name__ == "__main__":
    controller = PluginController()
    print(cyp_base.read_all(controller))

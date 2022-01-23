import kivy.app
import xindmap.view.config as xconfig

from .XindmapCommandDict import XindmapCommandDict
from .XindmapController import XindmapController

class XindmapApp(kivy.app.App):
    """Xindmap app class.
    """
    def __init__(self, config_file_path, **kwargs):
        """Instantiates the Xindmap app.

        Args:
            config: the app config
        """
        super().__init__(**kwargs)
        
        self.__command_dict = XindmapCommandDict()
        
        self.config_file_path = config_file_path
        self.__config_parser = xconfig.ConfigParser()

    def init(self):
        """Inits this app.
        """
        self.__config_parser.parse_config_file(self.config_file_path)

    def build(self):
        """Builds the Xindmap app.
        """
        return XindmapController(self.__config_parser.config)


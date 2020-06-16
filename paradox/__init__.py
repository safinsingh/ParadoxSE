from .loader import Loader
from .functions import Functions
from .config import parse_cli


class ParadoxSE(Functions):
    def __init__(self, production=False):
        """Initializing method for the ParadoxSE class

        Args:
            production (bool, optional): Whether to build for production or not. Defaults to False.
        """

        self.verbose = vars(parse_cli())["verbose"]

        self.vulns = []
        self.points = []

        self.pen = []
        self.penpoints = []

        self.totalscore = 0

        self.loader = Loader("config.yml", production).load()

        if production == False:
            self.data = self.loader
        else:
            self.data = "PLACEHOLDER"

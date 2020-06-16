import yaml
import os


class Loader():
    def __init__(self, file, production):
        """Initialization function for loader

        Args:
            file (string): Name of the file to read configuration from
            production (bool): Whether to build for production
        """
        self.file = os.path.join(os.path.dirname(__file__), "..", file)
        self.production = False  # for future releases (currently deprecated)

    def load(self):
        """Load and parse configuration file
        """
        if not self.production:
            with open(self.file) as f:
                data = yaml.load(f, Loader=yaml.FullLoader)
        else:
            data = self.parse()

            with open("engine.py", "r") as f:
                fdata = f.read()

            fdata = fdata.replace("PLACEHOLDER", data)

            with open("engine.py", "w") as f:
                f.write(fdata)

        return(data)

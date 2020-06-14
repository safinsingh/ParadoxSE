import yaml
from os import path


class ParadoxSE():
    def __init__(self, config):
        self.config = config
        self.data = {}
        self.points = 0

    def parse(self):
        with open(self.config) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        self.data = data
        return self.data

    def string_in_file(self, obj):
        if path.exists(obj[0]["file"]):
            with open(obj[0]["file"]) as f:
                if obj[1]["string"] in f.read():
                    return obj[2]["points"]
                return 0
        return 0

    def update(self):
        for func in self.data:
            self.points += getattr(self, func)(self.data[func])
            print(self.points)

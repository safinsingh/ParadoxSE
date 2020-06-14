import yaml
from os import path
import subprocess
import apt


class ParadoxSE():
    def __init__(self, config):
        self.config = config
        self.data = {}
        self.apt = apt.Cache()
        self.vulns = []
        self.points = []

    def parse(self):
        with open(self.config) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)

        self.data = data
        return self.data

    def string_in_file(self, obj):
        if path.exists(obj[1]["file"]):
            with open(obj[1]["file"]) as f:
                if obj[2]["string"] in f.read():
                    self.vulns.append(obj[0]["name"])
                    self.points.append(obj[3]["points"])

    def string_not_in_file(self, obj):
        if path.exists(obj[1]["file"]):
            with open(obj[1]["file"]) as f:
                if obj[2]["string"] not in f.read():
                    self.vulns.append(obj[0]["name"])
                    self.points.append(obj[3]["points"])

    def package_installed(self, obj):
        if self.apt[obj[1]["package"]].is_installed:
            self.vulns.append(obj[0]["name"])
            self.points.append(obj[2]["points"])

    def package_not_installed(self, obj):
        if not self.apt[obj[1]["package"]].is_installed:
            self.vulns.append(obj[0]["name"])
            self.points.append(obj[2]["points"])

    def update(self):
        self.apt = apt.Cache()

        for func in self.data:
            getattr(self, func)(self.data[func])

        print(self.points)
        print(self.vulns)

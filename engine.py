import yaml
from os import path
import subprocess
import apt
import pwd
import grp


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
                    return obj[0]["name"], obj[3]["points"]

    def string_not_in_file(self, obj):
        if path.exists(obj[1]["file"]):
            with open(obj[1]["file"]) as f:
                if obj[2]["string"] not in f.read():
                    return obj[0]["name"], obj[3]["points"]

    def package_installed(self, obj):
        if self.apt[obj[1]["package"]].is_installed:
            return obj[0]["name"], obj[2]["points"]

    def package_not_installed(self, obj):
        if not self.apt[obj[1]["package"]].is_installed:
            return obj[0]["name"], obj[2]["points"]

    def firewall_up(self, obj):
        if "Status: active" in subprocess.getoutput("sudo ufw status | grep 'Status: active'"):
            return obj[0]["name"], obj[1]["points"]

    def user_exists(self, obj):
        if obj[1]["user"] in [entry.pw_name for entry in pwd.getpwall()]:
            return obj[0]["name"], obj[2]["points"]

    def user_doesnt_exist(self, obj):
        if obj[1]["user"] not in [entry.pw_name for entry in pwd.getpwall()]:
            return obj[0]["name"], obj[2]["points"]

    def group_exists(self, obj):
        if obj[1]["group"] in [entry.gr_name for entry in grp.getgrall()]:
            return obj[0]["name"], obj[2]["points"]

    def group_doesnt_exist(self, obj):
        if obj[1]["group"] not in [entry.gr_name for entry in grp.getgrall()]:
            return obj[0]["name"], obj[2]["points"]

    def user_in_group(self, obj):
        if self.group_exists([{"name": ""}, {"group": obj[2]["group"]}, {"points": 0}]) != None:
            if obj[1]["user"] in grp.getgrnam(obj[2]["group"]).gr_mem:
                return obj[0]["name"], obj[3]["points"]

    def user_not_in_group(self, obj):
        if self.group_exists([{"name": ""}, {"group": obj[2]["group"]}, {"points": 0}]) != None:
            if obj[1]["user"] not in grp.getgrnam(obj[2]["group"]).gr_mem:
                return obj[0]["name"], obj[3]["points"]

    def service_up(self, obj):
        if subprocess.getoutput("systemctl is-active '" + obj[1]["service"] + "'") == "active":
            return obj[0]["name"], obj[2]["points"]

    def update(self):
        self.apt = apt.Cache()

        for func in self.data:
            res = getattr(self, func)(self.data[func])
            if res != None:
                self.vulns.append(res[0])
                self.points.append(res[1])

        print(self.points)
        print(self.vulns)

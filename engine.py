import os
import subprocess
import apt
import pwd
import grp
import stat
from loader import Loader


class ParadoxSE():
    def __init__(self, production=False):
        self.apt = apt.Cache()

        self.vulns = []
        self.points = []

        self.pen = []
        self.penpoints = []

        self.loader = Loader("config.yaml", production).load()

        if production == False:
            self.data = self.loader.parse()
        else:
            self.data = "PLACEHOLDER"

    def string_in_file(self, obj):
        if os.path.exists(obj[1]["file"]):
            with open(obj[1]["file"]) as f:
                if obj[2]["string"] in f.read():
                    return obj[0]["name"], obj[3]["points"]

    def string_not_in_file(self, obj):
        if os.path.exists(obj[1]["file"]):
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

    def service_down(self, obj):
        if subprocess.getoutput("systemctl is-active '" + obj[1]["service"] + "'") != "active":
            return obj[0]["name"], obj[2]["points"]

    def file_perm_is(self, obj):
        st = oct(os.stat(obj[1]["file"]).st_mode)[-4:]
        if st == str(obj[2]["perm"]):
            return obj[0]["name"], obj[3]["points"]

    def file_perm_isnt(self, obj):
        st = oct(os.stat(obj[1]["file"]).st_mode)[-4:]
        if not st == str(obj[2]["perm"]):
            return obj[0]["name"], obj[3]["points"]

    def command_succeeds(self, obj):
        code = subprocess.call(obj[1]["command"])
        if code == 0:
            return obj[0]["name"], obj[2]["points"]

    def command_fails(self, obj):
        code = subprocess.call(obj[1]["command"])
        if code != 0:
            return obj[0]["name"], obj[2]["points"]

    def update(self):
        self.apt = apt.Cache()

        for func in self.data:
            res = getattr(self, func)(self.data[func])
            if res != None:
                if not self.data[func][-1]["penalty"]:
                    self.vulns.append(res[0])
                    self.points.append(res[1])
                elif self.data[func][-1]["penalty"]:
                    self.pen.append(res[0])
                    self.penpoints.append(-1 * res[1])

        print(self.points)
        print(self.vulns)

        open("report/report.html", "w").close()

        with open("report/report.html", "a") as f:
            f.write("""<!DOCTYPE html>
<html>
    <head>
        <title>Vulnerability Analysis Report</title>

        <link
            rel="stylesheet"
            href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css"
            integrity="sha384-9aIt2nRpC12Uk9gS9baDl411NQApFmC26EwAOH8WgZl5MYYxFfc+NcPb1dKGj7Sk"
            crossorigin="anonymous"
        />

        <script
            src="https://code.jquery.com/jquery-3.5.1.slim.min.js"
            integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj"
            crossorigin="anonymous"
        ></script>
        <script
            src="https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js"
            integrity="sha384-Q6E9RHvbIyZFJoft+2mJbHaEWldlvI9IOYy5n3zV9zzTtmI3UksdQRVvoxMfooAo"
            crossorigin="anonymous"
        ></script>
        <script
            src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/js/bootstrap.min.js"
            integrity="sha384-OgVRvuATP1z7JjHLkuOU7Xw704+h835Lr+6QL9UvYjZE3Ipu6Tp75j7Bh/kR0JKI"
            crossorigin="anonymous"
        ></script>

        <link rel="stylesheet" href="../static/main.css" />
        <!-- <link rel="stylesheet" href="../static/css/main.css" /> -->
    </head>
    <body>
        <div class="root">
            <div class="container">
                <h1>ParadoxSE</h1>
                <h3>Vulnerability Analysis Report</h3>
                <hr />
                <div class="vulns">
                    <span id="vcont">
                        <h2>System Integrity Score: <scs>""")
            f.write(str(sum(self.points) + sum(self.penpoints)))
            f.write("""</scs></h2>
                        <div class="passed">
                            <h5>Checks <scs>Passed:</scs></h5>
                            <div class="row">
                                <div class="col-md-8">
                                    <ol>""")
            for el in self.vulns:
                f.write("<li>" + el + "</li>")

            f.write("""</ol>
                                </div>
                                <div class="col-md-4 passvals">
                                    <ol>""")

            for el in self.points:
                el = "+" + str(el)

                f.write("<li><scs>" + el + "</scs></li>")

            f.write("""</ol>
                                </div>
                            </div>
                        </div>
                        <div class="passed">
                            <h5>Checks <fail>Failed:</fail></h5>
                            <div class="row">
                                <div class="col-md-8">
                                    <ol>""")

            for el in self.pen:
                f.write("<li>" + el + "</li>")

            f.write("""</ol>
                                </div>
                                <div class="col-md-4 passvals">
                                    <ol>""")

            for el in self.penpoints:
                f.write("<li><fail>" + str(el) + "</fail></li>")

            f.write("""</ol>
                                </div>
                            </div>
                        </div>
                    </span>
                </div>
            </div>
        </div>
    </body>
</html>
""")

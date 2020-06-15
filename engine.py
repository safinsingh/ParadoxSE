import os
import subprocess
import apt
import pwd
import grp
import stat
from loader import Loader


class ParadoxSE():
    def __init__(self, production=False):
        """Initializing method for the ParadoxSE class

        Args:
            production (bool, optional): Whether to build for production or not. Defaults to False.
        """
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
        """Checks if a string is present in a file

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        file = obj[1]["file"]
        string = obj[2]["string"]
        points = obj[3]["points"]

        if os.path.exists(file):
            with open(file) as f:
                if string in f.read():
                    return name, points

    def string_not_in_file(self, obj):
        """Checks if a string is not present in a file

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        file = obj[1]["file"]
        string = obj[2]["string"]
        points = obj[3]["points"]

        if os.path.exists(obj[1]["file"]):
            with open(obj[1]["file"]) as f:
                if obj[2]["string"] not in f.read():
                    return obj[0]["name"], obj[3]["points"]

    def package_installed(self, obj):
        """Checks if a package is installed on the system

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        package = obj[1]["package"]
        points = obj[2]["points"]

        if self.apt[package].is_installed:
            return name, points

    def package_not_installed(self, obj):
        """Checks if a package is not installed on the system

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        package = obj[1]["package"]
        points = obj[2]["points"]

        if not self.apt[package].is_installed:
            return name, points

    def firewall_up(self, obj):
        """Checks if the firewall is running

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        points = obj[1]["points"]
        
        if "Status: active" in subprocess.getoutput("sudo ufw status | grep 'Status: active'"):
            return name, points

    def user_exists(self, obj):
        """Checks if a user exists on the system

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        user = obj[1]["user"]
        points = obj[2]["points"]
        
        if user in [entry.pw_name for entry in pwd.getpwall()]:
            return name, points

    def user_doesnt_exist(self, obj):
        """Checks if a user does not exist on the system

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        user = obj[1]["user"]
        points = obj[2]["points"]

        if obj[1]["user"] not in [entry.pw_name for entry in pwd.getpwall()]:
            return obj[0]["name"], obj[2]["points"]

    def group_exists(self, obj):
        """Checks if a group exists on the system

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        group = obj[1]["group"]
        points = obj[2]["points"]

        if group in [entry.gr_name for entry in grp.getgrall()]:
            return name, points

    def group_doesnt_exist(self, obj):
        """Checks if a group does not exist on the system

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        group = obj[1]["group"]
        points = obj[2]["points"]

        if group not in [entry.gr_name for entry in grp.getgrall()]:
            return name, points

    def user_in_group(self, obj):
        """Checks if a user exists in the specified group

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        user = obj[1]["user"]
        group = obj[2]["group"]
        points = obj[3]["points"]

        if self.group_exists([{"name": ""}, {"group": group}, {"points": 0}]) != None:
            if user in grp.getgrnam(group).gr_mem:
                return name, points

    def user_not_in_group(self, obj):
        """Checks if a user does not exist in the specified group

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        user = obj[1]["user"]
        group = obj[2]["group"]
        points = obj[3]["points"]

        if self.group_exists([{"name": ""}, {"group": group}, {"points": 0}]) != None:
            if user not in grp.getgrnam(group).gr_mem:
                return name, points

    def service_up(self, obj):
        """Checks if a systemctl service is up on the system

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        service = obj[1]["service"]
        points = obj[2]["points"]

        if subprocess.getoutput("systemctl is-active '" + service + "'") == "active":
            return name, points

    def service_down(self, obj):
        """Checks if a systemctl service is down on the system

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        service = obj[1]["service"]
        points = obj[2]["points"]

        if subprocess.getoutput("systemctl is-active '" + service + "'") != "active":
            return name, points

    def file_perm_is(self, obj):
        """Checks if the specified file has the specified octal permissions

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        file = obj[1]["file"]
        perm = obj[2]["perm"]
        points = obj[3]["points"]

        st = oct(os.stat(file).st_mode)[-4:]
        if st == str(perm):
            return name, points

    def file_perm_isnt(self, obj):
        """Checks if the specified file does not have the specified octal permissions

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        file = obj[1]["file"]
        perm = obj[2]["perm"]
        points = obj[3]["points"]

        st = oct(os.stat(file).st_mode)[-4:]
        if st != str(perm):
            return name, points

    def command_succeeds(self, obj):
        """Checks if a command succeeds

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        command = obj[1]["command"]
        points = obj[2]["points"]

        code = subprocess.call(command)
        if code == 0:
            return name, points

    def command_fails(self, obj):
        """Checks if a command fails

        Args:
            obj (array): Contains a list of dictionaries specific to each directive in the config YAML

        Returns:
            tuple: If successful, returns tuple containing name of vulnerability and point value
        """
        name = obj[0]["name"]
        command = obj[1]["command"]
        points = obj[2]["points"]

        code = subprocess.call(command)
        if code != 0:
            return name, points

    def update(self):
        """Loops through all checks in YAML configuration and writes updates to Score Report
        """
        self.apt = apt.Cache()

        for func in self.data:
            res = getattr(self, func)(self.data[func])
            if res != None:
                penbool = self.data[func][-1]["penalty"]
                scrname = res[0]
                scrpoints = res[1]

                if not penbool:
                    self.vulns.append(scrname)
                    self.points.append(scrpoints)
                else:
                    self.pen.append(scrname)
                    self.penpoints.append(-1 * scrpoints)

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
        <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
        <link href="https://unpkg.com/aos@2.3.1/dist/aos.css" rel="stylesheet">

        <link rel="stylesheet" href="../static/main.css" />
        <!-- <link rel="stylesheet" href="../static/css/main.css" /> -->
    </head>
    <body>
        <div class="root">
            <div class="container">
                <h1 data-aos="zoom-in">ParadoxSE</h1>
                <h3 data-aos="zoom-in">Vulnerability Analysis Report</h3>
                <hr data-aos="zoom-in" />
                <div data-aos="zoom-in" class="vulns">
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
        <script>
            AOS.init();
        </script>
    </body>
</html>
""")

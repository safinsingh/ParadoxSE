import os
import subprocess
import pwd
import grp


class Functions():
    def __init__(self):
        """Generate initial APT Cache for functions"""
        if useAPT:
            self.apt = apt.Cache()

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

        if os.path.exists(file):
            with open(file) as f:
                if string not in f.read():
                    return name, points

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

        try:
            self.apt[package].is_installed
        except:
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

        if user not in [entry.pw_name for entry in pwd.getpwall()]:
            return name, points

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
        if os.path.exists(file):
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

        if os.path.exists(file):
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

        with open(os.devnull, 'w') as FNULL:
            code = subprocess.call(
                command.split(), stdout=FNULL, stderr=subprocess.STDOUT)
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

        try:
            with open(os.devnull, 'w') as FNULL:
                code = subprocess.call(
                    command.split(), stdout=FNULL, stderr=subprocess.STDOUT)
        except:
            return name, points

    def update(self):
        """Loops through all checks in YAML configuration and writes updates to Score Report"""
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

        self.totalscore = sum(self.points) + sum(self.penpoints)

        print("Your updated score is: " + str(self.totalscore))

        if self.verbose:
            print("Checks Passed:\n" + '\n'.join(map(str, self.vulns)) + "\n")
            print("Checks Failed:\n" + '\n'.join(map(str, self.pen)))

        open(os.path.join(os.path.dirname(__file__),
                          "report/report.html"), "w").close()

        partials = {}

        for i in range(1, 7):
            with open(os.path.join(os.path.dirname(__file__), "report/partial/r" + str(i) + ".html"), "r") as f:
                partials["f"+str(i)] = f.read()

        with open(os.path.join(os.path.dirname(__file__), "report/report.html"), "a") as f:
            f.write(partials["f1"])

            f.write(str(sum(self.points) + sum(self.penpoints)))

            f.write(partials["f2"])

            for el in self.vulns:
                f.write("<li>" + el + "</li>")

            f.write(partials["f3"])

            for el in self.points:
                el = "+" + str(el)

                f.write("<li><scs>" + el + "</scs></li>")

            f.write(partials["f4"])

            for el in self.pen:
                f.write("<li>" + el + "</li>")

            f.write(partials["f5"])

            for el in self.penpoints:
                f.write("<li><fail>" + str(el) + "</fail></li>")

            f.write(partials["f6"])

        with open(os.path.join(os.path.dirname(__file__), "misc/oldscore"), "r") as f:
            oldscore = int(f.read())

            if self.totalscore > oldscore:
                self.notify("You gained points!")
            elif self.totalscore < oldscore:
                self.notify("You lost points!")

        with open(os.path.join(os.path.dirname(__file__), "misc/oldscore"), "w") as f:
            f.write(str(self.totalscore))

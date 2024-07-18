import subprocess, os

class Install:
    def __init__(self):
        pass

    def check_env(self):
        if not os.path.exists("/env"):
            subprocess.run(["python3", "-m", "venv", "env"])

    def source_env(self):
        if os.name == "nt":
            subprocess.run([".\\env\\bin\\Activate.ps1"], shell=True)
        else:
            subprocess.run(["source", "env/bin/activate"], shell=True)

    def install_requirements(self):
        self.source_env()
        installed_discord = False
        with open("requirements.txt", "r") as f:
            def check_requirement(requirement):
                check = subprocess.run(["pip", "show", requirement], capture_output=True)
                if "not found" in check.stderr.decode():
                    return False
                return True
            requirements = [requirement.split("==")[0].strip() for requirement in f.readlines()]

            for requirement in requirements:
                if "discord" not in requirement:
                    if not check_requirement(requirement):
                        subprocess.run(["pip", "install", requirement])
                else:
                    if installed_discord:
                        continue
                    installed_discord = True
                    subprocess.run(["pip", "install", "discord"])
                    subprocess.run(["pip", "uninstall", "discord.py", "-y"])
                    subprocess.run(["pip", "install", "discord.py==1.7.3"])

if __name__ == "__main__":
    install = Install()
    install.check_env()
    install.install_requirements()
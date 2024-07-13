import subprocess

def install_requirements():
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


install_requirements()
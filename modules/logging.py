from modules.colors import Colors

class Logging:
    def __init__(self):
        pass

    def Success(self, message):
        print("[{red}>{reset}] {message}".format(red=Colors.green, reset=Colors.white, message=message))
    
    def Error(self, message):
        print("[{red}>{reset}] {message}".format(red=Colors.red, reset=Colors.white, message=message))

    def Info(self, message):
        print("[{red}>{reset}] {message}".format(red=Colors.blue, reset=Colors.white, message=message))
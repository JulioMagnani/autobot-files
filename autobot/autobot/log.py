class Output(object):

    # def __init__(self, window):
    #     self.window = window

    def write(self, message):
        with open("templog.txt", "a+") as proc:
            proc.write(message)

    def read(self):
        with open("templog.txt", "r") as proc:
            result = proc.read()
            return result

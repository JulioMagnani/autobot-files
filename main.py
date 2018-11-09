import sys
from autobot import app


if __name__ == '__main__':
    application = app.App()
    sys.exit(application.run())

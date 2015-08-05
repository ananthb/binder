from flask.ext.script import Manager

from binder import create_app

MANAGER = Manager(create_app)
MANAGER.add_option('-c',
                   '--config',
                   dest='config',
                   required=False,
                   help='Path to configuration file')

if __name__ == "__main__":
    # And we're off!
    MANAGER.run()

import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join( os.path.dirname( __file__ ), 'config.ini'))
config = config[os.environ["GFG_ENV"]]
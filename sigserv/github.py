from github3 import login
from sigserv.config import config

gh = login(config['bot']['username'], config['bot']['password'])

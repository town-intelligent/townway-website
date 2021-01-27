#!/usr/bin/python3.5
encoding = "utf-8"

import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/ubuntu/townway-website")

from server import app as application
application.root_path = '/home/ubuntu/townway-website'
application.secret_key = '2ulidgoo'

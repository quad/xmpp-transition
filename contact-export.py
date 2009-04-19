#!/usr/bin/env python

import logging
import sys

from helpers import parse_options, login_xmpp

if __name__ == '__main__':
  username, password, remain = parse_options(sys.argv[1:])

  logging.info('Logging in...')
  client, roster = login_xmpp(username, password, 'Scraper')

  for key in roster.keys():
    name = roster.getItem(key)['name']

    if name:
      print "%s\t%s" % (key, name)
    else:
      print key

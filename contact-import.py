#!/usr/bin/env python

import fileinput
import logging
import sys

import xmpp

from helpers import parse_options, login_xmpp

def parse_contacts(input):
  return [(xmpp.protocol.JID(jid.strip()), name.strip())
          for jid, name in [line.split('\t') for line in input]]

if __name__ == '__main__':
  username, password, remain = parse_options(sys.argv[1:])
  contact_list = parse_contacts(fileinput.input(remain))

  logging.info('Logging in...')
  client, roster = login_xmpp(username, password, 'Scraper')

  # Add every contact under the "Imported" group.

  for jid, name in contact_list:
    logging.info("Importing %s under %s..." % (name, jid))
    roster.setItem(jid, name, groups = ['Imported'])
    roster.Subscribe(jid)

    client.Process(1)

  # Finish any last transactions.

  client.Process()
  client.disconnect()

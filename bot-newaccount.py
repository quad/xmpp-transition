#!/usr/bin/env python

import logging
import sys

import xmpp

from helpers import parse_options, login_xmpp

reply_header = "This is an automated message. PLEASE DO NOT REPLY."
reply_moved = "Scott's IM is now the same as his e-mail: scott@quadhome.com"
reply_new_server = """As an aside, the server you and he shared (jabber.org) has been unstable. Scott has started a new server for friends: @shadowpimps.net.

So, if you would like your IM name to be %s@shadowpimps.net, then give Scott an IM!""" 

if __name__ == '__main__':
  logging.basicConfig(level = logging.DEBUG)

  username, password, remain = parse_options(sys.argv[1:])

  logging.info('Logging in...')
  client, roster = login_xmpp(username, password, 'MovedBot')

  # Register callbacks.

  def cb_message(client, message):
    if message.getBody():   # Drop state changes.
      message_from = message.getFrom()
      reply = [reply_header, reply_moved]

      if message_from.getDomain() == 'jabber.org':
        reply.append(reply_new_server % message_from.getNode().split('@')[0])

      client.send(xmpp.Message(message.getFrom(), '\n\n'.join(reply)))

  client.RegisterHandler('message', cb_message)

  def cb_presence(client, presence):
    if presence.getType() == 'subscribe':
      logging.debug('Authorizing %s' % presence.getFrom())
      roster.Authorize(presence.getFrom())  # Eww, scoped variable.

  client.RegisterHandler('presence', cb_presence)

  # And now we wait...

  client.sendInitPresence()

  while client.Process():
    if not client.isConnected():
      logging.warn('Reconnecting.')
      client.reconnectedAndReauth()

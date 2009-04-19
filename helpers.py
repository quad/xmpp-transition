import getopt

import xmpp

def parse_options(args):
  opts, remain = getopt.getopt(args, None, ['username=', 'password='])

  opts_dict = dict(opts)

  return opts_dict['--username'], opts_dict['--password'], remain

def login_xmpp(username, password, resource = 'AutoBot'):
  jid = xmpp.protocol.JID(username)
  client = xmpp.Client(jid.domain, debug = None)

  assert client.connect() == 'tls'
  assert client.auth(jid.node, password, resource) in ['sasl', 'old_auth']

  return client, client.getRoster()

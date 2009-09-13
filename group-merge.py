#!/usr/bin/env python

import logging
import sys

from helpers import parse_options, login_xmpp

if __name__ == '__main__':
    username, password, (group_from, group_to) = parse_options(sys.argv[1:])

    logging.info('Logging in...')
    client, roster = login_xmpp(username, password, 'Merger')

    jids = [(jid, roster.getGroups(jid))
            for jid in roster.keys()
            if group_from in (roster.getGroups(jid) or [])]

    for jid, groups in jids:
        groups.remove(group_from)

        if group_to not in groups:
            groups.append(group_to)

        roster.setItem(jid, name=roster.getName(jid), groups=groups)

        print jid, '->', groups
        
    # Finish any last transactions.
    client.Process()
    client.disconnect()

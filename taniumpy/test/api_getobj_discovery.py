#!/usr/bin/env python
# -*- mode: Python; tab-width: 4; indent-tabs-mode: nil; -*-
# ex: set tabstop=4
# Please do not change the two lines above. See PEP 8, PEP 263.
import os
import sys

sys.dont_write_bytecode = True
my_file = os.path.abspath(__file__)
my_dir = os.path.dirname(my_file)
parent_dir = os.path.dirname(my_dir)
path_adds = [parent_dir]

for aa in path_adds:
    if aa not in sys.path:
        sys.path.append(aa)

import api

host = '172.16.31.128'
username = 'Tanium User'
password = 'T@n!um'

session = api.Session(host)
session.authenticate(username, password)

ots = dir(api)
skips = ['BaseType', 'Session', 'object_types', 'session']


def do(s):
    print '\n>>> '.join(s.splitlines())
    try:
        exec(s)
    except Exception as e:
        print "EXCEPTION: ", str(e).replace('\n', '')

print "# Generated by api_getobj_discovery.py"

for ot in ots:
    if ot.startswith('__') or ot in skips:
        continue

    if ot.endswith('List') and ot.replace('List', '') in ots:
        continue

    ot_vars = vars(getattr(api, ot)())
    ot_id = 'id' in ot_vars
    ot_name = 'name' in ot_vars
    ot_hash = 'hash' in ot_vars
    ot_list = ot + 'List' in ots

    print "## {}\n\n```".format(ot)

    do("""
# findall non list
a=api.{}()
r=session.find(a)
print r
""".format(ot))

    if ot_id:
        do("""
# find by id non list
a=api.{}()
a.id=1
r=session.find(a)
print r
""".format(ot))

    if ot_name:
        do("""
# find by name non list
a=api.{0}()
a.id=1
r1=session.find(a)
print r1
b=api.{0}()
b.name=r1.name
r2=session.find(b)
print r2
""".format(ot))

    if ot_hash:
        do("""
# find by hash non list
a=api.{0}()
a.id=1
r1=session.find(a)
print r1
b=api.{0}()
b.hash=r1.hash
r2=session.find(b)
print r2
""".format(ot))

    if ot_list:
        do("""
# findall list
a=api.{}List()
r=session.find(a)
print r
""".format(ot))

        if ot_id:
            do("""
# find by id in list
a=api.{0}()
a.id=1
b=api.{0}List()
b.append(a)
r=session.find(a)
print r
""".format(ot))

        if ot_name:
            do("""
# find by name in list
a=api.{0}()
a.id=1
r1=session.find(a)
print r1
b=api.{0}()
b.name=r1.name
c=api.{0}List()
c.append(b)
r2=session.find(c)
print r2
""".format(ot))

    print "```\n"

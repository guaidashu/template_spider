"""
author songjie
"""
from tool.lib.function import debug


def print_default():
    d = {'yy': '奕弈', 'google': 'Google'}

    debug("Value : %s" % d.setdefault('yy', "because of dream"))
    debug("Value : %s" % d.setdefault('google', '谷歌'))

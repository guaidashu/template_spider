"""
author songjie
"""
from tool_yy import Helper


class HelperInstance(Helper):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


def create_helper():
    helper = HelperInstance()
    helper.set_config('config.secure')
    helper.set_config('config.settings')
    return helper

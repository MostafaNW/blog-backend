import re

class Validator(object):
    """docstring for Validator."""

    def __init__(self):
        pass
    def v_sortBy(self, sortBy):
        match = re.search('(id|reads|likes|popularity)', sortBy)
        return match != None
    def v_direction(self, direction):
        match = re.search('(asc|desc)', direction)
        return match != None

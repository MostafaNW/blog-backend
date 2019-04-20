
class Post(object):
    """A user post"""

    def __init__(self, data):
        self.data = data
    def get_element(self, element='id'):
        return self.data[element]
    def __eq__(self, another):
        return another.get_element('id') == self.get_element('id')
    def __hash__(self):
        return hash(self.get_element('id'))

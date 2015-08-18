class State(object):
    def __init__(self, name):
        self.name = name
        self.edges = []

    def add_edge(self, edge):
        self.edges.append(edge)

    def __str__(self):
        return 'State({})'.format(self.name)


class Edge(object):
    def __init__(self, start, end, label):
        self.start = start
        self.end = end
        self.label = label

    def get_timeout(self):
        import re
        m = re.match('t(\d+)', self.label)
        if m:
            return m.groups()[0]
        else:
            return 0

    def __str__(self):
        return 'Edge({}->{}, {})'.format(self.start, self.end, self.label)

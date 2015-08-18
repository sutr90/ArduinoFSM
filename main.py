import collections
import pydot_ng as pydot
from fsmPygen import *
from fsmClasses import *

graph = pydot.graph_from_dot_file('data/graph2.gv')
dot_edges = graph.get_edges()


def parse_data(edges_p):
    states = {}
    edges = []

    for e in edges_p:
        s, d, l = e.get_source(), e.get_destination(), e.get_label()

        start = states[s] = states.get(s, State(s))
        end = states[d] = states.get(d, State(d))
        edge = Edge(start, end, l)

        start.add_edge(edge)
        edges.append(edge)

    return states.values(), edges


def generate_state_table(states, edges):
    d = collections.defaultdict(dict)
    en = set([e.label for e in edges])

    for s in states:
        for e in en:
            d[s][e] = s

    for e in edges:
        d[e.start][e.label] = e.end

    return d


def pretty(d, indent=0):
    for key, value in d.iteritems():
        print '\t' * indent + str(key) + '\t' * (indent + 1) + str(value)


def create_file(states, events, table):
    cfile = create_events(events) + "\n"
    cfile += create_states(states) + "\n"
    cfile += create_fsm_table(table) + "\n"

    cfile += 'unsigned long currentMillis, previousMillis = 0, interval;\n\n'

    cfile += create_poll() + "\n"

    cfile += create_actions(states) + "\n"
    cfile += create_eval_state(states) + "\n"
    cfile += create_setup(states[0]) + "\n"
    cfile += create_loop() + "\n"

    return cfile


def main():
    s, e = parse_data(dot_edges)

    t = generate_state_table(s, e)
    # pretty(t)

    print create_file(s, e, t)


if __name__ == '__main__':
    main()

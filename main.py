import collections
import pydot_ng as pydot
from fsmPygen import *
from fsmClasses import *

graph = pydot.graph_from_dot_file('data/graph1.gv')
edges = graph.get_edges()

# state prefix
sp = 'st_'
# event prefix
ep = 'evt_'
# null event
enull = ep + 'null'


def parse_data(dot_edges):
    states = {}

    for e in dot_edges:
        s, d, l = e.get_source(), e.get_destination(), e.get_label()

        start = states[s] = states.get(s, State(s))
        end = states[d] = states.get(d, State(d))

        start.add_edge(Edge(start, end, l))

    return states


def extract_state_names(edges_p):
    state_set = set()

    for e in edges_p:
        state_set.add(sp + e.get_source())
        state_set.add(sp + e.get_destination())

    return sorted(state_set)


def extract_event_names(edges_p):
    event_set = set()

    for e in edges_p:
        event_set.add(ep + e.get_label())

    event_set.add(enull)

    return sorted(event_set)


def generate_state_table(edges_p):
    events = extract_event_names(edges_p)
    states = extract_state_names(edges_p)

    d = collections.defaultdict(dict)

    for s in states:
        for e in events:
            d[s][e] = s

    for e in edges_p:
        d[sp + e.get_source()][ep + e.get_label()] = sp + e.get_destination()

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

    actions = [s[len(sp):] for s in states]

    cfile += create_actions(actions) + "\n"
    cfile += create_eval_state(actions, sp) + "\n"
    cfile += create_setup(states[0]) + "\n"
    cfile += create_loop() + "\n"

    return cfile


def main():
    s = extract_state_names(edges)
    # print(s)

    e = extract_event_names(edges)
    # print(e)

    t = generate_state_table(edges)
    # pretty(t)

    print create_file(s, e, t)


if __name__ == '__main__':
    main()

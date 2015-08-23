import collections
import pydot_ng as pydot
from fsmPygen import *
from fsmClasses import *

graph = pydot.graph_from_dot_file('data/ledScroll.gv')
dot_edges = graph.get_edges()
class_name = 'FsmTest'
cls_prefix = class_name + '::'


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


# def create_file(states, events, table):
#     cfile = create_events(events) + "\n"
#     cfile += create_states(states) + "\n"
#     cfile += create_fsm_table(table) + "\n"
#
#     cfile += 'unsigned long currentMillis, previousMillis = 0, interval;\n\n'
#
#     cfile += create_poll() + "\n"
#
#     cfile += create_actions(states) + "\n"
#     cfile += create_eval_state(states) + "\n"
#     cfile += create_setup(states[0]) + "\n"
#     cfile += create_loop() + "\n"
#
#     return cfile


def create_cpp_file(states, table):
    cpp_file = '#include "{}.hpp"\n\n'.format(class_name)
    cpp_file += create_fsm_table(table, cls_prefix) + '\n'
    cpp_file += create_poll(cls_prefix) + '\n'
    cpp_file += create_actions(cls_prefix, states) + '\n'
    cpp_file += create_eval_state(cls_prefix, states) + '\n'
    cpp_file += create_setup(cls_prefix, states[0]) + '\n'
    cpp_file += create_loop(cls_prefix) + '\n'
    return cpp_file


def create_hpp_file(events, states):
    hpp_file = 'class {}{{\n'.format(class_name)
    hpp_file += 'public:\n'
    hpp_file += '\t{}();\n'.format(class_name)
    hpp_file += '\tvoid loop();\n'
    hpp_file += 'private:\n'

    hpp_file += create_events(events) + '\n'
    hpp_file += create_states(states) + '\n'

    # -1 because it contains the evt_none which is not present in fsm table
    hpp_file += '\tstatic const State fsmTable[{}][{}];\n'.format(len(states), len(events)-1)
    hpp_file += '\tunsigned long currentMillis, previousMillis, interval;\n'
    hpp_file += '\tvoid pollEvents();\n'

    for s in states:
        hpp_file += "\tvoid action_{}();\n".format(s.name)

    hpp_file += '\tvoid evalState();\n'
    hpp_file += '};\n'
    return hpp_file


def main():
    s, e = parse_data(dot_edges)

    t = generate_state_table(s, e)

    with open('{}.cpp'.format(class_name), 'w') as f:
        f.write(create_cpp_file(s, t))

    with open('{}.hpp'.format(class_name), 'w') as f:
        f.write(create_hpp_file(e, s))

if __name__ == '__main__':
    main()

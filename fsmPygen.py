event_prefix = 'evt_'
state_prefix = 'st_'
event_none = 'none'


def create_events(events):
    event_names = set()

    for en in events:
        event_names.add(en.label)

    evt_str = 'typedef enum {'
    for e in sorted(event_names):
        evt_str += '{}{}, '.format(event_prefix, e)

    if event_none not in event_names:
        evt_str += '{}{}'.format(event_prefix, event_none)

    evt_str += '} Event;\n'
    evt_str += 'Event currentEvent, lastEvent;\n'
    return evt_str


def create_states(states):
    state_str = 'typedef enum {'
    for s in sorted(states, key=lambda x: x.name):
        state_str += '{}{}, '.format(state_prefix, s.name)

    state_str += '} State;\n'
    state_str += 'State currentState;\n'
    return state_str


def create_fsm_table(table):
    states = table.keys()
    events = table.values()[0].keys()
    col_width = max(max([len(s.name) for s in states]), max([len(e) for e in events]))
    col_width += 4  # length of prefix

    s_count = len(states)
    e_count = len(events)

    fsm_str = 'int fsmTable[{0}][{1}] = {{\n'.format(s_count, e_count)

    fsm_str += '\t/*'

    for e in sorted(events):
        fsm_str += '{:>{}}, '.format(event_prefix + e, col_width)

    fsm_str += '*/\n'
    for s in sorted(states, key=lambda x: x.name):
        fsm_str += '\t{ '
        for e in sorted(events):
            fsm_str += '{:>{}}, '.format(state_prefix + table[s][e].name, col_width)
        fsm_str += '}},/* {} */\n'.format(s.name)

    fsm_str += '};\n'

    return fsm_str


def create_poll():
    poll_str = 'void pollEvents() {\n'
    poll_str += '\tlastEvent = currentEvent;\n'
    poll_str += '\t/* TODO: update currentEvent */\n'
    poll_str += '\tcurrentEvent = {}{};\n'.format(event_prefix, event_none)
    poll_str += '}\n'
    return poll_str


def create_actions(states):
    actions_str = ""
    for s in states:
        actions_str += "void action_{}(){{\n".format(s.name)

        min_edge = min(s.edges, key=lambda (edge): edge.get_timeout())
        timeout = min_edge.get_timeout()

        if not timeout == 0:
            actions_str += '\tcurrentEvent = {}{};\n'.format(event_prefix, min_edge.label)
            actions_str += '\tinterval = {};\n'.format(timeout)

        actions_str += "\t/* TODO: add action for state {} */\n".format(s.name)
        actions_str += "}\n"
    return actions_str


def create_eval_state(states):
    eval_str = "void evalState(){\n"
    eval_str += "\tswitch(currentState){\n"

    for s in states:
        eval_str += "\t\tcase {}{}:\n".format(state_prefix, s.name)
        eval_str += "\t\t\taction_{}();\n".format(s.name)
        eval_str += "\t\t\tbreak;\n"

    eval_str += "\t}\n"
    eval_str += "}\n"

    return eval_str


def create_setup(start):
    setup_str = "void setup(){\n"
    setup_str += '\tinterval = 0;\n'
    setup_str += "\tcurrentState = {}{};\n".format(state_prefix, start.name)
    setup_str += '\tcurrentEvent = {}{};\n'.format(event_prefix, event_none)
    setup_str += "}\n"

    return setup_str


def create_loop():
    loop_str = "void loop() {\n"
    loop_str += "\tpollEvents();\n"
    loop_str += '\tcurrentMillis = millis();\n'

    loop_str += '\tif (currentMillis - previousMillis > interval) {\n'
    loop_str += '\t\tpreviousMillis = currentMillis;\n'

    loop_str += '\t\tif(currentEvent != {}{}){{\n'.format(event_prefix, event_none)
    loop_str += '\t\t\tcurrentState = (State) fsmTable[currentState][currentEvent];\n'
    loop_str += '\t\t}\n'

    loop_str += "\t\tevalState();\n"
    loop_str += "\t}\n}\n"

    return loop_str

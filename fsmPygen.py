def create_events(events):
    evt_str = "typedef enum {"
    for e in events:
        evt_str += "{}, ".format(e)

    evt_str += "} Event;\n"
    evt_str += "Event currentEvent, lastEvent;\n"
    return evt_str


def create_states(states):
    state_str = "typedef enum {"
    for s in states:
        state_str += "{}, ".format(s)

    state_str += "} State;\n"
    state_str += "State currentState;\n"
    return state_str


def create_fsm_table(table):
    states = sorted(table.keys())
    events = sorted(table.values()[0].keys())

    col_width = max([len(max(row.values(), key=len)) for row in table.values()])

    s_count = len(states)
    e_count = len(events)

    fsm_str = "int fsmTable[{0}][{1}] = {{\n".format(s_count, e_count)

    fsm_str += "\t/*"

    for e in events:
        fsm_str += "{:>{}}, ".format(e, col_width)

    fsm_str += "*/\n"
    for s in states:
        fsm_str += "\t{ "
        for e in events:
            fsm_str += "{:>{}}, ".format(table[s][e], col_width)
        fsm_str += "}},/* {} */\n".format(s)

    fsm_str += "};\n"

    return fsm_str


def create_poll():
    poll_str = 'void pollEvents() {\n'
    poll_str += '\tlastEvent = currentEvent;\n'
    poll_str += '\t/* TODO: update currentEvent */\n'
    poll_str += '}\n'
    return poll_str


def create_actions(states):
    # TODO actions for timed intervals need to set next interval and next action according to diagram
    # time on edge mean time for leaving the source state
    actions_str = ""
    for s in states:
        actions_str += "void action{}(){{\n".format(s)
        actions_str += "\t/* TODO: add action for state {} */\n".format(s)
        actions_str += "}\n"
    return actions_str


def create_eval_state(states, prefix):
    eval_str = "void evalState(){\n"
    eval_str += "\tswitch(currentState){\n"

    for s in states:
        eval_str += "\t\tcase {}:\n".format(prefix + s)
        eval_str += "\t\t\taction{}();\n".format(s)
        eval_str += "\t\t\tbreak;\n"

    eval_str += "\t}\n"
    eval_str += "}\n"

    return eval_str


def create_setup(start):
    setup_str = "void setup(){\n"
    setup_str += "\tcurrentState = {};\n".format(start)
    setup_str += "}\n"

    return setup_str


def create_loop():
    loop_str = "void loop() {\n"
    loop_str += "\tpollEvents();\n"
    loop_str += "\tif (lastEvent != currentEvent) {\n\t\tinterval = 0;\n\t}\n"
    loop_str += '\tcurrentMillis = millis();\n'

    loop_str += '\tif (currentMillis - previousMillis > interval) {\n'
    loop_str += '\t\tpreviousMillis = currentMillis;\n'
    loop_str += '\t\tcurrentState = (State) fsmTable[currentState][currentEvent];\n'

    loop_str += "\t\tevalState();\n"
    loop_str += "\t}\n}\n"

    return loop_str

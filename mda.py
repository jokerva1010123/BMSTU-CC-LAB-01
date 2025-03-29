from dfa import *
import os
class MDA:
    def __init__(self, dfa):
        self.states = dfa.states
        self.finalStates = set(x.name for x in dfa.finalStates)
        self.alphabet = dfa.alphabet
        self.startStatesSet = set(x.name for x in dfa.startStatesSet)
        self.inv = {}
    
    def show(self, name, a):
        gv_file = open(name+".gv", "w")
        gv_file.write("digraph G {\nrankdir = LR;\n")
        for x in a.keys():
            for char in self.alphabet:
                if a[x][char] != set():
                    for y in list(a[x][char]):
                        gv_file.write('\t"'+x + '"' + " -> " + '"' + y + '"[label="' + str(char) + '"];\n')
        gv_file.write("}\n")
        gv_file.close()
        os.system("dot -Tsvg " + name + ".gv -o " + name + ".svg")
        os.system("explorer " + name + ".svg")
    
    def mda_build(self, view = False):
        for state in self.states:
            if state.name not in self.inv:
                self.inv[state.name] = {char: set() for char in self.alphabet}
            if state.transitions == {}:
                    continue
            for char in self.alphabet:
                new_state = state.transitions[char]
                self.inv[state.name][char].add(new_state.name)
        f_inv = self.r(self.inv)
        f_d_inv = self.d(f_inv)
        s_inv = self.r(f_d_inv)
        s_d_inv = self.d(s_inv)
        if view:
            self.show('f_inv', f_inv)
            self.show("f_d_inv", f_d_inv)
            self.show('s_inv', s_inv)
        self.show('s_d_inv', s_d_inv)
        return s_d_inv, self.finalStates        
    
    def r(self, pre_transitions):
        inv_trac = {}
        current_states = self.startStatesSet
        new_startStatesSet = set()
        new_finalStatesSet = set()
        used_states = set()

        while current_states != set():
            next_states = set()
            print("*****")
            for state in current_states:
                used_states.add(state)
                print(f"* {state} added in used_states")
                print("*****")
                for char in self.alphabet:
                    if pre_transitions[state][char] == set():
                        continue
                    trans_state = list(pre_transitions[state][char])[0]
                    if trans_state not in inv_trac:
                        inv_trac[trans_state] = {char: set() for char in self.alphabet}
                    inv_trac[trans_state][char].add(state)
                    print("inv " + str(trans_state) + ' ' + char + ' ' + str(state))
                    print("Inverse:")
                    print(f"{state} <---{char}--- {trans_state}")

                    if trans_state not in used_states:
                        print(f"{trans_state} not in used_states yet")
                        next_states.add(trans_state)
                        print(f"{trans_state} added in next_states")

                if state in self.finalStates:
                    new_startStatesSet.add(state)
                if state in self.startStatesSet:
                    new_finalStatesSet.add(state)

                print("*****")

            current_states = next_states
        self.startStatesSet = new_startStatesSet
        self.finalStates = new_finalStatesSet

        return inv_trac
    
    def d(self, pre_transitions):
        inv_trac = {}
        dict_state = {}
        queue = set()
        used = set()
        queue.add(frozenset(self.startStatesSet))
        new_finalStatesSet = set()
        while queue != set():
            current_states = queue.pop()
            if current_states not in dict_state:
                dict_state[current_states] = len(dict_state)
            start = 's'+ str(dict_state[current_states])
            new_state = dict_state[current_states]
            if start not in inv_trac:
                inv_trac[start] = {char : set() for char in self.alphabet}
            for char in self.alphabet:
                new_set_state = set()
                for state in current_states:
                    if state not in pre_transitions or pre_transitions[state][char] == set():
                        continue
                    new_set_state |= pre_transitions[state][char]
                if new_set_state == set():
                    continue
                if frozenset(new_set_state) not in dict_state:
                    dict_state[frozenset(new_set_state)] = len(dict_state)
                end = 's'+str(dict_state[frozenset(new_set_state)])
                inv_trac[start][char].add(end)
                if new_set_state not in used:
                    queue.add(frozenset(new_set_state))
                    used.add(frozenset(new_set_state))
                if new_set_state.intersection(self.finalStates):
                    new_finalStatesSet.add(end)
        self.startStatesSet = set()
        self.startStatesSet.add("s0")
        self.finalStates = new_finalStatesSet
        return inv_trac
            

                    
        
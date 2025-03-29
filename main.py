from parsing import *
from nfa import *
from dfa import *
from mda import *

def modeling(alphabet, da, final_state, terminalString):
    current_state = 's0'
    print('Start with state s0.')
    for x in terminalString:
        print('Next character: ' + x)
        if x not in alphabet:
            return False
        next = list(da[current_state][x])
        if not len(next):
            return False
        current_state = next[0]
        print('Change to state ' + current_state)
    return current_state in final_state

regex = input("Enter regex: ")

print(">>> Выполним парсинг регулярного выражения <<<")
parser = Parser()
regularString = parser.parsing(regex)

print(">>> №1. Построим НКА по введённому регулярному выражению <<<")
nfa = NFA()
nfa.nfa_build(regularString)

print(">>> №2. По НКА построим эквивалентный ему ДКА <<<")
dfa = DFA(nfa)
task3 = dfa.dfa_build()

print(">>> №3. По ДКА построим эквивалентный ему КА с min кол-вом состояний -- алгоритм Бржозовского <<<")
# dfa.dfa_minimize()
# dfa.output_dfa()
view = input('View step (0/1)?\n0 - No\n1 - Yes\n')
mda = MDA(task3)
mini_da, final_state = mda.mda_build(view == '1')
print(">>> №4. Моделируем минимальный КА для входной цепочки <<<")
# # terminalString = "babb"
while 1:
    terminalString = input("Enter terminal string: ")
    print(modeling(task3.alphabet, mini_da, final_state, terminalString))
    con = input("\nContinue? (0/1)\n")
    if not con:
        break


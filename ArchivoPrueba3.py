# GENERATED FILE FOR COMPILER ArchivoPrueba3

class FiniteAutomaton(object): 
    # Models finite automatons


    def __init__(self, states, input_symbols, initial_state, acceptance_states, transition_function):
        # TODO: If space or tab (32, 9) comes and is in state zero, continue to next char
        self.states = states
        self.input_symbols = input_symbols
        self.initial_state = initial_state
        self.acceptance_states = acceptance_states.keys()
        self.acceptance_dictionary = acceptance_states
        self.transition_function = transition_function
        self.delimiters = ['9', '32']

    # Epsilon closure for NFAs
    def epsilon_closure(self, state):

        # Epsilon closure for NFAs
        # :param state: current state to validate
        # :return: set with all states

        # Create a new set, with state as its only member
        states = set()
        states.add(state)

        # Check if there are epsilon transitions to follow recursively
        if state.identifier1 == 'ε':
            if state.edge1 is not None:
                states |= self.epsilon_closure(state.edge1)
        if state.identifier2 == 'ε':
            if state.edge2 is not None:
                states |= self.epsilon_closure(state.edge2)

        # Returns the set of states
        return states

    # Generates a list with all tokens according to an input string
    def match_tokens(self, character_list):
        # Matches an input string and generates tokens
        # :param character_list: string to validate
        # :return: if string is valid + tokens

        # 0 is the initial state of the DFA
        current_state = 0

        tokens = []
        current_iterating_string = ''
        current_acceptance_string = ''
        blank_spaces = 0

        while len(character_list) > 0:
            # Iterates through all characters
            for character in character_list:

                # Updates the transitions and iterating string
                current_transitions = self.transition_function[current_state]
                current_iterating_string += chr(int(character))

                # If character is in the input symbols
                if character in self.input_symbols:
                    print('TRANSITION WITH', character)
                    # State on the transition list
                    attempted_state = current_transitions[self.input_symbols.index(character)]

                    # No transitions
                    if attempted_state is None:
                        print('THERE IS NO TRANSITION WITH', character, chr(int(character)))
                        if current_state != 0:
                            break
                        blank_spaces += 1
                        continue
                    # There is a transition
                    else:
                        current_state = attempted_state
                        if current_state in self.acceptance_states:
                            current_acceptance_string = current_iterating_string

                # Delimiters (space or tabs between tokens)
                elif character in self.delimiters and current_state == 0:
                    current_iterating_string = current_iterating_string[1::]
                    blank_spaces += 1
                    continue

                # Not a valid character
                else:
                    break

            # Tokens were found
            if len(current_acceptance_string) > 0:
                tokens.append(f"{current_acceptance_string}, {self.acceptance_dictionary[current_state]}")
                # Remove iterated characters
                character_list = character_list[len(current_acceptance_string) + blank_spaces::]

                # Restart token reading parameters
                current_iterating_string = ''
                current_acceptance_string = ''
                current_state = 0
                blank_spaces = 0
            # No tokens found
            else:
                tokens.append(f"TOKEN INVÁLIDO {''.join(character_list)}")
                return False, tokens

        if len(tokens) > 0:
            return True, tokens
        elif current_state in self.acceptance_states:
            return True, tokens

        tokens.append(f"TOKEN INVÁLIDO {''.join(character_list)}")
                

def read_file_characters():
    file = open('ArchivoPrueba3Entrada.txt', 'r', encoding='utf-8')
    characters = []
    for line in file:
        for character in line:
            characters.append(str(ord(character)))
    print(characters)

    return characters

automaton = FiniteAutomaton([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35], ['0', '100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '32', '34', '46', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '9', '90', '97', '98', '99'], 0, {1: 'null', 2: 'identificador', 3: 'identificador', 4: 'identificador', 5: 'identificador', 6: 'identificador', 7: 'espacioEnBlanco', 9: 'numero', 10: 'identificador', 11: 'identificador', 12: 'identificador', 13: '~si~', 14: 'identificador', 15: 'identificador', 16: 'cadena', 19: 'numeroHex', 20: 'identificador', 21: 'identificador', 22: 'identificador', 23: '~para~', 24: 'identificador', 25: 'identificador', 26: 'numeroDecimal', 27: 'identificador', 28: 'identificador', 29: '~null~', 30: 'identificador', 31: 'identificador', 32: 'identificador', 33: '~mientras~', 34: '~Mientras~', 35: '~MIENTRAS~'}, [[1, 2, 2, 3, 2, 2, 4, 2, 2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 2, 2, 6, 2, 2, 2, 7, 8, None, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 10, 10, 10, 10, 10, 10, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 11, 2, 2, 7, 2, 2, 2, 2], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 12, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 13, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 14, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 15, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 7, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 7, None, None, None, None], [None, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 16, None, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 17, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 18, 18, 18, 18, 18, 18, None, 19, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 2, 20, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 21, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 22, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 23, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 24, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 25, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, None, 19, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 27, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 28, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 29, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 30, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 26, 26, 26, 26, 26, 26, 26, 26, 26, 26, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, 2, 2, 2, 2, 2, 2, 2, 2, 31, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 32, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 33, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 34, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 35, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2], [None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, None, None, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, None, 2, 2, 2, 2]])
valid, tokens = automaton.match_tokens(read_file_characters())
print(tokens)
                
# GENERATED FILE FOR COMPILER ArchivoPrueba2
class FiniteAutomaton(object):
    # Models finite automatons

    def __init__(self):
        self.states = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
        self.input_symbols = ['100', '101', '102', '103', '104', '105', '106', '107', '108', '109', '110', '111', '112', '113', '114', '115', '116', '117', '118', '119', '120', '121', '122', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79', '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '9', '90', '97', '98', '99']
        self.initial_state = 0
        self.acceptance_states = [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12, 13, 14]
        self.acceptance_dictionary = {1: 'identificador', 2: 'identificador', 3: 'identificador', 4: 'numero', 5: 'identificador', 6: 'identificador', 7: 'tabulador', 8: 'identificador', 9: '~si~', 11: 'numeroHex', 12: 'numeroHex', 13: '~SI~', 14: '~para~'}
        self.transition_function = [[1, 1, 2, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5, 5, 1, 1, 6, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, None, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, None, 1, 1, 1, 1], [1, 1, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, None, 1, 1, 1, 1], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 10, 10, 10, 10, 10, 10, None, 11, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 1, 12, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, None, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 13, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, None, 1, 1, 1, 1], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 14, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, None, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, None, 1, 1, 1, 1], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, None, 11, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, None, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, None, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, None, 1, 1, 1, 1]]
        self.delimiters = ['9', '32', '13', '10']

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
                    # State on the transition list
                    attempted_state = current_transitions[self.input_symbols.index(character)]

                    # No transitions
                    if attempted_state is None:
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
                try:
                    tokens.append([current_acceptance_string, self.acceptance_dictionary[current_state]])
                except KeyError:
                    tokens.append("TOKEN INVÁLIDO " + ' ' + current_acceptance_string + ' ' + ''.join(character_list))
                # Remove iterated characters
                character_list = character_list[len(current_acceptance_string) + blank_spaces::]

                # Restart token reading parameters
                current_iterating_string = ''
                current_acceptance_string = ''
                current_state = 0
                blank_spaces = 0
            # No tokens found
            else:
                if len(character_list) > 0:
                    if character_list[0] in self.delimiters:
                        character_list.pop(0)
                else:
                    tokens.append("TOKEN INVÁLIDO " + ''.join(character_list))
                    return False, tokens

        if len(tokens) > 0:
            return True, tokens
        elif current_state in self.acceptance_states:
            return True, tokens

        tokens.append("TOKEN INVÁLIDO " + ''.join(character_list))
        return False, tokens


def read_file_characters(filename):
    file = open(filename, 'r', encoding='utf-8')
    characters = []
    for line in file:
        if line.replace(" ", "")[0:2] == '//':
            continue
        for character in line:
            characters.append(str(ord(character)))

    return characters


lexer = FiniteAutomaton()
file = input("Introduzca el nombre del archivo para probar>>")
try:
    valid, tokens = lexer.match_tokens(read_file_characters(file))
    for token in tokens:
        print(token)
except FileNotFoundError:
    print("Archivo no encontrado, revise que el nombre sea correcto y que incluya su extension")
                
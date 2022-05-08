# encoding utf-8
import os
from lexer_backend import direct_dfa_construction
from os import path, remove

class Compiler:
    def __init__(self):
        self.reserved_definition_words = ['COMPILER', 'CHARACTERS', 'KEYWORDS', 'TOKENS', 'PRODUCTIONS', 'IGNORE', 'END']
        self.characters = {}
        self.name = ''
        self.keywords = {}
        self.tokens = {}
        self.has_errors = False
        self.lexer = None

    def print_error(self, line, message):
        print(f'[ERROR, LINE {line}] {message}')
        self.has_errors = True

    def check_element_compatibility(self, element, line, keyword):
        if '=' not in element:
            self.print_error(line, f"'=' sign not present in {keyword} definition")
            return False
        elif '.' not in element[-1]:
            self.print_error(line, "'.' not present at line end")
            return False
        return True


    def handle_keyword(self, keyword_list, data):
        keyword = keyword_list[0]
        # print('handling... :)', keyword)

        errors = []
        if keyword == 'COMPILER':
            if len(keyword_list) == 2:
                self.name = keyword_list[1]
            else:
                self.print_error(data.pop(), "Invalid definition in COMPILER")
            pass
        elif keyword == 'CHARACTERS':

            for element in data:
                element_characters = []
                line = element.pop()
                if not self.check_element_compatibility(element, line, 'CHARACTER'):
                    continue
                identifier = element.pop(0)

                # Pops the equal sign
                element.pop(0)

                addition = True
                prev_expression = ''

                while len(element) > 0:
                    current_expression = element.pop(0)

                    if current_expression == '-':
                        addition = False
                    elif current_expression == '+':
                        addition = True

                    if len(element) == 0:
                        # Deletes the final point
                        current_expression = current_expression[0:len(current_expression) - 1]

                    if current_expression[0] == '"' and current_expression.count('"') == 2:
                        current_definition = []
                        for char in current_expression[0: len(current_expression) - 1].replace('"', ""):
                            current_definition.append(str(ord(char)))
                        if addition:
                            element_characters += current_definition
                        else:
                            element_characters -= current_definition

                    elif current_expression in list(self.characters.keys()):
                        if addition:
                            element_characters += self.characters[current_expression]
                        else:
                            element_characters -= self.characters[current_expression]
                    elif 'CHR' in current_expression:
                        if prev_expression == '..':
                            start = int(element_characters[-1]) + 1
                            stop_inclusive = int(current_expression.replace('CHR(', '').replace(')', '')) + 1
                            for i in range(start, stop_inclusive):
                                element_characters += [str(i)]
                        elif addition:
                            element_characters += [current_expression.replace('CHR(', '').replace(')', '')]
                        else:
                            element_characters -= [current_expression.replace('CHR(', '').replace(')', '')]

                    # Removes duplicate characters
                    element_characters = list(set(element_characters))
                    element_characters.sort()

                    self.characters[identifier] = element_characters
                    prev_expression = current_expression


        elif keyword == 'KEYWORDS':
            for element in data:
                line = element.pop()

                self.check_element_compatibility(element, line, 'KEYWORD')

                if len(element) == 3:
                    identifier, equal, definition = element
                    if definition.count('"') % 2 != 0 or definition.count('"') == 0:
                        self.print_error(line, '" characters do not match a keyword definition')

                    definition = definition[0: len(definition) - 1].replace('"', "")
                    character_list = []
                    for char in definition:
                        character_list.append(str(ord(char)))

                    definition = f"({'.'.join(character_list)}).#~[{identifier}]~"

                    self.keywords[identifier] = definition
                else:
                    self.print_error(line, 'Invalid KEYWORD definition')

        elif keyword == 'TOKENS':
            for element in data:
                line = element.pop()
                self.check_element_compatibility(element, line, 'TOKEN')

                if 'EXCEPT' in element and 'KEYWORDS.' in element:
                    element.pop()
                    element.pop()
                    element[-1] = element[-1] + '.'
                if len(element) > 3:
                    concatenated_element = []
                    for i in range(2, len(element)):
                        current_element = element.pop()
                        concatenated_element.insert(0, current_element)
                    concatenated_element = '.'.join(concatenated_element)
                    element.append(concatenated_element)

                if len(element) == 3:
                    identifier, equal, definition = element
                    definition = definition[0: len(definition) - 1]
                    keys_present = True
                    current_accepted_key = ''

                    while keys_present:
                        for key in self.characters.keys():
                            if key in definition:
                                if len(current_accepted_key) < len(key):
                                    current_accepted_key = key
                        if len(current_accepted_key) > 0:
                            definition = definition.replace(current_accepted_key, f"({'|'.join(self.characters[current_accepted_key])})").replace('{', '(').replace('}', ')*').replace(')(', ').(').replace('*(', '*.(').replace('*(', '*.(')
                            current_accepted_key = ''
                        else:
                            break

                    while '"' in definition:
                        first_index = definition.find('"')
                        definition = definition.replace('"', '', 1)
                        second_index = definition.find('"')
                        definition = definition.replace('"', '', 1)

                        if second_index == -1:
                            self.print_error(line, 'Missing quotation on TOKEN definition')
                        else:

                            character_list = []
                            for character in definition[first_index:second_index]:
                                character_list.append(str(ord(character)))

                            definition = (definition[:first_index] + f"({'.'.join(character_list)})" + definition[second_index:]).replace('*(', '*.(').replace(')(', ').(')

                    definition = f'({definition}).#[{identifier}]'
                    self.tokens[identifier] = definition

        elif keyword == 'PRODUCTIONS':
            # Doing this on the third project
            pass

        elif keyword == 'END':
            # Generates the output file
            final_regexp = ''
            final_character_list = []

            constructions = list(self.keywords.values()) + list(self.tokens.values())
            for construction in constructions:
                final_regexp += f'{construction}|'

            if final_regexp[-1] == '|':
                final_regexp = final_regexp[0: len(final_regexp) - 1]

            if not self.has_errors:
                automaton = direct_dfa_construction(final_regexp)


                file_content = f"""# GENERATED FILE FOR COMPILER {self.name}
class FiniteAutomaton(object):
    # Models finite automatons

    def __init__(self):
        self.states = {automaton.states}
        self.input_symbols = {automaton.input_symbols}
        self.initial_state = {automaton.initial_state}
        self.acceptance_states = {list(automaton.acceptance_dictionary.keys())}
        self.acceptance_dictionary = {automaton.acceptance_dictionary}
        self.transition_function = {automaton.transition_function}
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
                """

                generate_lexer_file(f'{self.name}.py', file_content)
                self.lexer = automaton

            else:
                raise Exception("COCO File Exception: could not build compiler, check logs")

        return errors

    def get_lexer_tokens(self, filename):
        valid, tokens = self.lexer.match_tokens(read_file_characters(filename))
        for token in tokens:
            print(token)


def add_character_spacing(line, character):
    found_index = 0
    while found_index != -1:
        found_index = line.find(character, found_index)
        if line[0:found_index].count('"') % 2 == 0:
            line = line.replace(character, f' {character} ')
        break
    return line


def read_file(filename, compiler):
    with open(filename, encoding='utf-8') as file:
        lines = file.readlines()
    clean_lines = []
    character_mode = False

    # Removes leading + trailing whitespaces and removes \n
    for line in lines:

        if ['CHARACTERS'] == line.split():
            character_mode = True
        elif ['KEYWORDS'] == line.split() or ['TOKENS'] == line.split():
            character_mode = False
        if '+' in line and character_mode:
            line = add_character_spacing(line, '+')
        if '-' in line and character_mode:
            line = add_character_spacing(line, '-')

        line = line.strip().rstrip('\n').replace('=', ' = ', 1).replace('..', ' .. ').split()
        clean_lines.append(line)

    # We can now work with the clean lines
    second_pointer = 0
    data = []
    errors = []

    i = 0

    while i < len(clean_lines):
        if len(clean_lines[i]) <= 0:
            i += 1
            continue


        # Compiler finds a keyword
        if clean_lines[i][0] in compiler.reserved_definition_words:
            current_keyword = clean_lines[i]
            second_pointer = i + 1
            if current_keyword[0] != 'END':
                try:
                    while True:
                        if len(clean_lines[second_pointer]) == 0:
                            second_pointer += 1
                            continue
                        if clean_lines[second_pointer][0] in compiler.reserved_definition_words:
                            break
                        # Reference to the line to handle errors
                        data.append(clean_lines[second_pointer] + [second_pointer + 1])
                        second_pointer += 1
                except IndexError:
                    print(f'[LINE {len(clean_lines)}] Missing END statement!')
            if len(data) == 0:
                data.append(i + 1)
            i = second_pointer
            compiler.handle_keyword(current_keyword, data)

            data = []
        # Not a keyword
        else:
            i += 1


def generate_lexer_file(filename, file_content):
    if path.exists(filename):
        os.remove(filename)
    file = open(filename, "x", encoding='utf-8')
    file.write(file_content)


def read_file_characters(filename):
    file = open(filename, 'r', encoding='utf-8')
    characters = []
    for line in file:
        if line.replace(" ", "")[0:2] == '//':
            continue
        for character in line:
            characters.append(str(ord(character)))

    return characters

# TODO: Check errors

compiler = Compiler()
# Generates Lexer
read_file('ArchivoPrueba3.atg', compiler)
# encoding utf-8
from main import *


def print_error(line, message):
    print(f'[ERROR, LINE {line}] {message}')

class Compiler:
    def __init__(self):
        self.reserved_definition_words = ['COMPILER', 'CHARACTERS', 'KEYWORDS', 'TOKENS', 'PRODUCTIONS', 'IGNORE', 'END']
        self.characters = {}
        self.name = ''
        self.keywords = {}
        self.tokens = {}
        self.errors = []

    def check_element_compatibility(self, element, line, keyword):
        if '=' not in element:
            print_error(line, f"'=' sign not present in {keyword} definition")
        elif '.' not in element[-1]:
            print_error(line, "'.' not present at line end")


    def handle_keyword(self, keyword_list, data):
        # TODO: ADD ERROR LINE
        keyword = keyword_list[0]
        print('handling... :)', keyword)

        errors = []
        if keyword == 'COMPILER':
            if len(keyword_list) == 2:
                self.name = keyword_list[1]
            else:
                print_error(data.pop(), "Invalid definition in COMPILER")
            pass
        elif keyword == 'CHARACTERS':

            for element in data:
                line = element.pop()
                self.check_element_compatibility(element, line, 'CHARACTER')

                if len(element) == 3:
                    identifier, equal, definition = element
                    character_list = []

                    for char in definition[0: len(definition) - 1].replace('"', ""):
                        character_list.append(str(ord(char)))

                    definition = f"({'|'.join(character_list)})"
                    self.characters[identifier] = definition

            print('CHARACTERSSSS', self.characters)


        elif keyword == 'KEYWORDS':
            for element in data:
                line = element.pop()

                self.check_element_compatibility(element, line, 'KEYWORD')

                if len(element) == 3:
                    identifier, equal, definition = element
                    definition = definition[0: len(definition) - 1].replace('"', "")
                    character_list = []
                    for char in definition:
                        character_list.append(str(ord(char)))

                    definition = f"({'.'.join(character_list)}).#~[{identifier}]~"

                    self.keywords[identifier] = definition

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
                        concatenated_element.insert(0, element.pop())
                    concatenated_element = '.'.join(concatenated_element)
                    element.append(concatenated_element)

                if len(element) == 3:
                    identifier, equal, definition = element
                    definition = definition[0: len(definition) - 1].replace('"', "")
                    for key in self.characters.keys():
                        if key in definition:
                            definition = definition.replace(key, self.characters[key]).replace('{', '(').replace('}', ')*').replace(')(', ').(').replace('*(', '*.(').replace('*(', '*.(')

                    definition = f'({definition}).#[{identifier}]'
                    self.tokens[identifier] = definition

        elif keyword == 'PRODUCTIONS':
            # Doing this on the third project
            pass

        elif keyword == 'END':
            final_regexp = ''
            constructions = list(self.keywords.values()) + list(self.tokens.values())
            for construction in constructions:
                final_regexp += f'{construction}|'

            if final_regexp[-1] == '|':
                final_regexp = final_regexp[0: len(final_regexp) - 1]

            automaton = direct_dfa_construction(final_regexp)
            valid, tokens = automaton.match_tokens(read_file_characters())
            print(tokens)

            pass

        return errors


def read_file(filename):
    compiler = Compiler()
    with open(filename, encoding='utf-8') as file:
        lines = file.readlines()
    clean_lines = []

    # Removes leading + trailing whitespaces and removes \n
    for line in lines:
        line = line.strip().rstrip('\n').replace('=', ' = ', 1).split()

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





# TODO: Make automaton file
# TODO: make edge cases solvable
# TODO: Check errors
read_file('ArchivoPrueba1.atg')
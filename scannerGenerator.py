# encoding utf-8
from main import *



class Compiler:
    def __init__(self):
        self.reserved_definition_words = ['COMPILER', 'CHARACTERS', 'KEYWORDS', 'TOKENS', 'PRODUCTIONS', 'IGNORE', 'END']
        self.characters = {}
        self.name = ''
        self.keywords = {}
        self.tokens = {}
        self.has_errors = False

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
        print('handling... :)', keyword)

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
                print('handling element', element)
                line = element.pop()
                if not self.check_element_compatibility(element, line, 'CHARACTER'):
                    continue
                identifier = element.pop(0)

                # Pops the equal sign
                element.pop(0)

                addition = True

                while len(element) > 0:
                    current_expression = element.pop(0)
                    print("CURRENT EXPRESSION", current_expression)

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
                        if addition:
                            element_characters += [current_expression.replace('CHR(', '').replace(')', '')]
                        else:
                            element_characters -= [current_expression.replace('CHR(', '').replace(')', '')]

                    # Removes duplicate characters
                    element_characters = list(set(element_characters))
                    element_characters.sort()

                    self.characters[identifier] = element_characters

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
                else:
                    self.print_error(line, 'Invalid KEYWORD definition')

        elif keyword == 'TOKENS':
            for element in data:
                print('TOKEN ELEMENT', element)
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
                        print(first_index, second_index, "INDICES")

                        if second_index == -1:
                            self.print_error(line, 'Missing quotation on TOKEN definition')
                        else:

                            print(definition[:first_index])
                            print(definition[second_index:], "WOW")
                            print(definition[first_index:second_index])
                            character_list = []
                            for character in definition[first_index:second_index]:
                                character_list.append(str(ord(character)))

                            definition = (definition[:first_index] + f"({'.'.join(character_list)})" + definition[second_index:]).replace('*(', '*.(').replace(')(', ').(')
                            print("REPLACED DEFINITION", definition)
                        break

                    definition = f'({definition}).#[{identifier}]'
                    print('setting definition as', definition)
                    self.tokens[identifier] = definition

                    print(definition, ' THE DEFINITION')

        elif keyword == 'PRODUCTIONS':
            # Doing this on the third project
            pass

        elif keyword == 'END':
            final_regexp = ''
            final_character_list = []

            constructions = list(self.keywords.values()) + list(self.tokens.values())
            for construction in constructions:
                final_regexp += f'{construction}|'

            if final_regexp[-1] == '|':
                final_regexp = final_regexp[0: len(final_regexp) - 1]

            print("FINAL REGEX", final_regexp)
            if not self.has_errors:
                automaton = direct_dfa_construction(final_regexp)
                valid, tokens = automaton.match_tokens(read_file_characters())
                print(tokens)
            else:
                raise Exception("COCO File Exception: could not build compiler, check logs")

            pass

        return errors


def add_character_spacing(line, character):
    found_index = 0
    while found_index != -1:
        found_index = line.find(character, found_index)
        print(found_index)
        if line[0:found_index].count('"') % 2 == 0:
            line = line[:found_index] + f' {character} ' + line[found_index + 1:]
        if found_index == -1:
            break
        found_index += 2

def read_file(filename):
    compiler = Compiler()
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
            add_character_spacing(line, '+')
        if '-' in line and character_mode:
            add_character_spacing(line, '-')
        if '..' in line and character_mode:
            add_character_spacing(line, '..')

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
read_file('ArchivoPrueba3.atg')

KEYWORD_IDENTIFIER = '~'

def infix_to_postfix(infix):
    """
    Generates a postfix expression from an infix one
    Based on: https://github.com/niemaattarian/Thompsons-Construction-on-NFAs/blob/master/Project.py
    Modified to take strings as characters
    :param infix: infix
    :return: postfix
    """
    # Precedence of operators (higher = higher priority)
    operators = {'*': 4, '+': 3, '.': 2, '|': 1}
    ending_strings = ['*', '+', '.', '|', '(', ')']

    postfix, stack = [], []
    character_index = -1

    # We iterate through all characters
    for character in infix:
        character_index += 1
        try:
            character = infix[character_index]
        except IndexError:
            character = character
            break

        if character == '(':
            stack.append(character)

        # Parenthesis check
        elif character == ')':
            while stack[-1] != '(':
                postfix.append(stack.pop())
            stack.pop()  # Removal of the opening bracket
        # Determine whether the character is in the 'operators' dictionary
        elif character in operators:
            while stack and operators.get(character, 0) <= operators.get(stack[-1], 0):
                postfix.append(stack.pop())
            stack.append(character)  # We check for operator precedence
        else:
            concat = character
            next_character = '.'
            if character_index < len(infix) - 1:
                next_character = infix[character_index + 1]
            while next_character not in ending_strings and len(infix) - 1 > character_index:
                character_index += 1
                next_character = infix[character_index]
                if next_character in ending_strings:
                    character_index -= 1
                    break
                concat += next_character

            # Character is appended to postfix
            postfix.append(concat)

    # We append to the postfix the ordered stack
    while stack:
        postfix.append(stack.pop())

    # returns postfix argument
    return postfix


class Node(object):
    """
    Node superclass
    """
    def __init__(self, identifier1=None, identifier2=None, edge1=None, edge2=None):
        self.identifier1 = identifier1
        self.identifier2 = identifier2
        self.edge1 = edge1
        self.edge2 = edge2


class DirectConstructionNode(Node):
    """
    Nodes for direct construction
    """
    def __init__(self, character=None, first_position=None, last_position=None):
        super().__init__()
        self.character = character
        self.nullable = character == '*' or character == '?' or character == '??'
        self.first_position = first_position
        self.last_position = last_position

    def update_node_positions(self):
        self.first_position = self.calculate_first_position(self.first_position)
        self.last_position = self.calculate_last_position(self.last_position)

    def calculate_first_position(self, first_position):
        if first_position is not None:
            return first_position

        # OR
        if self.character == '|':
            return self.edge1.first_position | self.edge2.first_position
        # AND
        elif self.character == '.':
            if self.edge1.nullable:
                return self.edge1.first_position | self.edge2.first_position
            else:
                return self.edge1.first_position
        # KLEENE, POSITIVE CLOSURE, QUESTION MARK
        else:
            # Note that we use edge 2 since edge 1 is empty
            return self.edge2.first_position

    def calculate_last_position(self, last_position):
        if last_position is not None:
            return last_position
        # OR
        if self.character == '|':
            return self.edge1.last_position | self.edge2.last_position
        # AND
        elif self.character == '.':
            if self.edge2.nullable:
                return self.edge1.last_position | self.edge2.last_position
            else:
                return self.edge2.last_position
        # KLEENE, POSITIVE CLOSURE, QUESTION MARK
        else:
            # Note that we use edge 2 since edge 1 is empty
            return self.edge2.last_position


def postfix_to_tree(postfix):
    node_stack = []
    operators = ['*', '+', '.', '|', '?']
    single_operators = ['*', '+', '?']
    character_index = 1
    characters = set([])
    acceptance_states = {}
    next_pos_dict = {}

    while len(postfix) > 0:
        # First item of the stack
        current_character = postfix.pop(0)

        # Operators
        if current_character in operators:
            new_node = DirectConstructionNode(character=current_character)
            if current_character in single_operators:
                new_node.edge2 = node_stack.pop()
                node_stack.append(new_node)
            else:
                new_node.edge2 = node_stack.pop()
                new_node.edge1 = node_stack.pop()
                node_stack.append(new_node)
        # Normal characters
        else:
            new_node = DirectConstructionNode(character=current_character)
            if current_character != '??':
                new_node.first_position = {character_index}
                new_node.last_position = {character_index}
            else:
                new_node.first_position = set([])
                new_node.last_position = set([])
            next_pos_dict[(character_index, current_character)] = set([])

            if '#' in current_character:
                acceptance_states[character_index] = current_character.replace('[', '').replace(']', '').replace('#', '')
            character_index += 1
            node_stack.append(new_node)

            if '#' not in current_character:
                characters |= {current_character}

        # First position, next position, last position
        new_node.update_node_positions()

        # Get the keys according to index
        next_pos_keys = list(next_pos_dict.keys())

        if current_character == '.':
            for last_pos in new_node.edge1.last_position:
                next_pos_dict[next_pos_keys[last_pos - 1]] |= new_node.edge2.first_position
        elif current_character == '*' or current_character == '+':
            for last_pos in new_node.edge2.last_position:
                next_pos_dict[next_pos_keys[last_pos - 1]] |= new_node.edge2.first_position

    return node_stack[0], next_pos_dict, sorted(characters), acceptance_states


class FiniteAutomaton(object):
    """
    Models finite automatons
    """

    def __init__(self, states, input_symbols, initial_state, acceptance_states, transition_function):
        self.states = states
        self.input_symbols = input_symbols
        self.initial_state = initial_state
        self.acceptance_states = acceptance_states.keys()
        self.acceptance_dictionary = acceptance_states
        self.transition_function = transition_function
        self.delimiters = ['9', '32', '13', '10']

    # Generates a list with all tokens according to an input string
    def match_tokens(self, character_list):
        """
        Matches an input string and generates tokens
        :param character_list: string to validate
        :return: if string is valid + tokens
        """
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
                        # Non tokens
                        if (current_state != 0 or character not in self.delimiters) and len(current_acceptance_string) == 0:
                            tokens.append(['INVALID', current_iterating_string])
                            character_list = character_list[len(current_iterating_string)::]
                            current_iterating_string = ''
                            break
                        # Delimiter that might be in the alphabet
                        elif current_state != 0:
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
                    tokens.append("TOKEN INV??LIDO " + ' ' + current_acceptance_string + ' ' + ''.join(character_list))
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
                    tokens.append("TOKEN INV??LIDO " + ''.join(character_list))
                    return False, tokens

        if len(tokens) > 0:
            return True, tokens
        elif current_state in self.acceptance_states:
            return True, tokens

        tokens.append("TOKEN INV??LIDO " + ''.join(character_list))
        return False, tokens


def build_dfa(syntactic_tree, next_pos_dict, symbols, acceptance_indexes):

    next_position_keys = list(next_pos_dict.keys())

    # Initial state is the first position of the root tree
    states = [syntactic_tree.first_position]
    all_states = [syntactic_tree.first_position]

    automaton_states = [0]
    acceptance_states = {}
    transition_function = []

    for index in states[0]:
        if index in list(acceptance_indexes.keys()):
            if 0 not in list(acceptance_states.keys()) or f"{KEYWORD_IDENTIFIER}" in acceptance_indexes[index]:
                acceptance_states[0] = acceptance_indexes[index]

    while len(states) > 0:
        row_transitions = []
        checking_state = states.pop(0)
        for character in symbols:
            building_state = set([])
            for index in checking_state:
                if (index, character) in next_position_keys:
                    building_state |= next_pos_dict[(index, character)]
            if len(building_state) == 0:
                row_transitions.append(None)
            elif building_state in all_states:
                row_transitions.append(all_states.index(building_state))
            else:
                states.append(building_state)
                all_states.append(building_state)
                state_number = len(all_states) - 1
                automaton_states.append(state_number)
                row_transitions.append(state_number)

            for index in building_state:
                if index in list(acceptance_indexes.keys()):
                    if all_states.index(building_state) not in list(acceptance_states.keys()) or f"{KEYWORD_IDENTIFIER}" in acceptance_indexes[index]:
                        acceptance_states[all_states.index(building_state)] = acceptance_indexes[index]
        transition_function.append(row_transitions)
    automaton = FiniteAutomaton(automaton_states, symbols, 0, acceptance_states, transition_function)

    return automaton


def direct_dfa_construction(regular_expression):
    postfix_expression = infix_to_postfix(f'{regular_expression}')
    tree, next_position, symbols, acceptance_states = postfix_to_tree(postfix_expression)
    return build_dfa(tree, next_position, symbols, acceptance_states)

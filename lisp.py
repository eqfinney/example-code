#
# Lisp Parser
# Author: Emily Quinn Finney
# This code is supposed to take Lisp code and turn it into an AST.
# I had to look up what an AST is. It's an "Abstract Syntax Tree".
# I had to look up what an Abstract Syntax Tree is, too.
#

def parse_lisp(example_lisp):
    """ This function takes a string and turns it into an abstract syntax tree.
        Input: example_lisp, a string containing lisp code
        Output: a list containing lists in a structured order (aka, an AST)
    """
    # initialize empty objects
    # word denotes the current word, separating by parentheses and whitespace
    # current_list is the abstract syntax tree
    word = ''
    current_list = []

    # base case: empty string
    # recursive case: involves parentheses
    pos = 0

    while pos != len(example_lisp):
        char = example_lisp[pos]

        # test to see if the character is finishing a branch of the AST
        # if it is, return the results
        if (char == ')'):
            if word != '':
                current_list.append(word)
            return current_list

        # test to see if the character is starting a branch of the AST
        # if it is, recurse over the remaining AST
        elif char == '(':
            new_list = parse_lisp(example_lisp[(pos+1):])
            current_list.append(new_list)
            # have to update the pointer by the length of the string
            # up until the correct right paren
            # which means you have to find the correct right paren
            paren_pos = find_correct_right_paren(example_lisp[(pos+1):])
            # add the length of the string, plus two for the
            # left paren and right paren denoting the branch
            pos = pos + paren_pos + 2
            
        # test to see if the character is finishing a word
        # if it is, add the word to the current list
        elif char == ' ':
            if word != '':
                current_list.append(word)
            word = ''
            pos = pos + 1

        # otherwise, add the character to the current word
        else:
            word = word + char
            pos = pos + 1

    # make sure we add the final word, if current_list has not been updated
    if word != '':
        current_list.append(word)

    return current_list

def find_correct_right_paren(paren_string):
    """ Finds the position of the corresponding right parenthesis
        Input: paren_string, the string for which we want the right paren
               note: the left paren has already been removed from
               paren_string and counted
        Output: the position of the corresponding right paren
    """
    # note: the left paren has been counted already
    nleftparen = 1
    nrightparen = 0

    for pos, char in enumerate(paren_string):
        
        # count the number of left parens
        if char == '(':
            nleftparen = nleftparen + 1

        # count the number of right parens
        elif char == ')':
            nrightparen = nrightparen + 1

        # return the correct position, if they're equal
        if nleftparen == nrightparen:
            return pos

    # raise an error if they are never equal
    raise ValueError("Error: There is no matching right paren")


"""
TEST CASES
This is for my own benefit.
'()' should return [[]]
'+ 1 2' should return ['+', '1', '2']
'+ (+ 3 5) (+ 2 4)' should return ['+', ['+', '3', '5'], ['+', '2', '4']]
'' should return []
'+ (+ 1 (+ 1 1))' should return ['+', ['+', '1', ['+', '1', '1']]]
'+ (+ 4 6) 7' should return ['+', ['+', '4', '6'], '7']
'(+ 1 2)' should return [['+', '1', '2']]
"""

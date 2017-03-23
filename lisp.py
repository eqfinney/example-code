#
# Lisp Parser
# Author: Emily Quinn Finney
# This code is supposed to take Lisp code and turn it into an AST.
# I had to look up what an AST is. It's an "Abstract Syntax Tree".
# I had to look up what an Abstract Syntax Tree is, too.
#

# parse it character by character I suppose
# if there's not whitespace or a parenthesis, save as a character
# if there's whitespace, it's a new character
# if there's a parenthesis, start a new list and the next character goes into it

def parse_lisp(example_lisp):
    """ This function takes a string and turns it into an abstract syntax tree.
        Input: example_lisp, a string containing lisp code
        Output: a list containing lists in a structured order (aka, an AST)
    """
    # initialize empty objects
    # n counts all characters in the input string
    # word denotes the current word, separating by parentheses and whitespace
    # newobj is the abstract syntax tree
    n = 0
    nleftparen = 0
    nrightparen = 0
    word = ''
    newobj = []
    # loop through all characters in the input string
    for n in range(len(example_lisp)+1):
        print(n)
        print(newobj)
        # test to see if the input string is empty
        # if it is, return the object
        if n == len(example_lisp):
            if word != '':
                newobj.append(word)
                word = ''
            return newobj
        else: 
            char = example_lisp[n]
            # test to see if the character is ending a branch of the AST
            # if it does, add the current word to the AST and return the tree
            # the "return to the tree" is the hard part of this apparently
            if char == ')':
                newobj.append(word)
                return newobj
            # test to see if the character is whitespace
            # if it is, add current word to the AST and move on to next character
            elif char == ' ':
                newobj.append(word)
                word = ''
                n = n+1
            # test to see if the character is starting a branch of the AST
            # if it is, recurse over the remaining AST
            elif char == '(':
                # save all the things until you get to the correct )
                # then recurse on that string
                nleftparen = nleftparen+1
                m = 0
                newstring = example_lisp[(n+1):]
                # search your new string until you get the correct )
                while nleftparen != nrightparen:
                    if newstring[m] == '(':
                        nleftparen = nleftparen + 1
                        m = m + 1
                    elif newstring[m] == ')':
                        nrightparen = nrightparen + 1
                        m = m+1
                    else:
                        m = m+1
                newobj.append(parse_lisp(newstring[0:m]))
                word = ''
                n = n+len(newstring[0:m])
            else:
                word = word + char
                n = n+1

    return newobj


import re

function_names = ['pow',
                  'sqrt',
                  'sin',
                  'cos',
                  'tan',
                  'asin',
                  'acos',
                  'atan',
                  'atan2'
                  'sinh',
                  'cosh',
                  'tanh',
                  'exp',
                  'log',
                  'log10',
                  'abs',
                  'min',
                  'max']

trig_funcs = ['sin',
              'cos',
              'tan']

invtrig_funcs = ['asin',
                 'acos',
                 'atan',
                 'atan2']


def find_matching_parenthesis(expr):
    stack = []
    matches = []

    # Traverse the expression
    for i, char in enumerate(expr):
        if char == '(':
            # Push index of the opening parenthesis onto the stack
            stack.append(i)
        elif char == ')':
            if stack:
                # Pop the most recent unmatched opening parenthesis
                opening_index = stack.pop()
                # Store the matching pair (opening, closing)
                matches.append((opening_index, i))

    if len(stack) > 0:
        print(f"unmatched parentheses in: {expr}")

    return matches

def gdml_trig_to_FC(expr):
    matching_paren = find_matching_parenthesis(expr)
    if len(matching_paren) == 0:
        return expr

    # Check if any of the trig functions are in the expression
    trig_parenthesis = []
    for func in trig_funcs:
        pattern = r'\b' + func + r'\b'
        matches = re.finditer(pattern, expr)
        for match in matches:
            # print(f"Match: {match.group()} at index {match.start()}-{match.end()}")
            # find which parenthese pair matches the enclosing arguments of the trig function
            for paren_pair in matching_paren:
                if paren_pair[0] == match.end():
                    trig_parenthesis.append(paren_pair)

    paren_dict = {}
    # sort the parenthesis in the order of thei indexes
    for paren in trig_parenthesis:
        paren_dict[paren[0]] = '('
        paren_dict[paren[1]] = ')'

    sorted_dict = dict(sorted(paren_dict.items()))

    out_expr = []
    src_pos = 0
    for index in sorted_dict:
        out_expr += expr[src_pos:index+1]
        if sorted_dict[index] == '(':
            out_expr += 'deg*('
        else:
            out_expr += ')'
        src_pos = index

    return ''.join(out_expr)

def gdml_invtrig_to_FC(expr):
    for func in invtrig_funcs:
        pattern = r'\b' + func + r'\b'
        if re.search(pattern, expr):
            expr = re.sub(pattern, '1/deg*'+func, expr)

    return expr
    

import sys
if __name__ == "__main__":
    expr = sys.argv[1]
    # expr = "(4*E*E+4*E*sin((RICH_mirror_tilt_angle)*DEGtoRAD)+1) / (cos((RICH_mirror_tilt_angle)*DEGtoRAD)*cos((RICH_mirror_tilt_angle)*DEGtoRAD))"
    
    matching_paren = find_matching_parenthesis(expr)
    if len(matching_paren) == 0:
        print("No parentheses found")
    else:
        print(matching_paren)
        replaced_expr = gdml_trig_to_FC(expr)
        print(replaced_expr)
        replaced_expr = gdml_invtrig_to_FC(replaced_expr)
        print(replaced_expr)
        


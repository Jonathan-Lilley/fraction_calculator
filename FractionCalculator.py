'''                                     FRACTION CALCULATOR                                             '''
# Program that takes in an equation and outputs a fraction as a string instead of a float or a long

# Takes result of a calculation and generates it in fraction form
def calculateFraction(inputVal):
    denom = 1 # Starting with two...
    # Check if inputVal*denom is a whole number
    while (inputVal*denom)%1 != 0:
        # If not, increment denom
        denom += 1
    # Return the string of the whole number over the calculated denominator
    numer = int(inputVal*denom)
    if denom > 1:
        return str(numer)+'/'+str(denom)
    else:
        return str(numer)

# Splits an input on a single character, like ( or +
def splitOnChar(string,char):
    segments = []
    segment = ''
    # Goes through every character in the string
    for c in range(len(string)):
        if string[c] != char: # Adds character to current segment if it is not the separator
            segment += string[c]
        elif string[c] == char: # On separator, appends segment if non empty to segments and separator to segments
            if segment != '':
                segments.append(segment)
                segment = ''
            segments.append(string[c])
        if c == len(string) - 1 and c != char: # If it's the end of the string and it's not a separator, adds segment
            segments.append(segment)
    segments = [segment for segment in segments if segment != ''] # Deletes any empty strings
    return segments # Returns segments as a list

# Larger segmentation function, generates a segments list based on a single separator
def segmentation(segments,newsegs,char):
    for segment in segments:
        newsegs += splitOnChar(segment,char)
    segments = newsegs
    newsegs = []
    return segments, newsegs

# Parses the equation using segmentation()
def parseEquation(streq):
    segments = [streq]
    newsegs = []
    i = 0
    for char in "()^*/-+": # Separates on basic mathematical operators
        segments, newsegs = segmentation(segments, newsegs, char)
        i += 1
    return segments

# Recursively groups parenthesis groups
def group(parsedEq):
    if '(' in parsedEq:
        start = parsedEq.index('(')
        replace, remainder = group(parsedEq[start+1:]) # Recursively generates grouped an rest of the equation
        parsedEq = parsedEq[:start]
        parsedEq.append(replace)
        if len(remainder) > 0:
            parsedEq += remainder
    if ')' in parsedEq:
        end = parsedEq.index(')')
        grouping = parsedEq[:end]
        if end != len(parsedEq)-1 and parsedEq[end+1] != ')':
            remainder = parsedEq[end+1:]
        else:
            remainder = []
    else:
        grouping = parsedEq
        remainder = []
    return grouping, remainder


def calculate(equation, operator):
    op = operator
    if op in equation:
        var1pos = equation.index(op)-1
        var2pos = equation.index(op)+1
        var1 = equation[var1pos]
        var2 = equation[var2pos]
        if op == '^':
            x = float(var1)**float(var2)
        elif op == '/':
            x = float(var1)/float(var2)
        elif op == '*':
            x = float(var1)*float(var2)
        elif op == '-':
            x = float(var1)-float(var2)
        elif op == '+':
            x = float(var1)+float(var2)
        else:
            return 0
        newvar = str(x)
        equation = equation[:var1pos] + [newvar] + equation[var2pos+1:]
    return equation

# Calculates total from parsed equation
def calculateFull(equation):
    for p in range(len(equation)):
        if type(equation[p]) is not str:
            equation = equation[:p] + calculateFull(equation[p]) + equation[p+1:]
    for char in '^/*-+':
        equation = calculate(equation,char)
    return equation


if __name__ == "__main__":
    inp = ''
    while inp != 'exit':
        inp = input()
        if inp == 'exit':
            "ending"
            break
        parsedEq = parseEquation(inp)
        groupings = group(parsedEq)[0]
        total = float(calculateFull(groupings)[0])
        print(total)
        fraction = calculateFraction(total)
        print(fraction)
        print('\n')
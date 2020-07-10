import sys

file_name = sys.argv[1]
input_file = open(file_name, "r")
input_text = input_file.read()

# split the string into an array of lines using the new line character '\n'
program_lines = input_text.split('\n')

# this will be used to store the variables in a PipePipe program
bindings = {}

# remove all spaces from a string
def spaceless(str):
  return str.replace(' ', '')

# --------------------------------------
# LOW-LEVEL LINE TYPE CHECKING FUNCTIONS
# --------------------------------------

# return True if line has first token and second token, but no third token
def has_no_third_col(tokens):
  return tokens[0] != None and tokens[1] != None and tokens[2] == None 

# return True if line has no third token, but has second token and third token 
def has_no_first_col(tokens):
  return tokens[0] == None and tokens[1] != None and tokens[2] != None 

# return True if line has all three tokens (for COMPOUND type)
def has_three_cols(tokens):
  return tokens[0] != None and tokens[1] != None and tokens[2] != None 

# return True if line has question in second token
def has_question_in_second_col(tokens):
  return tokens[1][-1] == '?'

# --------------------------------------
# TOP-LEVEL LINE TYPE CHECKING FUNCTIONS
# --------------------------------------

def is_input_type(tokens):
  return has_no_third_col(tokens) and has_question_in_second_col(tokens)

def is_assign_type(tokens):
  return has_no_third_col(tokens) and not has_question_in_second_col(tokens)

def is_output_type(tokens):
  return has_no_first_col(tokens)

def is_compound_type(tokens):
  return has_three_cols(tokens)

# -------------------
# EXECUTION FUNCTIONS
# -------------------

def execute_input(var_name, question):
  
  # remove all spaces from var_name
  var_name = spaceless(var_name)
  
  # use the input function to ask the user for input, and put the return value in bindings
  bindings[var_name] = int(input(question + ' '))

def execute_assign(var_name, expression):
  
  # remove all spaces from var_name and expression
  var_name = spaceless(var_name)
  expression = spaceless(expression)
  
  # build a Python statement as a string
  statement = var_name + '=' + expression
  
  # use the built-in exec function to execute the Python statement
  exec(statement, bindings)

def execute_output(expression, output_format):
  
  # use execute_assign to create a temporary variable 
  # since an OUTPUT line doesn't have a variable, we use the special name __tmpvar__
  # there's no need to remove spaces from expression here because 
  # execute_assign will take care of that
  execute_assign('__tmpvar__', expression)
  
  # replace the double underscore with the temporary variable, 
  # and print the output string
  print(output_format.replace('__', str(bindings['__tmpvar__'])))
  
# basically the same as execute_output, but using an actual variable name
def execute_compound(var_name, expression, output_format):
  execute_assign(var_name, expression)

  # we need to remove the spaces from var_name because 
  # it will be used directly in this function later
  var_name = spaceless(var_name)
  
  # we're using var_name here to get the value from bindings
  print(output_format.replace('__', str(bindings[var_name])))

# the main execute function, it doesn't do any real work itself
# it delegates the work to the other execute functions
def execute(ast):
  for line in ast:
    line_type = line[0]
    params = line[1:]
    if(line_type == 'INPUT'):    execute_input(*params)
    if(line_type == 'ASSIGN'):   execute_assign(*params)
    if(line_type == 'OUTPUT'):   execute_output(*params)
    if(line_type == 'COMPOUND'): execute_compound(*params)

# -------
# PARSING
# -------

# take the tokens of a line, and return the AST (as a tuple) for that line
def parse(tokens, line):
  if(is_input_type(tokens)):
    return ( 'INPUT', tokens[0], tokens[1] )
  elif(is_assign_type(tokens)):
    return ( 'ASSIGN', tokens[0], tokens[1] )
  elif(is_output_type(tokens)):
    return ( 'OUTPUT', tokens[1], tokens[2] )
  elif(is_compound_type(tokens)):
    return ( 'COMPOUND', tokens[0], tokens[1], tokens[2] )
  else:
    raise Exception('line type not supported - {}', line)

# ------------
# TOKENIZATION
# ------------

def tokenize(line):
  
  # break a string into a list of smaller strings, each represent a column (token)
  tokens = line.split('|')
  
  # strip surrounding spaces from each token (t)
  tokens = [ t.strip() for t in tokens ]
  
  # for each token, return None if it's an empty string, otherwise return the token (t) itself
  tokens = [ None if t=='' else t for t in tokens ]

  # if the line has only two tokens, that means it contains only one pipe (the second pipe is optional for INPUT line and ASSIGN line)
  if(len(tokens) == 2):
    
    # add a third token (None) to keep every line consistent with three tokens
    tokens.append(None)

  # if the line doesn't have three tokens, that means there's a syntax error
  if(len(tokens) != 3):
    raise Exception('too many columns - {}', line)
    
  return tokens

# -------------
# THE MAIN LOOP
# -------------
    
# prepare an array to store the AST    
ast = []

# for each line in a PipePipe program
for line in program_lines:
  
  # a valid line should have at least one pipe '|'
  if('|' in line):
    
    # get tokens from string
    tokens = tokenize(line)
    
    # get AST from tokens
    ast_line = parse(tokens, line)
    
    # add the AST of the line to the array
    ast.append(ast_line)

# call the execute function by passing the AST
execute(ast)

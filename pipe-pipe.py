import sys

tx_file = sys.argv[1]
input_file = open(tx_file, "r")
input_text = input_file.read()
program_lines = input_text.split('\n')

bindings = {}

def spaceless(str):
  return str.replace(' ', '')

def has_no_third_col(tokens):
  return tokens[0] != None and tokens[1] != None and tokens[2] == None 

def has_no_first_col(tokens):
  return tokens[0] == None and tokens[1] != None and tokens[2] != None 

def has_three_cols(tokens):
  return tokens[0] != None and tokens[1] != None and tokens[2] != None 

def has_question_in_second_col(tokens):
  return tokens[1][-1] == '?'

def has_no_question_in_second_col(tokens):
  return not has_question_in_second_col(tokens)

def is_input_type(tokens):
  return has_no_third_col(tokens) and has_question_in_second_col(tokens)

def is_assign_type(tokens):
  return has_no_third_col(tokens) and has_no_question_in_second_col(tokens)

def is_output_type(tokens):
  return has_no_first_col(tokens)

def is_compound_type(tokens):
  return has_three_cols(tokens)

def execute_input(var_name, question):
  bindings[var_name] = int(input(question + ' '))

def execute_assign(var_name, expression):
  if(' x ' in expression):
    expression = expression.replace(' x ', ' * ')
  expression = spaceless(expression)
  statement = var_name + '=' + expression
  if(var_name not in bindings):
    bindings[var_name] = None # declare variable
  exec(statement, bindings)

def execute_output(expression, output_format):
  execute_assign('__tmpvar__', expression)
  print(output_format.replace('__', str(bindings['__tmpvar__'])))

def execute_compound(var_name, expression, output_format):
  execute_assign(var_name, expression)
  print(output_format.replace('__', str(bindings[var_name])))

def run(program_lines):

  for line in program_lines:
    
    # ignore if the line doesn't contain a pipe
    if('|' not in line):
      continue
  
    # break a line into tokens
    tokens = line.split('|')

    # strip surrounding spaces
    tokens = [t.strip() for t in tokens]
    
    # use None to represent an empty token
    tokens = [None if t=='' else t for t in tokens]

    # if a line has only 2 tokens, add an extra None
    if(len(tokens)==2):
      tokens.append(None)

    # check error
    if(len(tokens) > 3):
      raise Exception('too many columns on the line - {}', line)

    # tokenization over, parsing begin
    if(is_input_type(tokens)):
      execute_input(spaceless(tokens[0]), tokens[1])

    elif(is_assign_type(tokens)):
      execute_assign(spaceless(tokens[0]), tokens[1])

    elif(is_output_type(tokens)):
      execute_output(tokens[1], tokens[2])

    elif(is_compound_type(tokens)):
      execute_compound(spaceless(tokens[0]), tokens[1], tokens[2])

    else:
      raise Exception('interpret can not understand the line - {}', line)

run(program_lines)

import sys

file_name = sys.argv[1]
input_file = open(file_name, "r")
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

def is_input_type(tokens):
  return has_no_third_col(tokens) and has_question_in_second_col(tokens)

def is_assign_type(tokens):
  return has_no_third_col(tokens) and not has_question_in_second_col(tokens)

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

def execute(ast):
  for line in ast:
    line_type = line[0]
    params = line[1:]
    if(line_type == 'INPUT'):    execute_input(*params)
    if(line_type == 'ASSIGN'):   execute_assign(*params)
    if(line_type == 'OUTPUT'):   execute_output(*params)
    if(line_type == 'COMPOUND'): execute_compound(*params)

def parse(tokens, line):
  if(is_input_type(tokens)):
    return ( 'INPUT', spaceless(tokens[0]), tokens[1] )
  elif(is_assign_type(tokens)):
    return ( 'ASSIGN', spaceless(tokens[0]), tokens[1] )
  elif(is_output_type(tokens)):
    return ( 'OUTPUT', spaceless(tokens[1]), tokens[2] )
  elif(is_compound_type(tokens)):
    return ( 'COMPOUND', spaceless(tokens[0]), tokens[1], tokens[2] )
  else:
    raise Exception('line type not supported - {}', line)

def tokenize(line):
  tokens = line.split('|')
  tokens = [t.strip() for t in tokens]
  tokens = [None if t=='' else t for t in tokens]

  if(len(tokens) == 2):
    tokens.append(None)

  if(len(tokens) == 3):
    return tokens
  else:
    raise Exception('too many columns - {}', line)

def run(program_lines):
  ast = []
  for line in program_lines:
    if('|' in line):
      tokens = tokenize(line)
      ast_line = parse(tokens, line)
      ast.append(ast_line)

  execute(ast)

run(program_lines)

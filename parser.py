# parser.py
#
"""
Parser for Command Language, of the form:

as principal admin password "admin" do
   create principal bob "B0BPWxxd"
   set x = "my string"
   set y = { f1 = x, f2 = "field2" }
   set delegation x admin read -> bob
   return y.f1
***

<prog> ::= as principal p password s do \n <cmd> ***
re = ^as\s+principal\s+[A-Za-z][A-Za-z0-9_]*\s+password\s+[A-Za-z0-9_ ,;\.?!-]*\s+\\n(.)+(\\n)*\*\*\*$
re = ^as\s+principal\s+[A-Za-z][A-Za-z0-9_]*\s+password\s+\"[A-Za-z0-9_ ,;\.?!-]*\"\s+do\s*\n(.*\n*)*\*{3}$
^as\s+principal\s+([A-Za-z][A-Za-z0-9_])*\s+password\s+\"([A-Za-z0-9_ ,;\.?!-]*)\"\s+do
<cmd> ::= exit \n | return <expr> \n | <prim_cmd> \n <cmd>
^\s*exit\s*\\n |

<expr> ::=  <value> | [] | { <fieldvals> }
<fieldvals> ::=  x = <value> | x = <value> , <fieldvals>
<value> ::=  x | x . y | s
[A-Za-z][A-Za-z0-9_]*
[A-Za-z][A-Za-z0-9_]+.[A-Za-z][A-Za-z0-9_]+
[A-Za-z0-9_ ,;\.?!-]*
<prim_cmd> ::=
          create principal p s
          ^\s*create\s+principal\s+([A-Za-z][A-Za-z0-9_]*)\s+(.)*([A-Za-z0-9_ ,;\.?!-]*)\s*\\n
        | change password p s
        ^\s*change\s+password\s+([A-Za-z][A-Za-z0-9_]*)\s+(.)*([A-Za-z0-9_ ,;\.?!-]*)\s*\\n
        | set x = <expr>
        ^\s*set\s+
        | append to x with <expr>
        ^\s*append\s+to\s+([A-Za-z][A-Za-z0-9_]*)\s+with\s+(.)
        | local x = <expr>
        | foreach y in x replacewith <expr>
        | set delegation <tgt> q <right> -> p
        | delete delegation <tgt> q <right> -> p
        | default delegator = p
<tgt> ::= all | x
<right> ::= read | write | append | delegate

regex alternative

as principal p password s do \n <cmd> ***
(


"""

import sys, re


def check_program(password, program):
    program_re = re.compile("^as\s+principal\s+[A-Za-z][A-Za-z0-9_]*\s+password\s+\"[A-Za-z0-9_ ,;\.?!-]*\"\s+do\s*\n(.*\n*)*\*{3}$")
    if program_re.match(program):
        print "program format is correct"
        check_pass(password, program)
    else:
        print >>sys.stderr, 'The program syntax is incorrect'
        sys.exit(1)

def check_pass(password, program):
    cmdline_tokens = re.compile("^as\s+principal\s+([A-Za-z][A-Za-z0-9_])*\s+password\s+\"([A-Za-z0-9_ ,;\.?!-]*)\"\s+do")
    principal, cmd_pass = cmdline_tokens.match(program)
    print "Server-set password: " + password
    print "Command-line password: " + cmd_pass
    if cmd_pass != password:
       print >>sys.stderr, 'The password is incorrect'
       sys.exit(1)
    else:
        pass

def expression(rbp=0):
    global token
    t = token
    token = next()
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next()
        left = t.led(left)
    return left

class literal_token:
    def __init__(self, value):
        self.value = int(value)
    def nud(self):
        return self.value


class operator_add_token:
    lbp = 10
    def led(self, left):
        right = expression(10)
        return left + right

class operator_sub_token:
    lbp = 10
    def led(self, left):
        return left - expression(10)

class operator_mul_token:
    lbp = 20
    def led(self, left):
        return left * expression(20)

class operator_div_token:
    lbp = 20
    def led(self, left):
        return left / expression(20)

class end_token:
    lbp = 0

token_pat = re.compile("\s*(?:(\d+)|(.))")

def tokenize(program):
    # tokenize based on sequential commands
    # need a storage system for the tokens
    # need all the possible token types and variables

    for number, operator in token_pat.findall(program):
        if number:
            yield literal_token(number)
        elif operator == "+":
            yield operator_add_token()
        elif operator == "-":
            yield operator_sub_token()
        elif operator == "*":
            yield operator_mul_token()
        elif operator == "/":
            yield operator_div_token()
        else:
            raise SyntaxError("unknown operator")
    yield end_token()


def parse(password, program):
    check_program(password, program)
    global token, next
    next = tokenize(program).next
    token = next()
    #need to return the format storage for instructions
    return expression()
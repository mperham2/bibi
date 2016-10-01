# cmdparse.py
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

from pyparsing import alphas, nums, dblQuotedString, Combine, Word, Group, delimitedList, Suppress, removeQuotes
import string, re


def getCmdFields( s, l, t ):
    t["method"],t["requestURI"],t["protocolVersion"] = t[0].strip('"').split()

cmdLineBNF = None
def getCmdLineBNF():
    global cmdLineBNF

    if cmdLineBNF is None:
        integer = Word( nums )
        ipAddress = delimitedList( integer, ".", combine=True )

        timeZoneOffset = Word("+-",nums)
        month = Word(string.uppercase, string.lowercase, exact=3)
        serverDateTime = Group( Suppress("[") +
                                Combine( integer + "/" + month + "/" + integer +
                                        ":" + integer + ":" + integer + ":" + integer ) +
                                timeZoneOffset +
                                Suppress("]") )

        cmdLineBNF = ( ipAddress.setResultsName("ipAddr") +
                       Suppress("-") +
                       ("-" | Word( alphas+nums+"@._" )).setResultsName("auth") +
                       serverDateTime.setResultsName("timestamp") +
                       dblQuotedString.setResultsName("cmd").setParseAction(getCmdFields) +
                       (integer | "-").setResultsName("statusCode") +
                       (integer | "-").setResultsName("numBytesSent")  +
                       dblQuotedString.setResultsName("referrer").setParseAction(removeQuotes) +
                       dblQuotedString.setResultsName("clientSfw").setParseAction(removeQuotes) )
    return cmdLineBNF

testdata = """
195.146.134.15 - - [20/Jan/2003:08:55:36 -0800] "GET /path/to/page.html HTTP/1.0" 200 4649 "http://www.somedomain.com/020602/page.html" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
111.111.111.11 - - [16/Feb/2004:04:09:49 -0800] "GET /ads/redirectads/336x280redirect.htm HTTP/1.1" 304 - "http://www.foobarp.org/theme_detail.php?type=vs&cat=0&mid=27512" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)"
11.111.11.111 - - [16/Feb/2004:10:35:12 -0800] "GET /ads/redirectads/468x60redirect.htm HTTP/1.1" 200 541 "http://11.11.111.11/adframe.php?n=ad1f311a&what=zone:56" "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1) Opera 7.20  [ru\"]"
127.0.0.1 - u.surname@domain.com [12/Sep/2006:14:13:53 +0300] "GET /skins/monobook/external.png HTTP/1.0" 304 - "http://wiki.mysite.com/skins/monobook/main.css" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.6) Gecko/20060728 Firefox/1.5.0.6"
"""
cmddata = """
as principal admin password "admin" do
   create principal bob "B0BPWxxd"
   set x = "my string"
***
"""

splitprogram = cmddata.split("\n")
proglength = len(splitprogram)

termsig = re.compile("\*\*\*")
if re.match(termsig, splitprogram[proglength-1]) == None:
    print >>sys.stderr, 'FAILED'
    sys.exit(1)

for line in cmddata.split("\n"):
    if not line: continue
    fields = getCmdLineBNF().parseString(line)
    print(fields.dump())
    #~ print repr(fields)
    #~ for k in fields.keys():
        #~ print "fields." + k + " =", fields[k]
    print(fields.asXML("LOG"))
    print()
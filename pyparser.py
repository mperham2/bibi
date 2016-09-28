from pyparsing import Word, alphas

# define grammar of a greeting
greet = Word(alphas) + "," + Word(alphas) + "!"
principal = "as " + "principal " + Word(alphas) + "password " + Word(alphas) + "do"
test1 = "\"" + Word(alphas) + "\""

hello = "Hello, World! Where is my cheese?"

msg1 = "as principal admin password \"admin\" do"
msg2 = "\"wooly\""

print (hello, "->", greet.parseString(hello))
print (msg1, "->", principal.parseString(msg1))
print (msg2, "->", test1.parseString(msg2))

if test1.parseString(msg1):
	print (msg1, "in wooly test->", test1.parseString(msg1))
else:
	print ("not matching gives a false ouput")


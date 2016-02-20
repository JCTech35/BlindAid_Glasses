
fo = open("colorshades.txt", "r")

mystring = fo.read()

#print("Old  = " + mystring + "\n\n")

mystring = mystring.replace('{ ', 'Color(')
mystring = mystring.replace(	' }', ')')

print("New  = " + mystring + "\n")

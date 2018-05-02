#lambda functions

def func(x,y,z):
    return x+y+z

print(func(1,2,3))

myVar = lambda x,y,z:x+y+z
print(myVar(1,2,3))

# List of lambdas

myVar2 = [lambda x:x**2,
          lambda x:x**3,
          lambda x:x+20]

for i in myVar2:
    print(i(2))

# Dictionary of lambdas

myCalcDict = {'add': lambda x,y:x+y,
              'subtract': lambda x,y:x-y}

print(myCalcDict['add'](2,4))# This calls the add lambda function inside the myCalcDict object and then returns the value.

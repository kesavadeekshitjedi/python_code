
def printList(*myList):
    print(myList)

def printDict(**myDict):
    print(myDict)

printList(1,2,3,5)
printDict(name="test",age="5")

data = (1,3)
def unpackTuple(a,b):
    print(a,b)


unpackTuple(*data)

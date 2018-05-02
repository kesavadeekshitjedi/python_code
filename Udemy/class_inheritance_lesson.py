class myClass(object): # This class called myClass is inheriting the object class
    count=0
    def __init__(self):
        type(self).count+=1
    def __del__(self):
        type(self).count-=1
    def regMethod(self,myMessage):
        self.message = myMessage
        print("Hello ",self.message)

myObj = myClass()
print("Number of instances of the MyClass objects are :",myObj.count)
myObj2 = myClass()
print("Number of instances of the MyClass objects are :",myObj.count)

del myObj # deleting an object
print("Number of instances of the MyClass objects are :",myObj2.count)
myObj2.regMethod("Test")
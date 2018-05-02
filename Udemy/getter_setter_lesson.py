class myClass():
    def __init__(self,name):
        self.__name=name # This makes the name variable private. This means that even the object of the class has no access to the variable. #security
        # To access the variable, create the getter and setter methods

    def set_name(self,name):
        self.__name=name
    def get_name(self):
        return self.__name

myObj = myClass("banana") # This creates an instance of the myClass object and passes banana as the parameter.
# To access the variable, call the getter method

print(myObj.get_name())
myObj.set_name("apple")
print(myObj.get_name())
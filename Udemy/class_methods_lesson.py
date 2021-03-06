class myClass(object): # inheriting the object class again
    # Here we are defining a method for this class. it does not need an object of the class to be passed to it.
    __writer = "Deekshit Addepalli"
    @classmethod # This is a decorator that tells the method following it that it is a classmethod

    def myMethod(cls): # the cls in the arg for the method is only to imply that it is a class method. this is a mandatory keyword.
        return myClass.__writer

    @staticmethod
    def myStaticMethod(readerName): # Does not need the self or cls keywords.
        returnVal = "Reader is "+readerName
        return returnVal
    # All other methods need to have the self keyword. When the self keyword is present, the object needs to be passed as an argument when calling it with the class.
    # example: myClass.regMethod(classObj,x,y) - where classObj is the object of myClass and x and y are variables of the regMethod method,
    # If a modeule (.py file) contains a list of methods and no class, then those methods are called functions

    def addNumbers(self,x,y):
        self.var1 = x
        self.var2 = y
        return x+y
        # The reason we use self.var1 etc is so that we attach the attribute to the object that is created.
        # In this case, myObj (line below) will be able to print the values of x and y using myObj.x and myObj.y with the print statement. If the self.var1 etc were not used this would not be possible.
myObj = myClass()
print("Author is : ",myClass.myMethod())
print(myClass.myStaticMethod("Anantha"))
print(myClass.addNumbers(myObj,2,3))
class FirstClass():
    print("This is the first class from the Udemy lesson")


instance = FirstClass() # Creating an instance of the FirstClass class.

print(type(instance))

class Fruit():
    fruit_cost = "60"
    def __init__(self,name):
        self.name=name
        print("Fruit is "+self.name)

obj1 = Fruit("banana")
print("Cost of "+obj1.name+" is "+obj1.fruit_cost)

obj1 = Fruit("apple")
print("Cost of "+obj1.name+" is "+obj1.fruit_cost)


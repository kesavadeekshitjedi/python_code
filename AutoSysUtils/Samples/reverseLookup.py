def reverse_lookup(dictionary,value):
    for key in dictionary:
        if dictionary[key]==value:
            return key

myDict = {"name":"Deekshit","phone":"651","name2":"Deekshit"}

print(reverse_lookup(myDict,"Deekshit"))
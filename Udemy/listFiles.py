import os

def listDirectory(dirName):
    for name in os.listdir(dirName):
        print(name)
        print(os.path.join(dirName,name))

listDirectory("C:\\github-repos-deek\\python_code\\Udemy")
my_word = "bananabana"
my_search_word = "ana"

def number_of_occurances(string, substring):
    count = start = 0
    while True:
        start = string.find(substring,start)+1
        if start > 0:
            count +=1

        else:
            return count
def main():
    print(number_of_occurances("banana","ana"))
    #print("banana".find("ana"))
main()
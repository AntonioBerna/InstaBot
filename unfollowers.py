def getUnFollowers(first_file, second_file):
    first_l = first_file.readlines()
    second_l = second_file.readlines()

    l = []
    for i in range(0, len(first_l)):
        if first_l[i] not in second_l:
            l.append(first_l[i])
    if l != []:
        return l
    else:
        return "Non sono stati trovati UnFollowers!"

first_file = open("(account_name) dd-mm-yyyy.txt", "r")
second_file = open("(account_name) dd-mm-yyyy.txt", "r")
result = getUnFollowers(first_file, second_file)
print(result)
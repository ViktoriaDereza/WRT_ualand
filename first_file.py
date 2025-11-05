"""age = int(input("вік.."))
if age > 18:
    print("Old")
else:
    print ("young")"""


"""age = int(input("вік.."))
print("old") if age > 18 else print("young")"""



"""student = ["Vlad", "Anton", "M"]
for i in student:
    print(f"st {i} is here")



n = int(input("enter number"))
for i in range(1, n):
    if i % 2 == 0:
        print(i)"""



result = 0
num_or_stop = input("number or stop")
while num_or_stop != "stop":
    result += int(num_or_stop)
    num_or_stop = input("number or stop")
print(result)
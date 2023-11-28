d=["a","b","c","d"]
teststr="aaaaaaaaaaaaaaa"
print(", ".join(d))
print(any(teststr in item for item in d))

# my_list = ["apple", "orange", "mango"]
# substring = "go"

# if any(substring in item for item in my_list):
#     print("List contains an element with 'go'")
# import re
# user_input="go east north"
# pattern=r"(east|west|north|south)"
# user_input=user_input.lower()
# if(not user_input):
#     user_input=input("Sorry, you need to 'go' somewhere.")
# else:
#     if "go" in user_input:
#             match=re.findall(pattern,user_input);
#             print(match)

lst=[12,23,4,5,3]
lst.append(1)

print(333 in lst)
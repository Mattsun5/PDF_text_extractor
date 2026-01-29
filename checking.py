import json
# student dictionary to practice traversing
# student_record = { "name" : "Joshua", 
#                   "age" : "22", 
#                   "country" : "Nigera", 
#                   "test_score" : {"math" : 45, "english" : 50, "basic_science" : 70, "civic_education" : 80} }


# FORMAT FOR THE PRINT RESULT
# NAME OF STUDENT: Joshua
# "math" - 45
# "english" - 50
# "basic_science" - 70
# "civic_education" - 80

# # to Print all key names in the dictionary:
# for x in student_record:
#   print(x)

# to Print all values in the dictionary:
# for x in student_record:
#   print(student_record[x])
#   print("Key : " + x + " - value : " + student_record[x])

# using the values() method to return values of a dictionary:
# for x in student_record.values():
#   print(x)

# using the keys() method to return the keys of a dictionary:
# for x in student_record.keys():
#   print(x)

#  traverse through both keys and values, by using the items() method:
# for x, y in student_record.items():
# #   print(x, y)
#     print("Key : " + x + " - value : " + y)



# TODAY

# SQUARE BOX
# horizontal = "--"
# vertical = "|"
# size = 4

# # top border
# print("+" + (horizontal) * size + horizontal + "+")

# # To draw vertical lines
# for x in range(size):
#     print(vertical + (" " * size * 2) + "  " + vertical)

# # bottom border
# print("+" + (horizontal) * size + horizontal + "+")


# SQUARE BOX WITH ASTERIKS
# building_block = "*"
# column = 2
# # size = 10
# horizontal = 10
# vertical = 3

# horizontal_border = (building_block + " ") * (horizontal - 1) + building_block

# # top border
# print(horizontal_border * column)

# for x in range((vertical - 2)):
#     print(building_block + (" " * (horizontal + (horizontal - 3))) + building_block)
    
# # bottom border
# print((building_block + " ") * (horizontal - 1) + building_block)

# TABLE WITH ASTERIKS
building_block = "*"
column = 2
# row = 3
# size = 10
horizontal = 4
vertical = 3

numbers = { "0" : "three", 
                  "1" : "four", 
                  "2" : "fifteen"}
# for x, y in numbers.items():
# #   print(x, y)
#     print("Key : " + x + " - value : " + y)

horizontal_border = " " + (building_block + " ") * (horizontal) + building_block

def vertical_content(*content): 
    toprint = ""
    for x in range(len(content[0])):
        if x == 1:
            toprint += ((" " * 3) + str(content[0][x]) + (" " * 3) + building_block)
        else:
            toprint += (building_block + (" " * 3) + str(content[0][x]) + (" " * 3) + building_block)
    return toprint


print(building_block + horizontal_border * column)
# top border
for title, entry in numbers.items():
    print(vertical_content((title, entry)))
        
    # bottom border
    print(building_block + horizontal_border * column)


# # SQUARE BOX WITH ASTERIKS, FILLED
# building_block = "*"
# size = 10

# # top border
# print((building_block + " ") * (size - 1) + building_block)

# for x in range((size - 2)):
#     print((building_block + " ") * (size - 1) + building_block)
    
# # bottom border
# print((building_block + " ") * (size - 1) + building_block)


# 
# print("=o=o=[8}>")



# FILE HANDLING

# "r" - Read - Default value. Opens a file for reading, error if the file does not exist

# "a" - Append - Opens a file for appending, creates the file if it does not exist

# "w" - Write - Opens a file for writing, creates the file if it does not exist

# "x" - Create - Creates the specified file, returns an error if the file exists



# "t" - Text - Default value. Text mode

# "b" - Binary - Binary mode (e.g. images)



# file = open("testfile.txt")
# The code above is the same as:

# file = open("testfile.txt", "rt")

# file = open("testfile.txt")
# print(file.read())

# NUMBER OF CHARACTERS TO READ
# print(file.read(5))


# file = open("testfile.txt")
# RETURNS ONE LINE
# print(file.readline())
# file.close()

# with open("testfile.txt") as file:
#     print(file.read())

# LOOP THROUGH THE FILE LINE BY LINE
# with open("testfile.txt") as file:
#   num = 0
#   for x in file:
#     num += 1
#     print(str(num) + " " + x)


# TO WRITE TO A FILE
# To write to an existing file, you must add a parameter to the open() function:

# "a" - Append - will append to the end of the file

# "w" - Write - will overwrite any existing content


"""
collect details
retrieve existing details from file to check if email exist
if not, update new information
write new json to file
output successful
"""
# print("HELLO, enter details to register")
# name = input("enter your name: ")
# email = input("enter your email: ")
# password = input("enter your password: ")

# students_record = []

# student_record = {
#     "name" : name,
#     "email": email,
#     "password" : password
# }
# # read data from file and validate if email exist
# with open("classFile.txt", "r") as file:
# #   new = file.read()
#   data = list(json.load(file))
#   # check if json is empty
#   if len(data) == 0:
#     data.append(student_record)
#     msg = "successful"
#   else:
#     for x in range(len(data)):
#       if data[x]["email"] == student_record["email"]:
#         msg = "failed"
#         break
#       elif x == (len(data) - 1):
#         data.append(student_record)
#         msg = "successful"


#   if msg == "successful":
#     with open("classFile.txt", "w") as file:
#       new = json.dumps(data)
#       file.write(new)
#       print("student added successfully")
#   else:
#     print("email already exist")


# students_record.append(student_record)

# with open("classFile.txt", "w") as file:
#   new = json.dumps(student_record)
#   file.write(new)



# print("thank you")
# entered_email = input("enter email to continue: ")
# entered_password = input("enter password to continue: ")

# if entered_password == correct_password:
#     print("success")
# WRITE AND READ FILE

# with open("classFile.txt", "w") as file:
#   file.write("this is class file")

#open and read the file after the appending:
# with open("testfile.txt") as file:
#   print(file.read())


# customer = [
#     {
#         "id" : 1,
#         "name" : "Matthew",
#         "email" : "test.email.com",
#         "password" : 1234,
#         "age" : 18,
#         "acct balance" : 30000
#     },
#     {
#         "id" : 2,
#         "name" : "Matthew",
#         "age" : 18
#     }
# ]


# PASCALS TRIANGLE
"""
THE LOGICS(to form the triangle)
   1
  1 1
 1 2 1
1 3 3 1
- if we have 4 levels, i.e the highest space provided will be level(4) - 1 and the highest space is given to the first item
- as the triangle is drawn downwards, the space is reduced by -1
"""

# tri = [[1], [1, 1]]
# levels = 3

# while len(tri) < levels:
#     prev_item = tri[-1]
#     new_item = [1]
#     for j in range(len(prev_item) - 1):
#         new_item.append(prev_item[j] + prev_item[j + 1])
#     new_item.append(1)
#     tri.append(new_item)

# for x in range(len(tri)):
#     space = levels - (x + 1)
#     print((" " * space) + " ".join(map(str, tri[x])))




# privileges
# examiners can view all students, can delete student from the system, can set quiz, can view student results.
# student can take quiz, view personal result, can update name

# registration (teachers/examiners)
# students(candidates)
# they have email, names, password, identification

# procedure
# register or login
# register - as teacher or student

# rules
# no two emails are the same
# id cannot be the same

# quiz
# quiz has questions

# questions
# question has options
# question has a correct answer

# result
# result is total correct score over available score
# belong to student

# JSON

# users = {{...}, {....}, {...}}

# {
#     users : {{...}, {....}, {...}},
#     results : {{...}, {....}, {...}}
# }

# User = {
#     "id" : 12,
#   "name" : "John",
#   "type" : "teacher",
#   "email" : "....",
#   "password" : "..."
# }

# result = {
#     "id" : 12,
#     "score" : 50
# }

# quiz = {
    
# }

# questions = {
    
# }


# user defined id
# python defined(inbuilt) math.random + email
# libries defined
# database generated
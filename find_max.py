"""
Finds biggest word and count of this word in the file
Example: 
    file: aaa aaa bb cc ddd
    output: 3 : 3
"""

with open('text') as file:
    list_word = file.read().split()
count_letter = 0
list_count = list()
for word in list_word:
    list_count.append(len(word))
    if (len(word) > count_letter):
        count_letter = len(word)
count_word = list_count.count(max(list_count))
print("{} : {}".format(count_letter,count_word))

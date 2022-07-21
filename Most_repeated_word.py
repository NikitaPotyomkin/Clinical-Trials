count = 0
word = ""
maxCount = 0
words = []
import pandas as pd
df = pd.read_csv("Drugs.csv")

with open('Interventions.txt','r') as f:
    file = f.readlines()
def most_common(lst):
    return max(set(lst), key=lst.count)

with open("Interventions.csv",'r') as f:
    lines = f.readlines()
# Opens a file in read mode
# Gets each line till end of file is reached  
for line in file:
    # Splits each line into words
    name = line[: line.find(':')]
    line = line[line.find(':')+1:].replace('\n','').lower().split(',')
    word = most_common(line)
    words.append([name,word.title()])


# word = most_common(words)
with open('drugs_competitors.txt','w') as f:
    for word in  words:
        f.write(':'.join(word))
        f.write('\n')





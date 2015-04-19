

# Read the Data into the exercice:
 
with open('sou_all.txt','r') as file_obj:
    raw_data = file_obj.read()

data = raw_data.split("**********")


print len(data)

title = [None] * (len(data)-1)
speech =[None] * (len(data)-1)

print len(title)
print len(speech)


## Split the main Speech of the tittle information
for i in range (1,len(data)):
    SpeechSplit = data[i].split("_*****")
    title[i-1]= SpeechSplit[0]
    speech[i-1] = SpeechSplit[1]
    
year = [None] * len(title)
president =[None] * len(title)
    
    
print title[len(title)-1]    
## Split the President Name and the Year
for i in range (0,len(title)):
    TitleSplit = title[i].split("_")
    year[i]= TitleSplit[1]
    last = len(TitleSplit)
    president[i] = TitleSplit[last-1]



print year
print president


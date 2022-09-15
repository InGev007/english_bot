import csv

with open('dict.csv', newline='') as f:
    reader = csv.reader(f)
    dict = []
    rowd = []
    for row in reader:
	temp = row.split(" [ ")
        word = temp[0]
        transcription = temp[1].split(" ] - ")[0]
        translation = temp[1].split(" ] - ")[1]
        rowd.append(word)
        rowd.append(transcription)
        rowd.append(translation)
	dict.append(rowd)
        rowd.clear()
print(dict)

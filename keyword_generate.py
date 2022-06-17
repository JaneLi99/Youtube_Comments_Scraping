import csv

def keywords():
    with open("All_combined.csv", "r", encoding='UTF-8') as f:
        reader = csv.reader(f)
        list = [e[1].strip().split(",") for e in reader if e]

    str_list = []
    str_list.extend([x[0] for x in list])
    str_list.remove("open")
    print(str_list)

    file = open('All_combined.txt', 'w', encoding='UTF-8')
    file.write(str(str_list))
    file.close()

    wordtext = open('All_combined.txt', 'r', encoding='UTF-8')
    countdict = {}
    for line in wordtext:
        for word in line.split():
            word = word.lower()
            if word in countdict:
                countdict[word] += 1
            else:
                countdict[word] = 1
        for word in sorted(countdict):
            print("%s:%d" % (word, countdict[word]))
        result = sorted(countdict.items(), key=lambda k: k[1], reverse=True)
        print(result)

if __name__ == "__main__":
    keywords()



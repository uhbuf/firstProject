with open('from.txt','r') as f:
    for i in f:
        i=i.replace('32','30')
        i=i.replace('\n',' ')
        print(i)
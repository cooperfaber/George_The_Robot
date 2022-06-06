async def saveName(name, tag):
    f = open("data.txt", "a")
    f.write(name+' = '+tag+'\n')
    f.close()

async def loadNames(storage):
    f = open("data.txt", "r")
    lines = (f.read().split('\n'))
    for line in lines:
        content = line.split(' = ')
        if(len(content) <= 1): 
            return
        key = content[0]
        value = content[1]
        storage[key] = value
    

async def saveName(name, tag):
    f = open("data.txt", "a")
    f.write(name+' = '+tag)
    f.close()

async def loadNames(name, tag):
    f = open("data.txt", "r")
    

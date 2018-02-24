
def log(label,data):
    file = open("log.txt","a+")
    logData = ("\n"+str(label)+" : "+str(data))
    file.write(logData)
    file.close()

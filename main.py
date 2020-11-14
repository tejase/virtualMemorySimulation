import sys

# from array import *
diskAccessCount = 0 
pageTable = []
i = 0
def freeFrame(totalFrames,usedFrameCount):
    if(totalFrames > usedFrameCount):
        return True
    else: 
        return False

def foundNonZero(pageTable):
    for x in pageTable:
        if(x[3]!=0):
            return True
    return False


def OS(pages, frames):
    global i
    global pageTable
    while(1):
        if(i==1):

            if(foundNonZero(pageTable)):
               
                global diskAccessCount
                print(pages,frames)
                usedFrameCount = 0
                for x in pageTable: 
                    if(x[3]!=0):
                        print(x)
                        #MMU wants the page at that index loaded. 
                        
                        #check if free frame availale
                        for y in pageTable:
                            if(y[0]):
                                usedFrameCount += 1
                        if(freeFrame(int(frames),int(usedFrameCount))):
                            x[1] = usedFrameCount
                            x[0] = 1
                        else:
                            print('else')
                            #get victim page frame number
                            #index = karthisFunction()
                            # if(pageTable[1][2]):
                            #     print("sleep 1")
                            #     diskAccessCount += 1
                            #     pageTable[1][0] = 0
                            print("sleep 1")
                            diskAccessCount += 1
                            x[1] = 9 #karthis returned frame number
                            x[0] = 1
                            x[2] = 0
                            x[3] = 0
                print(pageTable)     
                #i = 0
                #exit the loop
                continue
            else:
                break


                

                

def initialisePageTable(refString):
    global pageTable
    li = list(refString.split(" ")) 
    print(len(li))
    
    for i in range(len(li)):
        pageTable.append([1,0,0,0])
    pageTable.append([1,0,0,1])
    print(pageTable)
    return pageTable




if __name__ == '__main__':
    argumentList = sys.argv 
    #print (argumentList[3]) 
    pageTable = initialisePageTable(argumentList[3])
    OS(sys.argv[1],sys.argv[2])

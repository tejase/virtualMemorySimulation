import threading                #Importing necessary modules
import time

diskAccessCount = 0             #Initialising variables with default values 
pageTable = []
SIGCONT = False
SIGUSR1 = False

def printPageTable():          #Printing entries in Pagetable
    global pageTable
    for i in pageTable:
        print(i)
        
    print('\n\n')
        

def initialisePageTable(n):     #Initialising page table with necessary values 
    global pageTable
    for i in range(n):
        pageTable.append([0,-1,0,0,0])      #Each entry from left denotes valid bit, frame allocated, dirty bit, requested, counter(Used for LRU purpose) 
        

def freeFrame(totalFrames,usedFrameCount):   #Function to check for freeframes
    if(totalFrames > usedFrameCount):
        return True
    else: 
        return False

def foundNonZero():           #Checking for Non zeron value in pagetable
    global pageTable
    for x in pageTable:
        if(x[3]!=0):
            return True
    return False

def OS(pages, frames):              #OS function taking 2 arguments
    global SIGCONT
    global SIGUSR1
    global pageTable
    initialisePageTable(pages)
    #printPageTable()
    while(1):
        if SIGCONT == True:
            SIGCONT = False
            if(foundNonZero()):
                global diskAccessCount
                usedFrameCount = 0        
                for x in pageTable:          #Scanning through the page table for non-zero 
                    if(x[3]!=0):
                        for y in pageTable:
                            if(y[0]):
                                usedFrameCount += 1
                        if(freeFrame(int(frames),int(usedFrameCount))):
                            
                            x[1] = usedFrameCount   #
                            x[0] = 1
                            x[2] = 0
                            x[3] = 0
                            x[4] = 0
                            diskAccessCount += 1
                        else:
                            min = 100000                                 
                        
                            for i in range(len(pageTable)):   #Loop to find Victim page 
                                if pageTable[i][0]:
                                    if pageTable[i][4] <= min:
                                        min = pageTable[i][4]
                                        v = i
                            
                            if pageTable[v][2] == 1:    #Condition to check whether the victim page is dirty
                                time.sleep(1);
                                diskAccessCount += 1    #Diskaccesses has been incremented
                            
                            f = pageTable[v][1]         #Updation of Page Table
                            pageTable[v][0] = 0
                            pageTable[v][1] =-1
                            pageTable[v][2] = 0
                            pageTable[v][3] = 0
                            pageTable[v][4] = 0
                            
                            time.sleep(1)
                            
                            diskAccessCount += 1        #Diskaccesses has been incremented
                            x[1] = f 
                            x[0] = 1
                            x[2] = 0
                            x[3] = 0
                            x[4] = 0
                
                SIGUSR1 = True
                
                continue
            else:
                break           #exit the loop
    

def inRAM(pno):                          #checks whether the page is in RAM 
    global pageTable
    return pageTable[pno][0]
        

def MMU(p, ref_str, pid):          #Mentioning the PID to the requested field for                                 that page
    c = 0
    global pageTable
    global diskAccessCount
    while True:
        if len(pageTable) == p:
            break 
    printPageTable();
    global SIGCONT              
    global SIGUSR1       
    l = ref_str.split(' ')
    for i in l:
        request = i[0]
        page = int(i[1])
        if not inRAM(page):        #Simulation of Page Fault
            pageTable[page][3] = 1234         
            SIGCONT = True
            while True:
                if SIGUSR1 == True:
                    SIGUSR1 = False 
                    break
                
        if request == 'W':                #updation of Dirty bit if it is a write access 
            pageTable[page][2] = 1
            
        pageTable[page][4] = c         #Printing of Updated page table
        print(i)
        printPageTable()
        c += 1             #Counter used for the purpose of LRU replacement
        
    SIGCONT = True 
    time.sleep(2)
    
if __name__ == "__main__": 
    # creating thread 
    t1 = threading.Thread(target=OS, args=(5,3,)) 
    t2 = threading.Thread(target=MMU, args=(5,"R0 R1 R1 W3 R0 R2 R2 W4 R0 R2 R2 W4 R0 R2 R2 W4 R0 R1 R1 W3 R0 R1 R1 W3", 10,)) 
  
    # starting thread 1 
    t1.start() 
    # starting thread 2 
    t2.start() 
  
    # wait until thread 1 is completely executed 
    t1.join() 
    # wait until thread 2 is completely executed 
    t2.join() 
  
    print("Number of disc accesses is " + str(diskAccessCount))
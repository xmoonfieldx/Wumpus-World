import numpy as np
import random

def find_gold(prev2,prev, pos):
    x=str(int(pos/4+1))
    y=str(int(pos%4+1))
    strn='['+x+','+y+']'
    print("Moved to",strn)
    global wumpus, gold, pit, status, arrows, points
    points-=1
    for i in range(len(wumpus)):
    #Check if Wumpus was encountered
        if(wumpus[i] == pos):
            if(arrows>0):
                print("Wumpus was encountered. \nYou shot him with an arrow.")
                wumpus = np.delete(wumpus,i)
            else:
                print("The Wumpus killed you.\nGAME OVER!!!")
                return -1
    
    #Check if they are now in a pit
    for i in range(len(pit)):
        if(pit[i] == pos):
            print("Pit. You fell to your death. \nGAME OVER!!!")
            return -1
    status[pos][0]=1
    
    #Check if there's gold
    if pos == gold:
        print("Glitter.\nDigging...\nFound Gold.")
        if(arrows<=0):
            points-=10
        print("Points:", points)
        print("Escaping cave now.")
        return 0
    
    #Check if there's stench 
    if(status[pos][2] == 1):
        print("Wumpus around. \n")
    
    #Check if there's breeze
    if(status[pos][3] == 1):
        print("Pit nearby. \n")
    
    #Explore possible positions top, bottom, left, right and if few don't exist, label them -1
    next_move=np.array([pos+4,pos-4,pos-1,pos+1])
    if(next_move[0]>15):
        next_move[0] = -1
    if(next_move[1]<0):
        next_move[1] = -1
    if(next_move[2]==-1 or next_move[2]==3 or next_move[2]==7 or next_move[2]==11):
        next_move[2] = -1
    if(next_move[3]==4 or next_move[3]==8 or next_move[3]==12 or next_move[3]==16):
        next_move[3]=-1
    
    #if there's no stench and breeze, all neighboring places are safe to move        
    if(status[pos][2]==0 and status[pos][3]==0):
        for k in range(4):
            if(next_move[k]!=-1):
                status[next_move[k]][1] = 1
                
    #Else compute which places are safe 
    else:
        #find diagonal elements upper_left, upper_right, lower_left, lower_right,
        d=np.array([pos+3,pos+5,pos-5,pos-3])
        if(d[0]==3 or d[0]==7 or d[0]==11 or d[0]>=15):
            d[0]=-1
        if(d[1]==8 or d[1]==12 or d[1]>=16):
            d[1]=-1
        if(d[2]<0 or d[2]==3 or d[2]==7):
            d[2] = -1
        if(d[3]<=0 or d[3]==4 or d[3]==8 or d[3]==12):
            d[3] = -1
        
        #for stench, if the diagonal space has been visited and does not have stench
        if(status[pos][2]==1):
            if(d[0]!=-1 and status[d[0]][0]==1 and status[d[0]][2]==0): #top and left are safe
                status[next_move[0]][1]=1
                status[next_move[2]][1]=1
            elif(d[1]!=-1 and status[d[1]][0]==1 and status[d[1]][2]==0): #top and right are safe
                status[next_move[0]][1]=1
                status[next_move[3]][1]=1
            elif(d[2]!=-1 and status[d[2]][0]==1 and status[d[2]][2]==0): #bottom and left are safe
                status[next_move[1]][1]=1
                status[next_move[2]][1]=1
            elif(d[3]!=-1 and status[d[3]][0]==1 and status[d[3]][2]==0): #bottom and right are safe
                status[next_move[1]][1]=1
                #if(next_move[3]!=-1):
                status[next_move[3]][1]=1
        
        #for breeze, if the diagonal space has been visited and does not have breeze
        if(status[pos][3]==1):
            if(d[0]!=-1 and status[d[0]][0]==1 and status[d[0]][3]==0): #top and left are safe
                status[next_move[0]][1]=1
                status[next_move[2]][1]=1
            elif(d[1]!=-1 and status[d[1]][0]==1 and status[d[1]][3]==0): #top and right are safe
                status[next_move[0]][1]=1
                status[next_move[3]][1]=1
            elif(d[2]!=-1 and status[d[2]][0]==1 and status[d[2]][3]==0): #bottom and left are safe
                status[next_move[1]][1]=1
                status[next_move[2]][1]=1
            elif(d[3]!=-1 and status[d[3]][0]==1 and status[d[3]][3]==0): #bottom and right are safe
                status[next_move[1]][1]=1
                status[next_move[3]][1]=1
        
    while(True):
        elf = random.choice([0,0,0,1,2,3])
        if(status[next_move[elf]][1]==1 and prev2!=next_move[elf]):
            break
    find_gold(prev,pos,next_move[elf])                
                       
def escape_cave(pos):
    if(pos==0):
        print("Made a successful escape.")
        return
    
    #compute top, bottom, left, right
    next_move=np.array([pos+4,pos-4,pos-1,pos+1])
    if(next_move[0]>15):
        next_move[0] = -1
    if(next_move[1]<0):
        next_move[1] = -1
    if(next_move[2]==-1 or next_move[2]==3 or next_move[2]==7 or next_move[2]==11):
        next_move[2] = -1
    if(next_move[3]==4 or next_move[3]==8 or next_move[3]==12 or next_move[3]==16):
        next_move[3]=-1
    
    #give bottom more priority
    if(next_move[1]!=-1 and status[next_move[1]][0]==1):
        pos=next_move[1]
    
    else:
        while(True):
            elf = random.choice([0,2,2,2,3])
            if(status[next_move[elf]][0]==1 and next_move[elf]!=-1):
                pos=next_move[elf]
                break
            
    x=str(int(pos/4+1))
    y=str(int(pos%4+1))
    strn='['+x+','+y+']'
    print("Moved to",strn)
    escape_cave(pos)
    
if __name__ == "__main__":
    arrows=1
    wumpus = np.array([8])
    gold = 9
    pit = np.array([2,10,15])
    #0 indicates unkown, 1 indicates safe and -1 indicates dangerous and -2 indicates potentially dangerous
    #0 indicates whether it has been visited, 1 indicates safe, 2 indicates stench, 3 indicates breeze
    status = np.array([0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0])
    status = np.reshape(
               status,     # the array to be reshaped
               (16,4)  # dimensions of the new array
              )
    points=1000
    status[0][1]=1
    key = find_gold(-1,-1, 0)
    print("\n")
    if key !=-1:
        escape_cave(gold)

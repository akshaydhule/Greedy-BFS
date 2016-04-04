'''
	Part-I of 3 parts
	This program returns next step prediction which results best value using greedy best first algorithm
	for board games given the samples
'''

import sys
import os
adjmat = []
valmat = []
signmat = []
playerlist = []
oppolist = []
player_adj = []

def admat():
    for i in range(0,5):
        for j in range(0,5):
            if(signmat[i][j]=='X' or signmat[i][j]=='O'):
                adjmat.append((i,j))
            else:
                if(outofbound(i+1, j)==1 and (signmat[i+1][j]=='X' or signmat[i+1][j]=='O')):
                    adjmat.append((i,j))
                        
                elif(outofbound(i-1, j)==1 and (signmat[i-1][j]=='X' or signmat[i-1][j]=='O')):
                    adjmat.append((i,j))
                        
                elif(outofbound(i, j+1)==1 and (signmat[i][j+1]=='X' or signmat[i][j+1]=='O')):
                    adjmat.append((i,j))
                        
                elif(outofbound(i,j-1)==1 and (signmat[i][j-1]=='X' or signmat[i][j-1]=='O')):
                    adjmat.append((i,j))
    return adjmat
     
def outofbound(i,j):
    if (i<0 or i>4 or j<0 or j>4):
        return 0
    return 1

def adjlist (list, notlist):
    adjmatrix = []
    for index in list:
        i = index[0]
        j = index[1]
        if(outofbound(i+1, j)==1 and ((i+1,j) not in oppolist) and ((i+1,j) not in playerlist)):
            adjmatrix.append((i+1,j))
        if(outofbound(i-1, j)==1 and ((i-1,j) not in oppolist) and ((i-1,j) not in playerlist)):
            adjmatrix.append((i-1,j))
        if(outofbound(i, j+1)==1 and ((i,j+1) not in oppolist) and ((i,j+1) not in playerlist)):
            adjmatrix.append((i,j+1))
        if(outofbound(i, j-1)==1 and ((i,j-1) not in oppolist) and ((i,j-1) not in playerlist)):
            adjmatrix.append((i,j-1))
    return adjmatrix        


def sneak():
    maxvalue =0
    sneaklist = []
    n=0
    m=0
    for i in range(0,5):
        for j in range(0,5):
            if(i==4 & j==4):
                break
            else:
                val = int(valmat[i][j])
                if((val>maxvalue) and ((i,j) not in playerlist) and ((i,j) not in oppolist)):
                    maxvalue = val
                    n=i
                    m=j
    sneaklist.append(maxvalue)
    sneaklist.append((n,m))
    return sneaklist


def raidval(index):
    raidvalue =0
    i = index[0]
    j = index[1]
    if (outofbound(i, j)==1):
        raidvalue = int(valmat[i][j])
        if(outofbound(i+1, j)==1 and ((i+1,j) in oppolist)):
            raidvalue += int(valmat[i+1][j]) 
        if(outofbound(i-1, j)==1 and ((i-1,j) in oppolist)):
            raidvalue += int(valmat[i-1][j])
        if(outofbound(i, j+1)==1 and ((i,j+1) in oppolist)):
            raidvalue += int(valmat[i][j+1])
        if(outofbound(i, j-1)==1 and ((i,j-1) in oppolist)):
            raidvalue += int(valmat[i][j-1])
    return raidvalue

def raid(list):
    raidlist =[]
    m=0
    n=0
    maxvalue =0     
    for index in list:
        val = raidval(index)
        if(val>maxvalue):
            maxvalue = val
            m=index[0]
            n=index[1]
    raidlist.append(maxvalue)
    raidlist.append((m,n))
    return raidlist

    
def main():  
    global adjmat
    global valmat
    global signmat
    global playerlist
    global oppolist
    global player_adj
    nosign = 'O'  
    counter =0
    sign = ''
    path = sys.argv[2]
    f = open (path,'r')
    al = f.readline()
    algo = int(al)
    if(algo == 4):
        firstsign = f.readline()
        firstalgo = f.readline()
        firstdepth =  f.readline()
        secsign = f.readline()
        secalgo = f.readline()
        secdepth =  f.readline()
    else:
        sign = f.readline()
        if(sign.find('O')!=-1):
            nosign = 'X'
        depth = f.readline()
    for line in f.readlines():
        counter = counter + 1
        if (counter<=5):
            valmat.append(line.split(' '))
               
        elif(counter<=10):
            li = []
            li = list(line)
            signmat.append(li)
        else:
            f.close()
    
    #create player list
    xlist = []
    olist = []
    for i in range(0,5):
        for j in range(0,5):
            if(sign.find('X')!=-1):
                if((signmat[i][j])=='X'):
                    playerlist.append((i,j))
                if(signmat[i][j]=='O'):
                    oppolist.append((i,j))
            if(sign.find('O')!=-1):
                if((signmat[i][j])=='O'):
                    playerlist.append((i,j))
                if(signmat[i][j]=='X'):
                    oppolist.append((i,j))
    
    adjmat = admat()           
    player_adj = adjlist(playerlist,oppolist)
    
    sneakvaluelist = sneak()
    sneakindex = sneakvaluelist[1]
    raidvaluelist = raid(player_adj)
    raidindex = raidvaluelist[1]
    if((sneakvaluelist[0]>raidvaluelist[0])): #check if raid or sneak
        signmat[sneakindex[0]][sneakindex[1]] = sign.strip()
    elif((sneakvaluelist[0]==raidvaluelist[0]) and (sneakindex[0]<=raidindex[0])):
        if(sneakindex[1]<=raidindex[1]):
            signmat[sneakindex[0]][sneakindex[1]] = sign.strip() 
    else:
        index = raidvaluelist[1]
        i = index[0]
        j = index[1]
        signmat[i][j] = sign.strip()
        if(outofbound(i+1, j)==1 and ((i+1,j) in oppolist)):
            signmat[i+1][j] = sign.strip()
        if(outofbound(i-1, j)==1 and ((i-1,j) in oppolist)):
            signmat[i-1][j] = sign.strip()
        if(outofbound(i, j+1)==1 and ((i,j+1) in oppolist)):
            signmat[i][j+1] = sign.strip()
        if(outofbound(i, j-1)==1 and ((i,j-1) in oppolist)):
            signmat[i][j-1] = sign.strip()
    f = open('next_state.txt','w')    
    for i in range(0,5):
        for j in range(0,5):
            f.write(signmat[i][j])
        f.write('\n')
    f.close()
'''    
    f = open('traverse_log.txt','w')
    f.close()

    f = open('trace_state.txt','w')
    f.close()
'''
main()


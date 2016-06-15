import sys
import argparse
from tree import Node
V=[]
#takes a string. splits it on "->" first and on every "|" after.
#creates a dict entity with the variable name and the productions array.
def parseProduction(s):
    s=s.split("->")
    varName = s[0];
    s=s[1]
    s=s.split("|")
    prods = {i for i in s}
    var = {'name':varName,'productions':prods}
    return var

#parse the grammar.
#takes a string representing the grammar, splits it on newlines and parse newlines
def buildGrammar(G,Vi):
    grammar= G.read().splitlines()
    for p in grammar:
        rule=parseProduction(p)
        Vi.append(rule)

#return a list variables that have the argument string in their productions
def searchProd(s):
    possibleFathers=[];

    for v in V:#V is the dict {VARIABLE -> [PRODUCTIONS]}
        for p in v['productions']:
            if (p==s):
               possibleFathers.append(v['name'])#you're the father!
    return possibleFathers;



def cyk(stri, matr, nodeMatr):

    ##single chars#special case
    for j in xrange(0, len(stri)):
        lastBeforeTerminal = searchProd(stri[j])
        if len(lastBeforeTerminal)==0:#if the list of possible Variables responsible for a terminal is empty
            return False#then the string is not in the grammar
        else:
            #fills the principal diagonal with the starting variables
            #bit of a mess here
            possible=searchProd(stri[j])
            matr[j][j]=possible
            nodeMatr[j][j]=[]
            for p in possible:
                nodeMatr[j][j].append(Node(p, [Node(stri[j], None)]))

    #######################################
    '''
    nodeMatr is a len(string) x len(string) matrix
    The principal diagonal now has all the variables that produced the terminals
    The loop over the matrix will visit the diagonal on the right of the principal diagonal first
    then will move on the  other diagonal on the right
    like this:
    [ ][ ][ ][0]
    [ ][ ][0][1]
    [ ][0][1][2]
    [0][1][2][3]
    '''
    for d in xrange(1, len(stri)):
        for m in xrange(0, len(stri)-d):
            i=m#y index of the matrix
            j=m+d#x index of the matrix


            possibleProductions=[]
            s=[]
            sMat=[]
            nodes=[]

            #first time t=[0,1],second t=[0,1,2],...,last t=[0,...,len(string)]
            for t in xrange(0,d):
                #select pair ([i][i+t] ,[i+t+1][j]) of cells in the matrix
                for pL in nodeMatr[i][i+t]:
                    for pR in nodeMatr[i+t+1][j]:
                        #for each node inside the cell
                        productions=combineProd(pL.name,pR.name)#   combine them
                        possibleProductions.append([productions,pL,pR])# append productions along with a reference to the nodes that created it

            for comb in possibleProductions:#for each triple [[production1,...],parent1,parent2]
                for production in comb[0]:
                    fathers=searchProd(production)#look in the grammar for a possible generator
                    if(len(fathers)>0):
                        for f in fathers:#for every generator
                            node = Node(f,[comb[1],comb[2]])#create a new node , give it the 2 sons
                            comb[1].setParent(node)#set its parent
                            comb[2].setParent(node)#set its parent
                            nodes.append(node)#append it to the list of nodes that will go inside the [i][j] cell
                            s.append(f)
                            if(sMat.__contains__([comb,f])==False):
                                sMat.append([comb,f])
            nodeMatr[i][j]=nodes
            matr[i][j]= list(set(s)) #removes duplicates
    #prettyPrint(matr)
    #nodePrint(nodeMatr)
    if 'S' in matr[0][len(stri)-1]:#starting symbol is inside the last cell!
        return True
    return False

def prettyPrint(m):
    s = len(m)
    for i in reversed(xrange(0,s)):
            print m[i]

def nodePrint(m):
    s = len(m)
    for i in reversed(xrange(0,s)):
        s=''
        for j in m[i]:
            s+='['
            for l in j:
                s+=str(l)+"|"
            s+=']'
        print s


def buildMatrix(size,type):
    m=[]
    for i in xrange(0,size):
        m.append([type for k in xrange(0,size)])
    return m

#combine productions. ie : combineProd('A','B') returns ['AA','AB','BA','BB']
def combineProd(s1,s2):
    s=[]
    for j in s1:
        for k in s2:
            s.append(""+j+k)
    return s

def simpleVisit(matrix):
    for i in matrix[0][len(matrix[0])-1]:
        if(i.name=='S'):
            starting = i
    starting.pPrint("")

#########################################
#Grammar in the form "VAR->prod1|prod2|..."
#rules are separeted with newlines
#currently supports ONLY single char terminals

def main():

    parser = argparse.ArgumentParser(description='CKY Algorithm')
    parser.add_argument('directory', action="store",help="path for the grammar file")
    parser.add_argument('str', action="store",help="string to check")
    parser.add_argument('-t', action="store_true",default=False,help="Prints the derivation tree on console")


    args=parser.parse_args()
    path = args.directory
    string=str(args.str)
    tree=args.t
    G=open(path,'r')

    matr = buildMatrix(len(string),0)#this was the first matrix, when it was just a recoginzer
    nodeMatr = buildMatrix(len(string),[])#this is the new one
    buildGrammar(G,V)

    out=cyk(string,matr,nodeMatr)

    if(out and tree):
        simpleVisit(nodeMatr)

    return out


if __name__ == "__main__":
    main()

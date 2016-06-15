class Node:

    def __init__(self,name,children):
        self.name=name
        self.parent=[]
        self.children=[]
        if children!=None:
            for g in children:
                #for k in g:
                self.children.append(g)
    def __str__(self):
        s=''
        for k in self.children:
            if(type(k)==str):
                s+=k
            else:
                s+=k.name
        #s = ''.join(str(self.children))
        j= ''.join([i.name for i in self.parent]) if(len(self.parent)>0) else "0"
        k=len(self.parent)
        return s+"<-"+self.name+"<-"+j
    def setParent(self,f):
          self.parent.append(f)
    def hasParent(self):
        return len(self.parent)>0
    #shouldnt be used
    def setChildren(self,children):
        self.children=children
    def isLeaf(self):
        return self.children==None
    def pPrint(self,pref):
        print pref+"+--- "+self.name+" "
        for n in self.children:
            if n==self.children[len(self.children)-1]:
                n.pPrint(pref+"     ")
            else:
                n.pPrint(pref+"     |")





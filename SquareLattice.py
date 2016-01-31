import numpy
from math import factorial

a1=numpy.array([1,0])
a2=numpy.array([0,1])
Nx=4
Ny=4
t=1


def realDist(a,b):
    diff=a-b
    minVal=numpy.sqrt(numpy.dot(diff,diff))
    return minVal

def dist(a,b):
    diff=a-b
    minVal=numpy.sqrt(numpy.dot(diff,diff))
    for ix in range(-1,2):
        for iy in range(-1,2):
            newDiff=diff+ix*a1*Nx+iy*a2*Ny
            newVal=numpy.sqrt(numpy.dot(newDiff,newDiff))
            minVal=min(minVal,newVal)
    return minVal

def CreateKPoints(Nx,Ny,a1,a2):
    N1=int(Nx)
    N2=int(Ny)
    kPoints=[]
    k1=numpy.array([2*numpy.pi/(N1*a1[0]),0.])
    k2=numpy.array([0.,2*numpy.pi/(N2*a2[1])])
    for kxi  in range(-N1/2,N1/2):
        for kyi in range(-N2/2,N2/2):
            k=numpy.array(kxi*k1+kyi*k2)
            print "k-value: ",k[0],k[1],kxi,kyi
            kPoints.append([k[0]/Nx,k[1]/Ny])
    return kPoints

def CreatePoints(a1,a2,Nx,Ny):
    N1=int(Nx)
    N2=int(Ny)
    myPoints=[]
    for i in range(-N1/2,N1/2):
        for j in range(-N2/2,N2/2):
            thePoint=a1*i+a2*j
            myPoints.append(numpy.array([thePoint[0],thePoint[1]]))
    return myPoints

def CreateNeighbors(myPoints,minDist):
    H=numpy.zeros((len(myPoints),len(myPoints)),float)
    neighbors=[]
    for i in range(0,len(myPoints)):
        neighbors.append([])
    for i in range(0,len(myPoints)):
        for j in range(0,len(myPoints)):
            if abs(dist(myPoints[i],myPoints[j])-minDist)<1e-5:
                neighbors[i].append(j)
                H[i,j]=-t
    return (neighbors,H)

myPoints=CreatePoints(a1,a2,Nx,Ny)
myFile=open("rPoints.txt",'w')
myFile.write(str(a1[0])+" "+str(a1[1])+"\n")
myFile.write(str(a2[0])+" "+str(a2[1])+"\n")
myFile.write(str(int(Nx))+"\n")
myFile.write(str(int(Ny))+"\n")
for i in myPoints:
    print i
    myFile.write(str(i[0]))
    myFile.write(" ")
    myFile.write(str(i[1]))
    myFile.write("\n")
myFile.close()

#HACK! MOVING K POINTS SOONER
kPoints=list(CreateKPoints(Nx,Ny,a1,a2))

myFile=open("kPoints.txt",'w')
for i in kPoints:
        myFile.write(str(i[0]))
        myFile.write(" ")
        myFile.write(str(i[1]))
        myFile.write("\n")
myFile.close()

#DONE HACK!


(myNeighbors,H)=CreateNeighbors(myPoints,a1[0])

myFile=open("neighbors.txt",'w')
for i in range(0,len(myNeighbors)):
    myFile.write(str(i))
    myFile.write(" ")
    myFile.write(str(len(myNeighbors[i])))
    myFile.write(" ")
    for j in myNeighbors[i]:
        myFile.write(str(j))
        myFile.write(" ")
    myFile.write("\n")
myFile.close()
kPoints=list(CreateKPoints(Nx,Ny,a1,a2))

myFile=open("kPoints.txt",'w')
for i in kPoints:
        print i
        myFile.write(str(i[0]))
        myFile.write(" ")
        myFile.write(str(i[1]))
        myFile.write("\n")
myFile.close()

myFile=open("bonds.txt",'w')
for i in range(len(myNeighbors)):
    for j in myNeighbors[i]:
        if i < j:
            myFile.write(str(i)+" "+str(j)+"\n")
myFile.close()

myFile=open("corrs.txt",'w') # nearest neighbor correlators
myFile.write(str(Nx*Ny*2)+"\n")
for i in range(len(myNeighbors)):
    for j in range(len(myNeighbors)):#myNeighbors[i]:
        if i < j:
            myFile.write("2 "+str(i)+" "+str(j)+"\n")
myFile.close()


(a,b)=numpy.linalg.eigh(H)
print "EIGS",a

print numpy.shape(a),numpy.shape(b)
myFile=open("eigs.txt",'w')
zerosUsed=0
for i in range(0,len(a)):
    if a[i]<0:  # or 1==1:
        for j in range(0,len(b[:,i])):
            myFile.write(str(b[j,i]))
            myFile.write(" ")
        myFile.write("\n")
myFile.write("\n")
myFile.write("\n")
myFile.write("\n")
myFile.write("\n")
myFile.write("\n")
for i in range(0,len(a)):
    if a[i]>0 and a[i]<1e-10:
        for j in range(0,len(b[:,i])):
            myFile.write(str(b[j,i]))
            myFile.write(" ")
        myFile.write("\n")


myFile.close()

import os
import numpy as np
import random
import math

def getBlank(arr):
  for i in range(3):
    for j in range(3):
      if(int(arr[i][j])==0):
        x,y=i,j
  print(x,y)
  return x,y

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def createPuzzle():
  return np.zeros((3, 3))

def printPuzzle(arr):
  for i in range(3):
    for j in range(3):
      print(int(arr[i][j]),end=" ")
    print()
  print()

def shufflePuzzle():
  arr=createPuzzle()
  for i in range(1,9):
    k=random.randint(0,2)
    l=random.randint(0,2)
    while(arr[k][l]!=0):
      k=random.randint(0,2)
      l=random.randint(0,2)
    arr[k][l]=i
  return arr

def isFree(arr,i,j):
  freeBool=False
  x,y=getBlank(arr)
  if((i==x and abs(j-y)==1) or (j==y and abs(i-x)==1)):
    freeBool=True
  return freeBool
  

if __name__=="__main__":
  game=True
  
  puzzle=createPuzzle()
  printPuzzle(puzzle)
  
  puzzle=shufflePuzzle()
  printPuzzle(puzzle)
  
  puzzle=shufflePuzzle()
  printPuzzle(puzzle)
  
  while(game):
    #clearConsole()
    printPuzzle(puzzle)
    i,j=input("Give i and j").split()
    if(isFree(puzzle,i,j)==True):
      print("free")
      x,y=getBlank(puzzle)
      puzzle[i][j],puzzle[x][y]=puzzle[x][y],puzzle[i][j]
    
    

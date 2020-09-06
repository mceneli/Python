import numpy as np
from random import randrange
import random
import time
import os

#program her calistirildiginda h yüksekliginde, w genisliginde
#start ve end noktalarini bos birakacak sekilde rastgele labirent uretir
def make_maze(h,w,k,startX,startY,endX,endY):
    #her yeri 1, yani duvar olan labirent olusturur
    maze = np.ones((h,w), dtype="int")
    
    #olusturulan labirentin kenarlari disinda içini 0 yapar, yani bosaltir
    for i in range(1,h-1):
        for j in range(1,w-1):
            maze[i][j] = 0
    
    #bu dongu icerisinde cakismayacak sekilde labirente k adet 4x1 engel yerlestirilir
    for i in range(k):
        isHorizontal = randrange(2)
        
        count = 0
        
        #engeller rastgele uretilen degere gore yatay veya dusey yerlestirilir
        if isHorizontal:
            while count < 1:
                x = randrange(1,h-5)
                y = randrange(1,w)
 
                cakisti = 0
                for j in range(4):
                    if maze[x+j][y] == 1 or (x == startX and y == startY) or (x == endX and y == endY):
                        cakisti = 1
                
                if cakisti == 0:
                    for j in range(4):
                        maze[x+j][y] = 1
                    count = count + 1
        else:
            while count < 1:
                x = randrange(1,h)
                y = randrange(1,w-5)
                
                cakisti = 0
                for j in range(4):
                    if maze[x][y+j] == 1 or (x == startX and y == startY) or (x == endX and y == endY):
                        cakisti = 1
                
                if cakisti == 0:
                    for j in range(4):
                        maze[x][y+j] = 1
                    count = count + 1
    return maze

#n adet ve gen uzunlugu m olan populasyon olusturur genlerini 1,2,3, veya 4 olacak sekilde rastgele uretir.
def createPopulation(n,m):
    population = np.zeros((n,m))
    
    for i in range(n):
        for j in range(m):
            population[i][j] = randrange(1,5)

    return population

#cikisa olan yakinliga ve gidilen adim sayisina gore hangi bireyin daha iyi oldugunu secen fonksiyon
#ekrana bastirma islemleri de bu fonksiyon icerisinde yapiliyor.
def fitness_function(population,maze,startX,startY,endX,endY):
    #values icerisinde atilan adim sayisini ve cikisa olan uzakligi saklayan dizidir.
    values = np.zeros((population.shape[0],2))
    
    for i in range(population.shape[0]):
        x = startX
        y = startY
        j = 0
        #print(maze)
        
        #siradaki bireyin duvara carpmadan kac adim ve hangi konuma gittigini hesaplar
        while(maze[x][y] == 0 and (x != endX or y != endY) and (j < population.shape[1]) ):
            if(population[i][j]) == 1:
                y = y - 1
            elif(population[i][j]) == 2:
                x = x - 1
            elif(population[i][j]) == 3:
                y = y + 1
            else:
                x = x + 1
            j = j + 1
            #print("maze",maze[x][y]," (",x,y,") ",j)
        
        #bireyin adim sayisi ve uzakligi values icerisine kaydedilir
        values[i][0] = j - 1
        #values[i][1] = ( (endY - y) ** 2 + (endX - x) ** 2 ) ** (1 / 2)
        values[i][1] = (endY - y) ** 2 + (endX - x) ** 2 

#ekrana bastirma islemleri
###############################print#########################################################################
    #jenerasyon icerisindeki en iyi bireyi bulur
    
    indis = 0
    #print(values)
    min = 9999
    for ind in range(values.shape[0]):
        if( values[i][0] + values[i][1] < min):
            min = values[i][0] + values[i][1]
            indis = int(ind)
    #print(population)
    #print("indis ",indis)    
    #print(int(max))
    j=0
    xx=startX
    yy=startY
    tmpmaze = np.zeros((maze.shape),dtype="int")
    
    for ii in range(maze.shape[0]):
        for jj in range(maze.shape[1]):
            tmpmaze[ii][jj] = maze[ii][jj]
    
    for ii in range( int( values[indis][0] ) ):
        tmpmaze[xx][yy] = 7
        
        if(population[indis][j]) == 1:
            yy = yy - 1
        elif(population[indis][j]) == 2:
            xx = xx - 1
        elif(population[indis][j]) == 3:
            yy = yy + 1
        else:
            xx = xx + 1
            
        if(xx == endX and yy == endY):
            print("cozuldu")
            time.sleep(1)
        j = j + 1
    
    #jenerasyon icerisindeki en iyi bireyin yolu ve adim sayisi ekrana yazdirilir
    print("adim sayisi ",int( values[indis][0] ) )
    for ii in range(maze.shape[0]):
        for jj in range(maze.shape[1]):
            if tmpmaze[ii][jj] == 1:
                print("# ",end="")
            elif tmpmaze[ii][jj] == 7:
                print("* ",end="")
            else:
                print("  ",end="")
        print("")
    
    time.sleep(1)
    os.system('cls')
#########################################################################################################        
    #yeni populasyon olusturulur    
    new_population = np.zeros( (population.shape[0],population.shape[1] + 1) )
    new_population[:,:-1] = population
    
    for i in range(new_population.shape[0]):
        #new_population[i][new_population.shape[1] - 1] = (population.shape[1] - values[i][0]) + values[i][1]
        new_population[i][new_population.shape[1] - 1] = values[i][0] + values[i][1]
        #new_population[i][new_population.shape[1] - 1] =  values[i][1]
    
    #populasyon en iyi birey en asagida olacak sekilde siralanir
    new_population = new_population[np.argsort(new_population[:, new_population.shape[1] - 1])]
    #print(new_population)
    
    new_population = np.flip(new_population, 0)
    #print(new_population)
    
    new_population = np.delete(new_population, new_population.shape[1] - 1, 1)
    #print(new_population)
    
        
    #print(values)
    population = new_population
    
    return population,values

# populasyonda 10 birey varsa rastgele 10*11/2 araliginda sayi secilir ve hesaplama yapilip iyi bireyin secilme olasiligi su sekilde ayarlanir
# 1 22 333 4444 55555    soldaki gibi en altta kalan birey daha buyuk araliga sahiptir rastgele secilen sayinin hangi bireye denk geldigi secildiginde
# asagidaki bireylerin daha cok secilme sansi vardir
def sorted_selection(population_count):
    #i = randrange(1, population_count + 1)
    lngth = int( (population_count * (population_count + 1) ) / 2 )
    indis = randrange(0,lngth)
    i = 0
    while (i * (i + 1) ) / 2 < indis:
        i = i + 1
    
    return i - 1

#yeni populasyon olusturulurken rastgele sayi uretilip karsilik gelen 2 birey crossover gecirir
#crossover islemi secilen ilk bireyin duvara carpmadan gittigi mesafe den yapilir
#her kopyalama isleminde %1 mutasyon ihtimali vardir
def crossover(population, values):
    new_population = np.zeros(population.shape)
    
    for i in range(new_population.shape[0]):
        indis1 = sorted_selection(population.shape[0])
        indis2 = sorted_selection(population.shape[0])
        
        #bolum = random.randint(1, population.shape[1] - 1)
        bolum = int( max( values[indis1][0], values[indis2][0]  ) )
        
        for j in range(0, bolum ):
            randm = random.randint(1, 100)
            if(randm<2):
                new_population[i][j] = random.randint(1, 4)
            else:
                new_population[i][j] = population[indis1][j]
            
        for j in range( bolum , int( population.shape[1] ) ):
            randm = random.randint(1, 100)
            if(randm<2):
                new_population[i][j] = random.randint(1, 4)
            else:
                new_population[i][j] = population[indis2][j]
        
    return new_population


if __name__ == '__main__':
    mazeH = 20        #labirent yuksekligi
    mazeW = 20       #labirent genisligi
    mazeK = 10         #labirent icerisine koyulacak engel sayisi
    startX = 1         #baslangic x konumu
    startY = 1         #baslangic y konumu
    endX = mazeH - 2   #bitis x konumu
    endY = mazeW - 2   #bitis y konumu
   
    population_count = 50  #populasyondaki birey sayisi
    M = 51                 #populasyondaki bireylerin gen uzunlugu
    
    maze = make_maze(mazeH,mazeW,mazeK,startX,startY,endX,endY)
    #print(maze)
    """for ii in range(maze.shape[0]):
        for jj in range(maze.shape[1]):
            if maze[ii][jj] == 1:
                print("# ",end="")
            elif maze[ii][jj] == 7:
                print("* ",end="")
            else:
                print("  ",end="")
        print("")
    time.sleep(5)"""
    
    population = createPopulation(population_count,M)
    #print(population)
    
    generation = 1
    solved = 0
    while solved == 0:
        population ,values = fitness_function(population,maze,startX,startY,endX,endY)
        print(generation,". generation")
        
        population = crossover(population, values)
        
        for i in range(population_count):
            x = startX
            y = startY
            j = 0
            while(maze[x][y] == 0 and (x != endX or y != endY) and (j < M) ):
                if(population[i][j]) == 1:
                    y = y - 1
                elif(population[i][j]) == 2:
                    x = x - 1
                elif(population[i][j]) == 3:
                    y = y + 1
                else:
                    x = x + 1   
                j = j + 1
                if(x == endX and y == endY):
                    solved = 1
                    cozumindisi = i
                    cozumuzunlugu = j
        generation = generation + 1
            
    os.system('cls')
    print(generation,". jenerasyonda cozuldu")
    print("adim sayisi=",cozumuzunlugu)
    

    xx=startX
    yy=startY
    tmpmaze = np.zeros((maze.shape),dtype="int")
    
    #cozum bireyinin gittigi yol matrise kaydedilip ekrana yazdirilir
    for ii in range(maze.shape[0]):
        for jj in range(maze.shape[1]):
            tmpmaze[ii][jj] = maze[ii][jj]
   
    for ii in range( int( cozumuzunlugu + 1 ) ):
        tmpmaze[xx][yy] = 7
        
        if(population[cozumindisi][ii]) == 1:
            yy = yy - 1
        elif(population[cozumindisi][ii]) == 2:
            xx = xx - 1
        elif(population[cozumindisi][ii]) == 3:
            yy = yy + 1
        else:
            xx = xx + 1
    
    for ii in range(maze.shape[0]):
        for jj in range(maze.shape[1]):
            if tmpmaze[ii][jj] == 1:
                print("# ",end="")
            elif tmpmaze[ii][jj] == 7:
                print("* ",end="")
            else:
                print("  ",end="")
        print("")


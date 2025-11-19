import time
    
class BBS:

# Blum Blum Shub (B.B.S.) is a pseudorandom number generator
# proposed in 1986 by Lenore Blum, Manuel Blum and Michael Shub.
# M = pq is the product of two large primes p and q.
# The seed x0 should be an integer that is co-prime to M
# (i.e. p and q are not factors of x0) and not 1 or 0.
# The two primes, p and q, should both be congruent to 3 (mod 4)
# (this guarantees that each quadratic residue has one square root
# which is also a quadratic residue), and should be safe primes
# with a small gcd((p-3)/2, (q-3)/2) (this makes the cycle length large).
# Source: https://en.wikipedia.org/wiki/Blum_Blum_Shub
    
    def __init__(self, p = 982451819, q = 982451863):
        # generišemo seed uz pomoć sistemskog vremena
        seed = int(time.time()*1000)        # time() vrati u sekundama -> pretvorimo u milisekunde
        seed = 4*(seed//4) + 3              # treba da bude 3 (mod 4)
        while seed % p == 0 or seed % q == 0:
            seed = seed - 4
        self.m = p * q
        self.x = seed

    def parity(self, x):
        p = 0
        while x > 0:
            p = p ^ (x & 1)
            x = x >> 1
        return p
       
    def nextValue(self):
        # return random value 1..6
        while True:
            r = 0
            for i in range(3):    
                self.x = (self.x**2) % self.m
                r = (r << 1) | self.parity(self.x)
            if r < 6:
                return r+1

class Dices:
    def __init__(self, v = [0] * 5):
        self.n = len(v)
        self.v = v
        self.f = [1] * self.n # 1=menjamo, 0=zadržimo prethodnu vrednost
        self.count = [0] * 6
        for i in range(0,self.n):
            t = self.v[i] - 1 
            self.count[t] = self.count[t] + 1
        self.rnd = BBS()

    def reset(self):
        self.v = [0] * self.n
        self.f = [1] * self.n
        self.count = [0] * 6
    
    def roll(self):
        self.count = [0] * 6
        for i in range(0,self.n):
            if self.f[i] == 1:
                self.v[i] = self.rnd.nextValue()
            t = self.v[i] - 1 
            self.count[t] = self.count[t] + 1
        return self.v
    
    def hold(self,k):
        self.f[k]=0
    
    def release(self,k):
        self.f[k]=1
                    
    def isJamb(self):
        for i in range(6):
            if self.count[i] == 5:
                return i + 1
        return None
    
    def isPoker(self):
        for i in range(6):
            if self.count[i] >= 4:
                return i + 1
        return None
    
    def getCount(self,k):
        return self.count[k-1]
    
    def isKenta(self):
        # od 2..5 moraju da se pojavi tačno jednom
        for i in range(2,6):
            if self.getCount(i)!=1:
                return None
        return 1 # nije bitno da li je mala ili velika
    
    def isFul(self):
        # jamb se ne gleda kao ful (brojevi moraju biti različiti tj 3+2)
        a = 0 
        b = 0
        for i in range(6):
            if self.count[i] == 3:
                a = i + 1
            if self.count[i] == 2:
                b = i + 1
        if a > 0 and b > 0:
            return (a,b)
        return None

    def isGoalFulfilled(self,goal):
        if goal == "K" and self.isKenta():
            return True
        if goal == "P" and self.isPoker():
            return True
        if goal == "F" and self.isFul():
            return True
        if goal == "J" and self.isJamb():
            return True
        return False

class Board:
    ROWS = 10 # broj redova (bez poslednjeg)
    COLS = 3 # broj kolona
    MAX_THROWS = 3 # max broj bacanja

    def __init__(self):
        self.score=CoordinateList(self.ROWS + 1,self.COLS) # upisane vrednosti
        self.value=CoordinateList(self.ROWS + 1,self.COLS) # opcije za upisivanje vrednosti
        self.dices=Dices()
        self.format="CooList"
        # setiramo zbir kolona na 0
        for col in range(self.COLS):
            self.score.set(self.ROWS,col,0) 

    def render(self, i, j):
        score = self.score.get(i,j)
        if score != None:
           return str(score)
        value = self.value.get(i,j)
        if value != None:
            return "[{:s}]{:>3s}".format(self.getKey(i,j), str(value))
        return ""

    def sumOfRows(self,col,startrow,endrow):
        s = 0
        for row in range(startrow,endrow):
            val = self.score.get(row,col)
            if val != None:
                s = s + val
        return s
        
    def showBoard(self):
        labels=["1", "2", "3", "4", "5", "6", "Kenta", "Ful", "Poker", "Jamb", "Ukupno"]
        print()
        print("-----------------------------------------")
        print("| {:7s} | Na dole | Na gore |  Ručna  |".format(self.format))
        print("-----------------------------------------")
        for i in range(0,self.ROWS + 1):
            if i == 6: 
                print("-----------------------------------------")
                print("| {:>7s} | {:>7s} | {:>7s} | {:>7s} |".format("Zbir",str(self.sumOfRows(0,0,6)),str(self.sumOfRows(1,0,6)),str(self.sumOfRows(2,0,6))))
                print("-----------------------------------------")
            if i == self.ROWS:
                print("-----------------------------------------")
            print("| {:>7s} | {:>7s} | {:>7s} | {:>7s} |".format(labels[i],self.render(i,0),self.render(i,1),self.render(i,2)))
        print("-----------------------------------------")
    
    def calculateValue(self, row):
        # prvih 6 redova
        for i in range(6):
            if row == i:
                return self.dices.getCount(i + 1)*(i+1)
        
        if row == 6:
            if self.dices.isKenta():
                return [66,56,46][self.throw - 1]
            else:
                return 0

        if row == 7:
            x = self.dices.isFul()
            if x:
                return 30 + 3*x[0] +2*x[1]
            else:
                return 0

        if row == 8:
            x = self.dices.isPoker()
            if x:
                return 40 + 4*x
            else:
                return 0

        if row == 9:
            x = self.dices.isJamb()
            if x:
                return 50 + 5*x
            else:
                return 0
            
        return 0
    
    def rollDice(self):
        self.throw = self.throw + 1
        result = self.dices.roll()
        
        for i in range(5):
            self.dices.hold(i)
            
        # upisemo mogucnosti
        options = 0
        self.value.clear() 
        col = 0
        for row in range(self.ROWS):
            if self.score.get(row,col) != None:
                continue
            v = self.calculateValue(row)
            if v != None and v != 0:              
                self.value.set(row,col,v)
                options = options+1
            break
        col = 1
        for row in range(self.ROWS - 1,-1,-1):
            if self.score.get(row,col) != None:
                continue
            v = self.calculateValue(row)
            if v != None and v != 0:              
                self.value.set(row,col,v)
                options = options+1
            break
        col = 2
        for row in range(self.ROWS):
            if self.score.get(row,col) != None:
                continue
            v = self.calculateValue(row)
            if v != None and v != 0 and self.throw == 1:
                self.value.set(row,col,v)
                options = options+1

        # ako ne može nigde da se upiše, precrtaj jedno polje po izboru
        if options == 0: 
            for col in range(self.COLS):
                for row in range(self.ROWS):
                    if self.score.get(row,col) != None:
                        continue
                    self.value.set(row,col,0)
                    
        return result
        
    def playRound(self):
        self.throw = 0
        self.dices.reset()

        print("Menu:")
        print("[1] Baci kocke")
        print("[2] Pomoć prijatelja")
        print("[N] Nova igra")
        print("[Q] Izlaz")
        while True:
            print("Opcija: ", end="")
            s = input().upper()
            if s == '1':
                player = Human()
                break
            if s == '2':
                player = Robot()
                break
            if s == 'N':
                raise StartNewGameException
            if s == 'Q':
                raise QuitGameException
        player.playRound(self)
        self.value.clear() 

    def play(self):
        for i in range(self.ROWS * self.COLS):  # broj poteza = ROWS*COLS
            self.showBoard()
            self.playRound()

            if self.format != "Matrix":
                sizeOfMatrix = self.ROWS * self.COLS + self.COLS # polja koja se upisuju + ukupan zbir
                sizeOfCoordinateList = (i+1)*3 + self.COLS*3; # 3*int za svaki upis (dva za koordinate i jedan za vrednost), plus dodatak za ukupan zbir
                if sizeOfCoordinateList > sizeOfMatrix:
                    self.score = self.score.toMatrix()
                    self.format = "Matrix"

        print("Kraj igre", end="")
        self.showBoard()
        total = 0
        for col in range(self.COLS):
            total = total + self.score.get(self.ROWS, col)
        print("Ukupan broj poena: ", total)
        print()

    def submit(self,key):
        for row in range(self.ROWS):
            for col in range(self.COLS):
                if self.getKey(row,col) == key and self.score.get(row,col) == None and self.value.get(row,col) != None:
                    self.score.set(row,col,self.value.get(row,col))
                    self.value.clear() 
                    # ispravimo zbir kolona            
                    for col in range(self.COLS):
                        self.score.set(self.ROWS,col,self.sumOfRows(col,0,self.ROWS))
                    return (row,col)
        return None
        
    def isEndOfRound(self):
        if self.throw < self.MAX_THROWS:
            return False
        return True

    def getKey(self,row,col):
        cols=['D','G','R']
        rows=['1','2','3','4','5','6','K','F','P','J']
        return "" + cols[col] + rows[row]
        
class Matrix:
    def __init__(self,m,n):
        self.a=[[None for j in range(0,n)] for i in range(0,m)]
        self.m=m
        self.n=n
            
    def get(self,i,j):
        return self.a[i][j]
    
    def set(self,i,j,val):
        self.a[i][j]=val
        
    def clear(self):
        self.a=[[None for j in range(0,self.n)] for i in range(0,self.m)]


class CoordinateList:
    def __init__(self,m,n):
        self.a=[] # lista koordinata 
        self.v=[] # lista vrednosti
        self.m=m
        self.n=n

    def find(self,x): # binarna pretraga pozicije koordinate x=(x[0],x[1]) u listi koordinata a
        # vraca se pozicija na kojoj je u listi a ili na kojoj bi trebalo da bude ukoliko je nema (da bi se tu upisala)

        if len(self.a) == 0:
            return 0
        if x < self.a[0]:
            return 0
        if self.a[-1] < x:
            return len(self.a)
        lo = 0
        hi = len(self.a) - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if x < self.a[mid]:
                hi = mid
            elif x > self.a[mid]:
                lo = mid + 1
            else:
                return mid
        return lo

    def get(self,i,j):
        x = (i,j)               # koordinata
        p = self.find(x)        # pozicija koordinate
        if p >= len(self.a):
            return None
        if x == self.a[p]: 
            return self.v[p]
        return None
    
    def set(self,i,j,val):
        x = (i,j)
        p = self.find(x)          # pozicija koordinate
        if p >= len(self.a):
            # koordinata je veca od poslednje upisane (ubacimo na kraj)
            self.a.append(x)        
            self.v.append(val)
        else:
            if x == self.a[p]:
                self.v[p] = val         # posto1ji (zamenimo vrednost)
            else:
                # ne postoji (umetnemo na poziciju p)                
                self.a.insert(p,x)      
                self.v.insert(p,val)    
    
    def clear(self):
        self.a=[]
        self.v=[]

    def toMatrix(self):
        matrix = Matrix(self.m,self.n)
        for i in range(len(self.a)): 
            x = self.a[i]
            val = self.v[i]           
            matrix.set(x[0],x[1],val)
        return matrix
    
class Human:
    def playRound(self,board):
        while True:
            dices = board.rollDice()
            
            print()
            print()
            print("Bacanje #" + str(board.throw) + ": ", end=" ")
            for d in dices:
                print(" "  + str(d) + " ", end=" ")
            print("\n            ", end=" ")
            for key in 'ABCDE':
                print("[" + key + "]", end=" ")
            print()

            if board.isEndOfRound():
                break
            
            print("\nUpiši koje kockice želiš da baciš ponovo ili <ENTER> da upišeš rezultat: ", end=" ")
            s = input().upper()
            if s == "":
                break

            for ch in s:
                if ch >= 'A' and ch <= 'E':
                    k = ord(ch) - ord('A')
                    board.dices.release(k)
                
        board.showBoard()
        while True:
            print("Gde da upišem rezultat: ", end="")
            s = input().upper()
            if board.submit(s) != None:
                break

class Robot:
    def playRound(self,board):
        dices = board.rollDice()        
        print()
        print("Bacanje #" + str(board.throw) + ":", end=" ")
        for d in dices:
            print(" "  + str(d) + " ", end=" ")
        print()

        # ako je u ručnoj opcija
        s = None
        col = 2
        maxVal = 0
        for row in range(board.ROWS):
            val = board.value.get(row,col)
            if val != None and val > maxVal:
                s = board.getKey(row,col)
        
        if s != None:
            board.showBoard()
            print("\nUpisujemo u polje: ", "[" + s + "]")
            board.submit(s)           
            return
        
        # pozicija dole
        pd = None
        for row in range(board.ROWS):
            if board.score.get(row,0) != None:
                continue
            pd = row
            break
        
        # pozicija gore
        pg = None
        for row in range(board.ROWS - 1,-1,-1):
            if board.score.get(row,1) != None:
                continue
            pg = row
            break

        threshold = 0.35   # prag
        goal = ['1','2','3','4','5','6','K','F','P','J']        
        if pd != None and pg != None:
            if pd >= 6 and pg < 6:
                # Opcija 1
                if self.calculateProbability(board,goal[pd]) >= threshold:
                    self.autoplay(board,goal[pd],0)
                else:
                    self.autoplay(board,goal[pg],1)
            if pd < 6 and pg < 6:
                # Opcija 2: treba igrati kombinaciju za koju ima više bačenih kockica (ako je jednak broj igrati "na dole")
                if board.dices.getCount(int(goal[pd])) >= board.dices.getCount(int(goal[pg])):
                    self.autoplay(board,goal[pd],0)
                else:
                    self.autoplay(board,goal[pg],1)
            if pd >= 6 and pg >= 6:
                # Opcija 3
                if self.calculateProbability(board,goal[pd]) > self.calculateProbability(board,goal[pg]):
                    self.autoplay(board,goal[pd],0)
                else:
                    self.autoplay(board,goal[pg],1)
            if pd < 6 and pg >= 6:
                # Opcija 4
                if self.calculateProbability(board,goal[pg]) >= threshold:
                    self.autoplay(board,goal[pg],1)
                else:
                    self.autoplay(board,goal[pd],0)

        if pd != None and pg == None:
            self.autoplay(board,goal[pd],0)

        if pd == None and pg != None:
            self.autoplay(board,goal[pg],1)

        if pd == None and pg == None:
            pr = None
            for row in range(board.ROWS - 1,-1,-1):
                if board.score.get(row,2) != None:
                    continue
                pr = row
                break
            self.autoplay(board,goal[pr],2)

    def autoplay(self,board,goal,col):
        while not board.isEndOfRound():
            if board.dices.isGoalFulfilled(goal):          
                break
            else:
                self.hold(board.dices,goal,True)

                dices = board.rollDice()

                print("Bacanje #" + str(board.throw) + ":", end=" ")
                for d in dices:
                    print(" "  + str(d) + " ", end=" ")
                print()                
        self.hold(board.dices,goal,True)

        s = None
        for row in range(board.ROWS):
            val = board.value.get(row,col)
            if val != None:
                s = board.getKey(row,col)
        
        if s != None:
            board.showBoard()
            print("\nUpisujemo u polje: ", "[" + s + "]")
            board.submit(s)           
            return

    def calculateProbability(self,board,goal):
        return self.simulate(board.dices.v, goal, 2, 10**3, False)

    def hold(self,dices,goal,debug=False):
        goals = {
            "1": "kečevi",
            "2": "dvojke",
            "3": "trojke",
            "4": "četvorke",
            "5": "petice",
            "6": "šestice",
            "K": "kenta",
            "F": "ful",
            "P": "poker",
            "J": "jamb",
        }

        if dices.isGoalFulfilled(goal):          
            for i in range(5):
                dices.hold(i)
        else:        
            v = dices.v
            count = dices.count

            if goal >= "1" and goal <= "6":
                for i in range(5):
                    if str(v[i]) == goal:
                        dices.hold(i)
                    else:
                        dices.release(i)                    
                
            if goal == "P" or goal == "J":
                numberWithMaxCount = 0  #
                for i in range(6):
                    if count[i] >= count[numberWithMaxCount]:
                        numberWithMaxCount = i
                for i in range(5):
                    if v[i] == numberWithMaxCount + 1:
                        dices.hold(i)
                    else:
                        dices.release(i)                    
            if goal == "K":
                t = [0, 1, 1, 1, 1, 0]            

                for i in range(5):
                    k = v[i] - 1
                    if t[k] > 0: 
                        dices.hold(i)
                        t[k] = 0
                    else:
                        dices.release(i)
            if goal == "F":
                t = [0, 0, 0, 0, 0, 0]		
                for i in range(5):
                    k = v[i] - 1
                    if count[k] >= 3:
                        t[k] = 3
                    elif count[k] >= 2:
                        t[k] = 2
                    
                for i in range(5):
                    k = v[i] - 1
                    if t[k] > 0:
                        dices.hold(i)
                        t[k] = t[k] - 1
                    else:
                        dices.release(i)
        if debug: # True ako želim da mi ispiše
            print("Sačuvamo:  ", end=" ")
            for f in dices.f:
                if f == 1:
                    print(" . ", end=" ")
                else:
                    print(u" \u2191 ", end=" ") # \u2191 = karakter za strelicu gore
            print(" (" + goals[goal] + ")") # ispišemo šta jurimo
            print()

    def simulate(self, values, goal, rounds, n=10**4, debug=False):
        k = 0
        for i in range(n):
            dices = Dices(values.copy())
        
            if debug:
                print("Simulation #", i+1)
                throw = 1
                print("Bacanje #" + str(throw) + ":", end=" ")
                for d in dices.v:
                    print(" "  + str(d) + " ", end=" ")
                print()                

            if dices.isGoalFulfilled(goal):          
                k = k + 1
            else:
                for j in range(rounds):
                    self.hold(dices,goal,debug)

                    dices.roll()

                    if debug:        
                        throw = 2 + j
                        print("Bacanje #" + str(throw) + ":", end=" ")
                        for d in dices.v:
                            print(" "  + str(d) + " ", end=" ")
                        print()                

                    if dices.isGoalFulfilled(goal):          
                        k = k + 1
                        break                            
            self.hold(dices,goal,debug)

        return k/n

# Pojavljuje se kada korisnik želi da započne novu igru
class StartNewGameException(Exception): 
    pass

# Pojavljuje se kada korisnik želi da napusti igru
class QuitGameException(Exception):
    pass

try:
    # simulacija montekarlo metodom
    # print("Simulate: ", Robot().simulate([2,3,4,4,5], "K", 2, 10**2, False))

    while True:
        try:
            b=Board()
            b.play()
            
            print("Menu:")
            print("[N] Nova igra")
            print("[Q] Izlaz")
            while True:
                print("Opcija: ", end="")
                s = input().upper()
                if s == 'N':
                    raise StartNewGameException
                if s == 'Q':
                    raise QuitGameException
        except StartNewGameException:
            pass
except QuitGameException:
    pass

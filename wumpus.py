import random
import sys

def help():
    print ("""
        INI BENTUK DARI RUANGAN YANG TERSEDIA
        13 14 15 16
        9  10 11 12
        5  6  7  8
        1  2  3  4
        
    Agent memiliki indra untuk mencium bahaya
    bila ruangan terdekat memiliki:
        WUMPUS:   'STENCH'
        PIT   :   'BREEZE'
        """)

class Objek:

    def __init__(self, **kwargs):
        self.location = 0 # this is a room object
        for key, value in kwargs.items():
            setattr(self, key, value)

    def move(self, new_location):
        if new_location.number in self.location.relation or new_location == self.location:
            self.location = new_location
            return True
        else:
            return False

    def validate_move(self, new_location):
        return new_location.number in self.location.relation or new_location == self.location
                
    def is_hit(self, a_room):
        return self.location == a_room

class Ruangan:

    def __init__(self, **kwargs):
        self.number = 0
        self.relation = [] #These are NOT objects
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def connect(self, new_number):
        if new_number not in self.relation:
            self.relation.append(new_number)    

    def describe(self):
        print("Agent berada di ruangan {}.\nAgent bisa pergi ke ruangan : {}".format(self.number, self.relation))        

def create_objek(ruangan):
    Things=[]
    Things.append(Objek(location = ruangan[0])) # Agent berada di kolom 1.1
    checker = False

    while checker == False:
        Objects = random.sample(ruangan, 5) #Wumpus, Pit1, Pit2, Pit3, Gold
        Pits = [Objects[1], Objects[2], Objects[3]]
        # 13 [14]   [15] 16
        # [9] 10   11 [12]
        
        # [5] 6   7 [8]
        # 1 [2]   [3] 4
        # Pit tidak boleh berada pada pasangan ruangan seperti gambar diatas
        forbiddenRoom1 = [ruangan[1], ruangan[4]]
        forbiddenRoom2 = [ruangan[2], ruangan[7]]
        forbiddenRoom3 = [ruangan[13], ruangan[8]]
        forbiddenRoom4 = [ruangan[11], ruangan[14]]
    
        checker = True
        
        if Objects[0] == ruangan[0]:
            checker = False
        if Objects[1] == ruangan[0] or Objects[2] == ruangan[0] or Objects[3] == ruangan[0]:
            checker = False
        if (len(set(forbiddenRoom1) - set(Pits)) == 0):
            checker = False
        if (len(set(forbiddenRoom2) - set(Pits)) == 0):
            checker = False
        if (len(set(forbiddenRoom3) - set(Pits)) == 0):
            checker = False

    for room in Objects:
        Things.append(Objek(location = room))

    return Things

def create_map():
    # First create a list of all the rooms.
    for number in range(16):
        Map.append(Ruangan(number = number +1))

    # Then stich them together.
    for indeks, room in enumerate(Map):

        if indeks == 0:
            room.connect(2)
            room.connect(5)
        if indeks == 1:
            room.connect(1)
            room.connect(3)
            room.connect(6)
        if indeks == 2:
            room.connect(2)
            room.connect(4)
            room.connect(7)
        if indeks == 3:
            room.connect(3)
            room.connect(8)
        if indeks == 4:
            room.connect(1)
            room.connect(6)
            room.connect(9)
        if indeks == 5:
            room.connect(2)
            room.connect(5)
            room.connect(7)
            room.connect(10)
        if indeks == 6:
            room.connect(3)
            room.connect(6)
            room.connect(8)
            room.connect(11)
        if indeks == 7:
            room.connect(4)
            room.connect(7)
            room.connect(12)
        if indeks == 8:
            room.connect(5)
            room.connect(10)
            room.connect(13)
        if indeks == 9:
            room.connect(6)
            room.connect(9)
            room.connect(11)
            room.connect(14)
        if indeks == 10:
            room.connect(7)
            room.connect(10)
            room.connect(12)
            room.connect(15)
        if indeks == 11:
            room.connect(8)
            room.connect(11)
            room.connect(16)
        if indeks == 12:
            room.connect(9)
            room.connect(14)
        if indeks == 13:
            room.connect(13)
            room.connect(15)
            room.connect(10)
        if indeks == 14:
            room.connect(14)
            room.connect(16)
            room.connect(11)
        if indeks == 15:
            room.connect(15)
            room.connect(12)

# ============ BEGIN HERE ===========

Map = []
create_map()

Agent, Wumpus, Pit1, Pit2, Pit3, Gold = create_objek(Map)

print("""
    Selamat Datang di wumpus..
       COMMAND YANG TERSEDIA : \n 
       1. M {ANGKA} untuk bergerak
       2. S {ANGKA} untuk menembak
       3. H untuk bantuan
       4. Q untuk keluar")
    """)


while True:
    Agent.location.describe()

    for room in Agent.location.relation:
        if Wumpus.location.number == room:
            print("Stench")
        if Pit1.location.number == room or Pit2.location.number == room or Pit3.location.number == room:
            print("Breeze")
       
    if Gold.location == Agent.location:
        print("Gold ditemukan. Tekan T untuk mengambil gold")
    
    agent_input = input("\n> ")
    command_list = agent_input.split(' ')
    command = command_list[0].upper()
    if len(command_list) > 1:
        try:
            move = Map[int(command_list[1]) -1]
        except:
            print("\n Command tidak ditemukan")
            continue
    else:
        move = Agent.location

    if command == 'T':
        print("Gold berhasil diambil. Anda memenangkan permainan")
        sys.exit()

        continue
    if command == 'H':
        help()
        continue

    elif command == 'Q' or command == 'QUIT':
        sys.exit()

    elif command == 'M':
        Agent.move(move)

    elif command == 'S':
        if Agent.validate_move(move):
            print('Anda menembak ruangan {}'.format(move.number))
            if Wumpus.location == move:
                print("\n Wumpus mati. \n Selamat anda memenangkan permainan.\n")
                sys.exit()
        else:
            print("\n** Agent tidak bisa menembak ke ruangan yang tidak berelasi.")
            continue

        print("\n Tembakanmu meleset. Anda kalah.\n")
        sys.exit()
    
    else:
        print("\n **COMMAND YANG TERSEDIA : \n 1. M {ANGKA} \n 2. S {ANGKA} \n 3. H \n 4. Q")
        continue

    if Agent.location == Wumpus.location:
        print("Wumpus Memakanmu\n")
        sys.exit()    

    elif Agent.location == Pit1.location or Agent.location == Pit2.location or Agent.location == Pit3.location:
        print("Anda masuk kedalam PIT\n")
        sys.exit()

    else:
        pass

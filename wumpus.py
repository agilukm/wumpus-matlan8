import random
import sys
import threading

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
        
    Anda dinyatakan menang apabila Anda telah
    mendapatkan seluruh GOLD atau berhasil
    membunuh semua WUMPUS dengan Arrow.
    
    Anda dinyatakan kalah apabila terjatuh ke
    dalam PIT, dimakan oleh WUMPUS, atau saat
    kehilangan seluruh Arrow yang dimiliki.
        """)

def bentuk():
    print("""
        13 14 15 16
        9  10 11 12
        5  6  7  8
        1  2  3  4
        """)
    
class Objek:

    def __init__(self, **kwargs):
        self.lokasi = 0 #ini adalah objek Room
        for key, value in kwargs.items():
            setattr(self, key, value)

    def pindah(self, lokasi_baru):
        if lokasi_baru.number in self.lokasi.relasi or lokasi_baru == self.lokasi:
            self.lokasi = lokasi_baru
            return True
        else:
            return False

    def validasi_gerak(self, lokasi_baru):
        return lokasi_baru.number in self.lokasi.relasi or lokasi_baru == self.lokasi

class Ruangan:

    def __init__(self, **kwargs):
        self.number = 0
        self.relasi = [] 
        for key, value in kwargs.items():
            setattr(self, key, value)
    
    def connect(self, new_number):
        if new_number not in self.relasi:
            self.relasi.append(new_number)    

    def describe(self):
        print("Agent berada di ruangan {}.\nAgent bisa pergi ke ruangan : {}".format(self.number, self.relasi))        

def buat_objek(ruangan):
    Things=[]
    Things.append(Objek(lokasi = ruangan[0])) # Agent berada di kolom 1.1
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
        Things.append(Objek(lokasi = room))

    return Things

def buat_map():
    # Membuat list dari room
    for number in range(16):
        Map.append(Ruangan(number = number +1))

    # Menghubungkan seluruh room sesuai aturan 4x4
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
buat_map()

Agent, Wumpus, Pit1, Pit2, Pit3, Gold = buat_objek(Map)

#Membuat variabel untuk wait sebelum sys.exit
yyy = threading.Event()


print("""
    Selamat Datang di wumpus..
       COMMAND YANG TERSEDIA : \n 
       1. M {ANGKA} untuk bergerak
       2. S {ANGKA} untuk menembak
       3. H untuk bantuan
       4. Q untuk keluar")
    """)


while True:
    Agent.lokasi.describe()

    for room in Agent.lokasi.relasi:
        if Wumpus.lokasi.number == room:
            print("Stench")
        if Pit1.lokasi.number == room or Pit2.lokasi.number == room or Pit3.lokasi.number == room:
            print("Breeze")
       
    if Gold.lokasi == Agent.lokasi:
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
        move = Agent.lokasi

    if command == 'T':
        print("Gold berhasil diambil. Anda memenangkan permainan")
        yyy.wait(2)
        sys.exit()

    if command == 'H':
        help()

        continue

    elif command == 'Q' or command == 'QUIT':
        print("Anda Keluar")
        yyy.wait(2)
        sys.exit()

    elif command == 'M':
        Agent.pindah(move)
        bentuk()

    elif command == 'S':
        if Agent.validasi_gerak(move):
            print('Anda menembak ruangan {}'.format(move.number))
            if Wumpus.lokasi == move:
                print("\n Wumpus mati. \n Selamat anda memenangkan permainan.\n")
                sys.exit()
        else:
            print("\n** Agent tidak bisa menembak ke ruangan yang tidak berelasi.")
            continue

        print("\n Tembakanmu meleset. Anda kalah.\n")
        yyy.wait(2)
        sys.exit()
    
    else:
        print("\n **COMMAND YANG TERSEDIA : \n 1. M {ANGKA} \n 2. S {ANGKA} \n 3. H \n 4. Q")
        continue

    if Agent.lokasi == Wumpus.lokasi:
        print("Wumpus Memakanmu, KALAH!\n")
        yyy.wait(2)
        sys.exit()    

    elif Agent.lokasi == Pit1.lokasi or Agent.lokasi == Pit2.lokasi or Agent.lokasi == Pit3.lokasi:
        print("Anda masuk kedalam PIT, KALAH!\n")
        yyy.wait(2)
        sys.exit()

    else:
        pass

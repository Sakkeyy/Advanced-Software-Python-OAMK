import tkinter as tk
import random

# Matrixin arvot
Viidakko = [[0 for _ in range(100)] for _ in range(100)]

# Seikkailijat, Leijonan initialisoinnissa käytetään satunnaista sijaintia, toki ernestille ja kernestille myöskin, mutta eri toteutuksella
Ernesti = {'nimi': 'Ernesti', 'sijainti': (1, 1)}
Kernesti = {'nimi': 'Kernesti', 'sijainti': (99, 99)}
Leijona = {'nimi': 'Leijona', 'sijainti': (random.randint(0,99), random.randint(0,99))}
PudotaLeijona = False

# Toiminnot

# Ottaa askeleen
def Liiku(seikkalijanNimi, uusiSijainti):
    x, y = uusiSijainti
    if 0 <= x < 100 and 0 <= y < 100:
        
        Aikaisempi_x, Aikaisempi_y = seikkalijanNimi['sijainti']
        
        # Päivttää aikaisemman ruudun vihreäksi
        Viidakko[Aikaisempi_x][Aikaisempi_y] = 0
        
        # Ruudulle seikkailijalle sopiva väri
        if seikkalijanNimi['nimi'] == 'Ernesti':
            Viidakko[x][y] = 1  # Ernesti
        elif seikkalijanNimi['nimi'] == 'Kernesti':
            Viidakko[x][y] = 2  # Kernesti
        elif seikkalijanNimi['nimi'] == 'Leijona':
            Viidakko[x][y] = 3  # Leijona
        
        # Päivittää kirjastoon uuden sijainnin
        seikkalijanNimi['sijainti'] = uusiSijainti

        if Leijona['sijainti'] == Ernesti['sijainti'] or Leijona['sijainti'] == Kernesti['sijainti']:
            print("Nami olipa hyvä ohjelmoija")
            quit()
        if Ernesti['sijainti'] == Kernesti['sijainti']:
            print("Onpas mukava nähdä!")
            quit()
    

# Liikuttaa seikkailijaa toisiaan kohti

def LiikuKohti(Kuka, Ketä):
    x, y = Kuka['sijainti']
    Kohteen_x, Kohteen_y = Ketä['sijainti']

    HarhaAskel = random.uniform(0,2)

# Leijonathan ei harhaile!
    if Kuka['nimi'] == 'Leijona':
        # EI HARHAILE
        HarhaAskel = 1
    
    # Normaali askellus, mukaan luettuna harha-askel
    if HarhaAskel > 0.7:  #
        if x < Kohteen_x:
            Uusi_x = x + 1
        elif x > Kohteen_x:
            Uusi_x = x - 1
        else:
            Uusi_x = x
        
        if y < Kohteen_y:
            Uusi_y = y + 1
        elif y > Kohteen_y:
            Uusi_y = y - 1
        else:
            Uusi_y = y
    else:  # Harha-askel
        Uusi_x = x + random.choice([-1, 0, 1])
        Uusi_y = y + random.choice([-1, 0, 1])

    # Liikuta seikkailijaa
    Liiku(Kuka, (Uusi_x, Uusi_y))


# Auttaa leijonaa havaitsemaan lähimmän seikkailijan
def LeijonaEtsiLähin():
    LeijonaSijainti = Leijona['sijainti']
    ErnestiSijainti = Ernesti['sijainti']
    KernestiSijainti = Kernesti['sijainti']
    
    # Laskee kuinka pitkä etäisyys on kumpaankin seikkailijaan
    EtäisyysErnestiin = abs(LeijonaSijainti[0] - ErnestiSijainti[0]) + abs(LeijonaSijainti[1] - ErnestiSijainti[1])
    EtäisyysKernestiin = abs(LeijonaSijainti[0] - KernestiSijainti[0]) + abs(LeijonaSijainti[1] - KernestiSijainti[1])
    
    if EtäisyysErnestiin <= EtäisyysKernestiin:
        LiikuKohti(Leijona, Ernesti)
    else:
        LiikuKohti(Leijona, Kernesti)

# Jatkuvasti kutsuu liikkumista sekä päivittää matrixia
def Kävele():
    LiikuKohti(Ernesti, Kernesti)
    LiikuKohti(Kernesti, Ernesti)
    
    if PudotaLeijona:
        LeijonaEtsiLähin()  # Pudota leijona myös viidakkoon
    
    PiirräMatrix()
    ikkuna.after(500, Kävele)

# Laske seikkailijat satunnaiseen sijaintiin matrixissa, leijona on ehdollisen lipun takana
def LaskuvarjoHyppy():
    global PudotaLeijona
    PudotaLeijona = False
    print("COWABUNGA!!!!")
    Liiku(Ernesti, (random.randint(0,99), random.randint(0,99)))
    Liiku(Kernesti, (random.randint(0,99), random.randint(0,99)))
    PiirräMatrix()

def VapautaLeijona():
    global PudotaLeijona
    PudotaLeijona = True


ikkuna = tk.Tk()
ikkuna.title("Viidakko")

# Napit
LaskuvarjoHyppyPainike = tk.Button(ikkuna, text="Laskuvarjohyppy!", command=LaskuvarjoHyppy)
LaskuvarjoHyppyPainike.pack(side=tk.BOTTOM, pady=10)

SeikkailuPainike = tk.Button(ikkuna, text="Aloita Seikkailu!", command=Kävele)
SeikkailuPainike.pack(side=tk.BOTTOM, pady=30)

VapautaLeijonaPainike = tk.Button(ikkuna, text="Vapauta leijona!", command=VapautaLeijona)
VapautaLeijonaPainike.pack(side=tk.BOTTOM, pady=50)

# Matrixin luonti ja piirtäminen
Matrix = tk.Canvas(ikkuna, width=500, height=500)
Matrix.pack(side=tk.LEFT)

def PiirräMatrix():
    Matrix.delete("all")
    for i in range(100):
        for j in range(100):
            value = Viidakko[i][j]
            if value == 0:
                color = 'green' # Viidakko
            elif value == 1:
                color = 'yellow'  # Ernesti
            elif value == 2:
                color = 'blue'  # Kernesti
            elif value == 3:
                color = 'red'  # Leijona
            Matrix.create_rectangle(j*5, i*5, (j+1)*5, (i+1)*5, fill=color, outline='black')

ikkuna.mainloop()

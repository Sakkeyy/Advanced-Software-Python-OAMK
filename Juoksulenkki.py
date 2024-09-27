import tkinter as tk
import winsound
import random
import time
import numpy as np
import matplotlib.pyplot as plt

ikkuna = tk.Tk()
ikkuna.geometry("300x500+800+100") # leveysxkorkeus+resoluutio leveys+resoluutio korkeus / Vas->Oik / Ylhäältä -> Alas

# Muuttuja-osasto
E_sijainti_x=10
K_sijainti_x=10
usainPosition = 10
MaaliRange = 250
aloitusAika = 0
E_aika = 0
K_aika = 0
E_maalissa = False
K_maalissa = False
Ernesti_aika_string = tk.StringVar(value="Ernestin aika: --")
Kernesti_aika_string = tk.StringVar(value="Kernestin aika: --")
Voittaja_string = tk.StringVar(value="")
ErnestiKunto = 5
KernestiKunto = 5
TreeninKestoPv = 0
E_Treenikausi = False
K_Treenikausi = False
VuosituhannenKisaBool = False




# Toiminnot

def Ernesti_juoksu():
        Ernesti_askel()
        ikkuna.update()

def Kernesti_juoksu():
        Kernesti_askel()
        ikkuna.update()

def Ernesti_treeni(TreeninKestoPv):
    global ErnestiKunto, E_Treenikausi
    E_Treenikausi = True
    while not E_maalissa:
        Ernesti_juoksu()
    ErnestiKunto += 0.002 * TreeninKestoPv
    print(f"Ernestin treenipäivä: {TreeninKestoPv}", ErnestiKunto)
    time.sleep(1)
    print("Huhhuh, rankka treeni, nyt lepoa")
    Lähtöviivalle()

def Kernesti_treeni(TreeninKestoPv):
    global KernestiKunto
    global K_Treenikausi
    K_Treenikausi = True
    while not K_maalissa:
        Kernesti_juoksu()
    KernestiKunto += 0.002 * TreeninKestoPv
    print(f"Kernestin treenipäivä: {TreeninKestoPv}", KernestiKunto)
    time.sleep(1)
    print("Huhhuh, rankka treeni, nyt lepoa")
    Lähtöviivalle()

def Ernesti_askel():
    global E_sijainti_x, E_maalissa, E_aika, ErnestiKunto
    if E_sijainti_x < MaaliRange:
        E_sijainti_x=E_sijainti_x+random.uniform(1,ErnestiKunto)
        ErnestiLabel.place(x=E_sijainti_x,y=50)
        print("klomps klomps...")
        winsound.Beep(300,60)
        ikkuna.update()
    else:
        E_maalissa = True
        
    if not E_Treenikausi:
        if E_sijainti_x >= MaaliRange and not E_maalissa:
            E_aika=time.time() - aloitusAika
            print(f"Ernesti saapui maaliin ajassa: {E_aika:.2f}")
            Ernesti_aika_string.set(f"Ernestin aika: {E_aika:.2f} seconds")

def Kernesti_askel():
    global K_sijainti_x, K_maalissa, K_aika
    if K_sijainti_x < MaaliRange:
        K_sijainti_x=K_sijainti_x+random.uniform(1,KernestiKunto)
        KernestiLabel.place(x=K_sijainti_x,y=100)
        print("klips kops kips...")
        winsound.Beep(500,60)
        ikkuna.update()
    else:
        K_maalissa = True

    if not K_Treenikausi:
        if K_sijainti_x >= MaaliRange and not K_maalissa:
            K_aika=time.time() - aloitusAika
            print(f"Kernesti saapui maaliin ajassa: {K_aika:.2f}")
            Kernesti_aika_string.set(f"Kernestin aika: {K_aika:.2f} seconds")

def Juoskaa():
    global aloitusAika, E_Treenikausi, K_Treenikausi, VuosituhannenKisaBool
    E_Treenikausi = False
    K_Treenikausi = False
    aloitusAika = time.time()
    winsound.Beep(800,1000)
    while not (E_maalissa and K_maalissa):
        Kernesti_juoksu()
        Ernesti_juoksu()
        if VuosituhannenKisaBool:
            for Leijona in Leijonat:
                KilpailijaAskel(Leijona)
    if E_aika < K_aika:
        Voittaja_string.set(f"Ernesti voittaa {K_aika - E_aika:.2f}s Erotuksella!")
    else:
        Voittaja_string.set(f"Kernesti voittaa {E_aika - K_aika:.2f}s Erotuksella!")

def Lähtöviivalle():
    global K_aika
    global E_aika
    global K_maalissa
    global E_maalissa
    global K_sijainti_x
    global E_sijainti_x
    K_sijainti_x = 10
    E_sijainti_x = 10
    K_aika = 0
    E_aika = 0 
    K_maalissa = False
    E_maalissa = False
    ErnestiLabel.place(x=E_sijainti_x, y=50)
    KernestiLabel.place(x=K_sijainti_x, y=100)
    

def VuosituhannenKisa():
    global VuosituhannenKisaBool
    VuosituhannenKisaBool = True
    MuutKilpailijatViivalle()
    ErnestiAikaLabel.destroy()
    KernestiAikaLabel.destroy()
    VoittajaLabel.destroy()

    # Vuosituhanen kilpailun initialisointi
def MuutKilpailijatViivalle():
    y_offset = 150  
    usainLabel.place(x=10,y=75)
    for Leijona in Leijonat:
        LeijonaLabel[Leijona] = tk.Label(ikkuna, text=Leijona[0])  # Leijonan etukirjain
        Leijona_pos_x[Leijona] = 10  
        LeijonaLabel[Leijona].place(x=Leijona_pos_x[Leijona], y=y_offset)  
        y_offset += 20  # Siirtää seuraavaa leijonaa alemmas

def KilpailijaAskel(Leijona):
    global MaaliRange, usainPosition
    
    if Leijona_pos_x[Leijona] < MaaliRange or usainPosition < MaaliRange:
        Leijona_pos_x[Leijona] += random.uniform(1, 9)  # Leijonien kunto on n. 9
        LeijonaLabel[Leijona].place(x=Leijona_pos_x[Leijona], y=LeijonaLabel[Leijona].winfo_y())
        usainPosition += random.uniform(1,7)
        usainLabel.place(x=usainPosition, y=75)

        ikkuna.update()

# Osat

ErnestiLabel=tk.Label(ikkuna,text="E")
ErnestiLabel.place(x=E_sijainti_x,y=50)

usainLabel = tk.Label(ikkuna, text="🗲")

KernestiLabel=tk.Label(ikkuna,text="K")
KernestiLabel.place(x=K_sijainti_x,y=100)

MaaliLabel=tk.Label(ikkuna,text="🏁")
MaaliLabel.place(x=250, y=20)
VoittajaLabel=tk.Label(ikkuna, textvariable=Voittaja_string)
VoittajaLabel.place(x=50, y=10)

ErnestiAikaLabel=tk.Label(ikkuna, textvariable=Ernesti_aika_string)
ErnestiAikaLabel.place(x=10, y=250)
KernestiAikaLabel=tk.Label(ikkuna, textvariable=Kernesti_aika_string)
KernestiAikaLabel.place(x=10, y=270)


KernestiAskel=tk.Button(ikkuna,text="Kernesti askel",command=Kernesti_askel)
KernestiAskel.place(x=10,y=370)
KernestiJuokse=tk.Button(ikkuna,text="Kernesti Juokse",command=Kernesti_juoksu)
KernestiJuokse.place(x=100,y=370)
KernestiTreeniPainike=tk.Button(ikkuna,text="1pv",command=lambda: Kernesti_treeni(1))
KernestiTreeniPainike.place(x=200, y=370)
KernestiTreeniPainike=tk.Button(ikkuna,text="1kk",command=lambda: Kernesti_treeni(30))
KernestiTreeniPainike.place(x=230, y=370)
KernestiTreeniPainike=tk.Button(ikkuna,text="1v",command=lambda: Kernesti_treeni(365))
KernestiTreeniPainike.place(x=260, y=370)

ErnestiAskel=tk.Button(ikkuna,text="Ernesti askel",command=Ernesti_askel)
ErnestiAskel.place(x=10,y=400)
ErnestiJuokse=tk.Button(ikkuna,text="Ernesti Juokse",command=Ernesti_juoksu)
ErnestiJuokse.place(x=100,y=400)
ErnestiTreeniPainike=tk.Button(ikkuna,text="1pv",command=lambda: Ernesti_treeni(1))
ErnestiTreeniPainike.place(x=200, y=400)
ErnestiTreeniPainike=tk.Button(ikkuna,text="1kk",command=lambda: Ernesti_treeni(30))
ErnestiTreeniPainike.place(x=230, y=400)
ErnestiTreeniPainike=tk.Button(ikkuna,text="1v",command=lambda: Ernesti_treeni(365))
ErnestiTreeniPainike.place(x=260, y=400)


KilpailuPainike=tk.Button(ikkuna,text="Kilpailu alkaa",command=Juoskaa)
KilpailuPainike.place(x=100,y=430)

PalautusPainike=tk.Button(ikkuna,text="Lähtöviivalle",command=Lähtöviivalle)
PalautusPainike.place(x=10, y=430)

VuosituhannenKilpailuPainike=tk.Button(ikkuna,text="Vuosituhannen kisa", command=VuosituhannenKisa)
VuosituhannenKilpailuPainike.place(x=180,y=430)


LeijonaLabel = {}  # LeijonaLabelKirjasto
Leijona_pos_x = {}  # LeijonaSijaintiKirjasto



# Sanakirja 100 metrin maailmanennätysajoille.. Jotaki humpuukiaki
Ennätykset = {
    1912: {'time': 10.6, 'runner': 'Kari Tapio'},
    1936: {'time': 10.3, 'runner': 'Heikki Helander'},
    1968: {'time': 9.95, 'runner': 'Jim Halpert'},
    1988: {'time': 9.79, 'runner': 'Dwight Schrute'},
    1999: {'time': 9.79, 'runner': 'Taikuri Luttinen'},
    2009: {'time': 9.58, 'runner': 'Usain Bolt'}
}
 
# Leijonien juoksuajat ja nimet ¤NOIN 7 VUOTTA #Leijonien kunto n.9-8
Leijonat = {
    'Simba': {'time': 7.5},
    'Nala': {'time': 7.7},
    'Mufasa': {'time': 7.3},
    'Scar': {'time': 8.0},
    'Sarabi': {'time': 7.8},
    'Zazu': {'time': 7.9},
    'Rafiki': {'time': 7.6},
    'Bumba': {'time': 7.4},
    'Kiara': {'time': 7.85},
    'Timon': {'time': 8.1}
}
for Leijona, info in Leijonat.items():
    Ennätykset[Leijona] = {'time': info['time'], 'runner': Leijona}
 
vuodet = [1912, 1936, 1968, 1988, 1999, 2009]
times = [Ennätykset[year]['time'] for year in vuodet]
 
plt.plot(vuodet, times, marker='o', label='Maailman Ennätys')
 
TulevatVuodet = [2050]
TulevatAjat = [9.4]
plt.plot(TulevatVuodet, TulevatAjat, marker='x', linestyle='--', label='Ennustus 2050')
 
plt.title('100 metrin maailmanennätysajan kehittymisen ennustus')
plt.xlabel('Vuosi')
plt.ylabel('Aika (s)')
plt.legend()
plt.show()

vuodet = np.linspace(0, 50, 500)

performance = 10 - (9 * (1 - np.exp(-0.1 * vuodet)))

plt.figure(figsize=(10, 6))
plt.plot(vuodet, performance, label="Suoritus", color="blue", linewidth=2)

plt.title('Juoksijoiden kehitys 50 vuodessa', fontsize=14)
plt.xlabel('Treenivuosia', fontsize=12)
plt.ylabel('Tulos sekunneissa', fontsize=12)

plt.grid(True)
plt.legend()

plt.show()

ikkuna.mainloop()
import tkinter as tk
import threading
from PIL import Image, ImageTk
import time
import random

# Luodaan ikkuna
ikkuna = tk.Tk()
ikkuna.title("Tomaatin heitto")
ikkuna.geometry("800x300+200+300") #200+300
ErnestiPisteet = 0
KernestiPisteet = 0
KernestiPisteetString = tk.StringVar(value="Kernestin pisteet: --")
ErnestiPisteetString = tk.StringVar(value="Ernestin pisteet: --")
Ernestin_x = 730
Kernestin_x = 80
Kilpailu = True

#Maalin_x 360 ja 450
#Maalin_y 70 ja 120

RuutuLeveys = 800


# Toiminnot
def AsetaErnesti():
    ErnestinKuvaLabel.grid(row=0, column=2, padx=0, pady=20)
    ErnestiHeitäButton.place(x=700, y=235)

def KernestiHeitä(Mitä):
    if Mitä == "Maali":
        threading.Thread(target=Heitä, args=('Kernesti',"Maali")).start()
    else:
        threading.Thread(target=Heitä, args=('Kernesti',"Ernesti")).start()

def ErnestiHeitä(Mitä):
    if Mitä == "Maali":
        threading.Thread(target=Heitä, args=('Ernesti', "Maali")).start()
    else: 
        threading.Thread(target=Heitä, args=('Ernesti', "Kernesti")).start()


def HeittoKilpailu():
    global KernestiPisteet, ErnestiPisteet, Kilpailu
    # Kun kilpailu alkaa resetoidaan kaikki
    Kilpailu = True
    KernestiPisteet = 0
    ErnestiPisteet = 0
    KernestiPisteetString.set("Kernestin pisteet: --")
    ErnestiPisteetString.set("Ernestin pisteet: --")
    while Kilpailu:
        time.sleep(1)    
        # Jos johtaa yli yhdellä pisteellä, heitettävä vaihtuu
        if (ErnestiPisteet + 1) < KernestiPisteet:
            print("Kernesti johtaa!")
            KernestiHeitä("Ernesti")
            ErnestiHeitä("Maali")
        elif (KernestiPisteet + 1) < ErnestiPisteet:
            print("Ernesti johtaa!")
            ErnestiHeitä("Kernesti")
            KernestiHeitä("Maali")
        else:
            KernestiHeitä("Maali")
            ErnestiHeitä("Maali")
def KilpailuSeis():
    global Kilpailu
    Kilpailu = False
    print("KILPAILU SEIS!")

# Kuka heittää mitä argumentit
def Heitä(Heittäjä, Heitettävä):
    global ErnestiPisteet,KernestiPisteet
    MaalinOsumaAlue_x = random.randint(265,550)
    MaalinOsumaAlue_y = random.randint(40,150)
    if Heittäjä == 'Kernesti' and Heitettävä == "Maali":
        # Heittokaari on paraabeli
        a = (MaalinOsumaAlue_y - 20) / ((MaalinOsumaAlue_x - (MaalinOsumaAlue_x/2)) ** 2)
        for x in range(Kernestin_x, MaalinOsumaAlue_x, 10):
            y = 0 + a * (x - 200) ** 2 + 20
            time.sleep(0.03)  
            ikkuna.after(0, KernestinTomaatinKuvaLabel.place_configure, {'x': x, 'y': y})
        KernestiOsumaKuvaLabel.place(x=x, y=y)
        # Satunnainen osuma mahdollisuus maaliin
        if  345 < x < 455 and 60 < y < 135:
            print("Kernesti osuu!")
            KernestiPisteet += 1
            KernestiPisteetString.set(f"Kernestin pisteet: {KernestiPisteet}")
    elif Heittäjä == 'Kernesti' and Heitettävä == "Ernesti":
        for x in range(Kernestin_x, (random.randint(700,Ernestin_x)), 10):
            y = 0.0005 * (x - 400) ** 2
            time.sleep(0.03)
            ikkuna.after(0, KernestinTomaatinKuvaLabel.place_configure, {'x': x, 'y': y})
        KernestiOsumaKuvaLabel.place(x=x, y=y)
        # Osumamahdollisuus Ernestiin
        if  710 < x:
            print("KERNESTI VOITTAAA!!!!!!!!!!!!")
            KilpailuSeis()

    # Kaikki samat kuin Kernestillä
    elif Heittäjä == 'Ernesti' and Heitettävä == "Maali":
        a = (MaalinOsumaAlue_y - 20) / ((Ernestin_x - MaalinOsumaAlue_x) ** 2)
        for x in range(Ernestin_x, MaalinOsumaAlue_x, -10):
            y = a * (x - Ernestin_x) ** 2 + 20
            time.sleep(0.03)
            ikkuna.after(0, ErnestinTomaatinKuvaLabel.place_configure, {'x': x, 'y': y})
        ErnestiOsumaKuvaLabel.place(x=x, y=y)
        if  345 < x < 450 and 55 < y < 135:
            print("Ernesti osuu!")
            ErnestiPisteet += 1
            ErnestiPisteetString.set(f"Ernestin pisteet: {ErnestiPisteet}")
    elif Heittäjä == 'Ernesti' and Heitettävä == "Kernesti":
        for x in range(Ernestin_x, (random.randint(Kernestin_x,110)), -10):
            y = 0.0005 * (x - 400) ** 2
            time.sleep(0.03)
            ikkuna.after(0, ErnestinTomaatinKuvaLabel.place_configure, {'x': x, 'y': y})
        ErnestiOsumaKuvaLabel.place(x=x, y=y)
        if x < 100: 
            ErnestiOsumaKuvaLabel.place(x=x, y=y)
            print("ERNESTI VOITTAAA!!!!!!!!!!!!")
            KilpailuSeis()

# Kuvanluonti
KernestiPillow = Image.open("Kernesti.jpg")
KernestinKuva = ImageTk.PhotoImage(KernestiPillow)
MaaliTauluPillow = Image.open("Maalitaulu.jpg")
MaalitaulunKuva = ImageTk.PhotoImage(MaaliTauluPillow)
ErnestiPillow = Image.open("Ernesti.jpg")
ErnestinKuva = ImageTk.PhotoImage(ErnestiPillow)
TomaattiPillow = Image.open("Tomaatti.png")
PienempiTomaatti = TomaattiPillow.resize((20,20))
PienempiTomaatti = ImageTk.PhotoImage(PienempiTomaatti)
OsumaPillow = Image.open("Splat.png")
OsumaKuva = OsumaPillow.resize((20,20))
OsumaKuva = ImageTk.PhotoImage(OsumaKuva)

KernestiKuvaLabel = tk.Label(ikkuna, image=KernestinKuva)
MaalitauluKuvaLabel = tk.Label(ikkuna, image=MaalitaulunKuva)
ErnestinKuvaLabel = tk.Label(ikkuna, image=ErnestinKuva)
KernestinTomaatinKuvaLabel = tk.Label(ikkuna, image=PienempiTomaatti)
ErnestinTomaatinKuvaLabel = tk.Label(ikkuna, image=PienempiTomaatti)
KernestiOsumaKuvaLabel = tk.Label(ikkuna, image=OsumaKuva)
ErnestiOsumaKuvaLabel = tk.Label(ikkuna, image=OsumaKuva)

# Painikkeet
ErnestiPaljastusButton = tk.Button(ikkuna, text="Ernesti!", command=AsetaErnesti)
ErnestiPaljastusButton.place(x=700, y=270)
KernestiHeitäButton = tk.Button(ikkuna, text="Kernesti Heitä!", command=lambda: KernestiHeitä("Maali"))
KernestiHeitäButton.place(x=20, y=235)
ErnestiHeitäButton = tk.Button(ikkuna, text="Ernesti Heitä!", command=lambda: ErnestiHeitä("Maali"))
AloittakaaKilpailuButton = tk.Button(ikkuna, text="KILPAILU!", command=lambda: threading.Thread(target=HeittoKilpailu).start())
AloittakaaKilpailuButton.place(x=380, y=200)
LopettakaaKilpailuButton = tk.Button(ikkuna, text="STOP", command=KilpailuSeis)
LopettakaaKilpailuButton.place(x=390, y=250)


KernestiPisteetLabel = tk.Label(ikkuna, textvariable=KernestiPisteetString)
KernestiPisteetLabel.place(x=250, y=200)
ErnestiPisteetLabel = tk.Label(ikkuna, textvariable=ErnestiPisteetString)
ErnestiPisteetLabel.place(x=460, y=200)

KernestiKuvaLabel.grid(row=0, column=0, padx=0, pady=20)
MaalitauluKuvaLabel.grid(row=0, column=1, padx=240, pady=20) 


ikkuna.mainloop()

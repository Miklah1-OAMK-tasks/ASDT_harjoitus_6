import tkinter as tk
import random
import threading
import numpy as np
import time
import winsound

# SUUNNITELMA TURVALLISESTA UIMA-ALTAASTA (1 PISTETTÄ) ALKAA TÄSTÄ

# Luodaan pääikkuna
ikkuna = tk.Tk()
ikkuna.title("Turvallinen uima-allas")
ikkuna.geometry("1000x800+1300+100")
ikkuna.configure(bg='blue')  # Asetetaan taustaväri siniseksi (valtameri)

# Luodaan autiosaari
autiosaari = tk.Canvas(ikkuna, width=800, height=600, bg='#eab676', highlightthickness=0)  # Hiekkainen saari
autiosaari.place(anchor='center', relx=0.5, rely=0.5)

# Määritellään uima-allas (20x60), aluksi täynnä nollia (tyhjä)
uima_allas = [[0 for _ in range(60)] for _ in range(20)]

# Määritellään ojat (100x1), aluksi täynnä ykkösiä (hiekkaa)
oja_ernesti = [[1] for _ in range(100)]
oja_kernesti = [[1] for _ in range(100)]

# Määritellään metsäalue (20x60) numpytaulukkona, täynnä ykkösiä (metsä)
metsa = np.ones((20, 60), dtype=int)

# Funktio, joka piirtää uima-altaan
def piirra_uima_allas():
    ruudun_koko = 5  # Yhden ruudun koko 5x5 pikseliä
    for i in range(20): # luodaan taulukko 20x60
        for j in range(60):  
            x0, y0 = j * ruudun_koko, i * ruudun_koko # Ruudun vasemman yläkulman koordinaatit
            x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko # Ruudun oikean alakulman koordinaatit
            väri = "#eab676" if uima_allas[i][j] == 0 else "blue" # Hiekka = keltainen, vesi = sininen  
            autiosaari.create_rectangle(x0 + 250, y0 + 250, x1 + 250, y1 + 250, fill=väri, outline='grey') # Piirretään uima-allas

# Funktio, joka piirtää ojat ja ottaa parametreina ojan, aloituspisteen x- ja y-koordinaatit
def piirra_oja(oja, x_alku, y_alku):
    ruudun_koko = 2.5      # Yhden ruudun koko 5x5 pikseliä
    for i in range(100): # luodaan taulukko 100x1
        x0, y0 = x_alku, y_alku - i * ruudun_koko   # Ruudun vasemman yläkulman koordinaatit
        x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko # Ruudun oikean alakulman koordinaatit 
        if oja[i][0] == 0:      # Jos oja on kaivettu, väri on ruskea
            väri = "brown"
            ulkoreuna = "brown"
        elif oja[i][0] == 1:   # Jos oja on täyttämätön, väri on keltainen
            väri="#eab676"
            ulkoreuna = "#eab676"
        elif oja[i][0] == 2:    # Jos oja on täytetty vedellä, väri on sininen
            väri = "blue",
            ulkoreuna = "blue"
        autiosaari.create_rectangle(x0, y0, x1, y1, fill=väri, outline='grey') # Piirretään oja

# Funktio, joka piirtää metsäalueen
def piirra_metsa():
    ruudun_koko = 5  # Yhden ruudun koko 5x5 pikseliä
    for i in range(20):  # Piirretään vain tarvittavat ruudut
        for j in range(60):
            if metsa[i][j] == 1:  # Piirretään vain metsäruudut
                x0, y0 = j * ruudun_koko, i * ruudun_koko
                x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko
                autiosaari.create_rectangle(x0 + 250, y0 + 400, x1 + 250, y1 + 400, fill="green", outline='green')

# Piirretään aluksi uima-allas ja ojat (täynnä hiekkaa)
piirra_uima_allas()
piirra_oja(oja_ernesti, 250, 246)  # Ernestin oja
piirra_oja(oja_kernesti, 545, 246)  # Kernestin oja
piirra_metsa()  # Piirretään metsäalue

# SUUNNITELMA TURVALLISESTA UIMA-ALTAASTA (1 PISTETTÄ) PÄÄTTYY TÄHÄN

# RAKENTAMISEEN TARVITTAVAN TYÖVOIMAN HANKINTA (2 PISTETTÄ) ALKAA TÄSTÄ

apinoiden_tiedot = []   # Lista apinoiden tiedoista 

# Funktio, jolla luodaan apinoita satunnaisiin paikkoihin metsään
def luo_apina():
    for i in range(10):  # Lisätään 10 apinaa
        apina_id = len(apinoiden_tiedot)  # Apinan id
        apina_x = random.randint(0, 59)  # Arvotaan apinan x-koordinaatti
        apina_y = random.randint(0, 19)  # Arvotaan apinan y-koordinaatti
        metsa[apina_y][apina_x] = 0      # Asetetaan apina metsään
        
        ruudun_koko = 5
        x0, y0 = apina_x * ruudun_koko, apina_y * ruudun_koko
        x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko
        apinan_kuva = autiosaari.create_oval(x0 + 250, y0 + 400, x1 + 250, y1 + 400, fill='brown', outline='black')

        # Tallennetaan apinan tiedot listaan
        apinoiden_tiedot.append({
            "id": apina_id,
            "tila": 0,  # 0 = joutilaana, 1 = valmiina kaivamaan, 2 = kaivamassa
            "henkilo": None,
            "x": apina_x,
            "y": apina_y,
            "kuva": apinan_kuva,
            "y_koordinaatti": None,
            "y_koordinaatti_oja": None
        })
        paivita_metsa(apina_y, apina_x, 0)  # Päivitetään metsä
    print("10 apinaa lisätty metsään!")

def e_hakee_apinan(apina_id):
    global apinoiden_tiedot
    # Etsitään satunnainen y-koordinaatti
    y_koordinaatti = random.randint(0, 249)
    y_koordinaatti_oja = round(y_koordinaatti // 2.5)
    
    # Tarkistetaan, ettei samaa koordinaattia ole jo listassa
    while any(apina['y_koordinaatti'] == y_koordinaatti and apina['y_koordinaatti_oja'] == y_koordinaatti_oja for apina in apinoiden_tiedot):
        y_koordinaatti = random.randint(0, 249)
        y_koordinaatti_oja = round(y_koordinaatti // 2.5)
        
    # Määritetään x-koordinaatti Ernestin ojan varrelle
    x_koordinaatti = 0

    # Poistetaan apina metsästä (jos metsässä on apinoita)
    apina_loytynyt = False
    for i in range(20):
        for j in range(60):
            if metsa[i][j] == 0:  # Apina löytyy metsästä
                metsa[i][j] = 1
                paivita_metsa(i, j, 1)
                autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 245, y_koordinaatti, 250, y_koordinaatti + 5)
                # Päivitetään apinan tiedot
                apina = apinoiden_tiedot[apina_id]
                apina['henkilo'] = "Ernesti"
                apina['y_koordinaatti'] = y_koordinaatti
                apina['y_koordinaatti_oja'] = y_koordinaatti_oja
                apina['tila'] = 1
                print("Apinan päivitetyt tiedot:", apina)
                apina_loytynyt = True
                break
        if apina_loytynyt:
            break

    if not apina_loytynyt:
        print("Metsässä ei ole apinoita!")

def paivita_metsa(i, j, arvo):
    metsa[i][j] = arvo
    ruudun_koko = 5
    x0, y0 = j * ruudun_koko, i * ruudun_koko
    x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko
    väri = "brown" if arvo == 0 else "green"
    autiosaari.create_rectangle(x0 + 250, y0 + 400, x1 + 250, y1 + 400, fill=väri, outline='green')
    
def e_apina_kaivaa_ojaa(apina_id):
    global apinoiden_tiedot
    if len(apinoiden_tiedot) == 0:
        print("Ei apinoita kaivamassa!")
        return
    
    apina_sijainti_ojalla = apinoiden_tiedot[apina_id]['y_koordinaatti']
    apina_sijainti_ojassa = apinoiden_tiedot[apina_id]['y_koordinaatti_oja']
    y_sijainti = apina_sijainti_ojalla  # Apinan sijainti ojan varrella
    apinoiden_tiedot[apina_id]['tila'] = 2  # Apina on kaivamassa

    kaivamis_nopeus = 1  # Kaivamisnopeus sekunteina

    kaivamis_kohta = apina_sijainti_ojassa  
    print(f"Apina aloittaa kaivamisen kohdasta: {kaivamis_kohta}")

    while kaivamis_kohta >= 0:  # Kaivetaan kunnes oja on kaivettu tai apina on kaivanut koko ojan
        if oja_ernesti[kaivamis_kohta][0] == 1:  # Jos ojaa ei ole vielä kaivettu tässä kohtaa
            oja_ernesti[kaivamis_kohta][0] = 0  # Kaiva kohta
            
            print(f"Apina kaivoi kohdan: {kaivamis_kohta}")
            
            # Soitetaan kaivamisääniefekti
            print("Kaivamisääni!")

            # Siirretään apinaa ylöspäin ja piirretään apina
            y_sijainti = apina_sijainti_ojalla - (apina_sijainti_ojassa - kaivamis_kohta) * 2.5  # Päivitetään apinan sijainti
            autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 245, y_sijainti, 250, y_sijainti + 5)  # Piirretään apina
            time.sleep(kaivamis_nopeus)  # Apina kaivaa ja pitää tauon

            paivita_oja(oja_ernesti, 250, kaivamis_kohta)  # Päivitetään oja visuaalisesti
            kaivamis_kohta -= 1  # Siirrytään seuraavaan kohtaan
            kaivamis_nopeus *= 2 # Väsymys: Kaivaminen hidastuu kaksinkertaiseksi joka kerta

        else:  # Jos oja on jo kaivettu tässä kohtaa
            oja_ernesti[kaivamis_kohta][0] -= 1  # Kaiva kohta
            print(f"Oja on jo kaivettu tässä kohtaa! Vähennettiin arvosta yksi, uusi arvo: {oja_ernesti[kaivamis_kohta][0]}")
            break
    print(oja_ernesti)

def paivita_oja(oja, x_alku, kaivamis_kohta):
    ruudun_koko = 2.5
    x0 = x_alku
    y0 = kaivamis_kohta * ruudun_koko
    x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko
    
    if oja[kaivamis_kohta][0] == 0:      # Jos oja on kaivettu, väri on ruskea
        väri = "yellow"
        ulkoreuna = "yellow"
    elif oja[kaivamis_kohta][0] == 1:   # Jos oja on täyttämätön, väri on keltainen
        väri="#eab676"
        ulkoreuna = "#eab676"
    elif oja[kaivamis_kohta][0] == 2:    # Jos oja on täytetty vedellä, väri on sininen
        väri = "blue"
        ulkoreuna = "blue"

    # Päivitetään vain yksittäinen kohta
    autiosaari.create_rectangle(x0, y0, x1, y1, fill=väri, outline=ulkoreuna)

# Funktio, joka hakee satunnaisen apinan ja siirtää sen ojan varrelle
def e_hakee_satunnainen_apina():
    if apinoiden_tiedot:  # Varmistetaan, että listassa on apinoita
        satunnainen_apina_id = random.choice([apina['id'] for apina in apinoiden_tiedot if apina.get('henkilo') == None])
        e_hakee_apinan(satunnainen_apina_id)
    else:
        print("Ei apinoita saatavilla!")

def apina_kaivaa_ernestin_ojaa():
    # Suodatetaan ne apinat, joiden tila on 1 eli valmiita kaivamaan
    apinat_ojalla = [apina['id'] for apina in apinoiden_tiedot if apina.get('tila') == 1]
    
    if apinat_ojalla:  # Varmistetaan, että on apinoita ojalla
        satunnainen_apina_id = random.choice(apinat_ojalla)
        print(f"Apina {satunnainen_apina_id} aloittaa kaivamisen.")
        e_apina_kaivaa_ojaa(satunnainen_apina_id)
    else:
        print("Ei apinoita kaivamassa ojaa!")

# Painikkeiden tyylit (Kysyin ChatGPT:ltä apua painikkeiden tyylittelyyn)
painikkeiden_tyyli = {
    "bg": "#4CAF50",    # Taustaväri
    "fg": "white",      # Tekstin väri
    "font": ("Helvetica", 10, "bold"),
    "activebackground": "#45a049", # Painikkeen aktivoitu väri
    "activeforeground": "white",   # Painikkeen aktivoitu tekstin väri
    "padx": 20,  # Lisätään tyhjää tilaa sivuille
    "pady": 10,  # Lisätään tyhjää tilaa ylös ja alas
    "width": 20  # Asetetaan painikkeille vakio leveys
}

# Luodaan painike, jolla lisätään apinoita
lisaa_apinoita = tk.Button(ikkuna, text="Lisää apinoita", command=luo_apina,**painikkeiden_tyyli)
lisaa_apinoita.place(x=400, y=100)

# Luodaan painike, jolla Ernesti hakee apinan
ernesti_hakee_apinan = tk.Button(ikkuna, text="Ernesti hakee apinan", command=lambda: threading.Thread(target=e_hakee_satunnainen_apina).start(), **painikkeiden_tyyli)
ernesti_hakee_apinan.place(x=100, y=100)

# Luodaan painike, jolla apina alkaa kaivamaan ojaa
e_apina_kaivamaan_ojaa = tk.Button(ikkuna, text="Apina kaivaa ernestin ojaa", command=lambda: threading.Thread(target=apina_kaivaa_ernestin_ojaa).start(), **painikkeiden_tyyli)
e_apina_kaivamaan_ojaa.place(x=100, y=150)

# Luodaan painike, joka tulostaa Ernestin ojan tilan
ernestin_ojan_tila = tk.Button(ikkuna, text="Ernestin ojan tila", command=lambda: print(oja_ernesti), **painikkeiden_tyyli)   
ernestin_ojan_tila.place(x=100, y=200)

# RAKENTAMISEEN TARVITTAVAN TYÖVOIMAN HANKINTA (2 PISTETTÄ) PÄÄTTYY TÄHÄN

# YHDESSÄ ENEMMÄN (3 PISTETTÄ) ALKAA TÄSTÄ

# Saarella on kaksi ojaa. Senpä vuoksi:
 
# -tee vastaava toiminnallisuus Kernestille metsässä laiskottelevien apinoiden hakemista ja 
# ojan varteen työhön opastamista varten, kuin Ernestin tapauksessakin
 
# Ryhmätyönä niin ohjelmistojen teko kuin ojan kaivuukin sujuu parhaiten. Sen vuoksi… 

# -lisää toiminto, jonka avulla Ernesti voi milloin tahansa lisätä uuden apinan kaivamaan ojaa. 
# Uusi apina töihin laitettaessa kannattaa huomioida se, että apina kannattaa sijoittaa kohtaan, 
# mistä oja on tällä hetkellä vielä kaivamatta. Jos vahingossa laitat apinan kaivamaan ojaa kohdasta, 
# johon on jo kaivettu ojaa, siitä tulee siitä kohdasta vain vastaavasti syvempi, 
# eli oja muuttuu vaikkapa "nolla" syvyisestä kohdasta "miinus ykköseksi".  
# Tai, jos huonosti organisoidussa ojankaivuussa "miinus ykkösen syvyistä" ojaa kaivetaan lisää, 
# siitä tulee tietysti "miinus kakkosen syvyinen"

# -lisää vastaava toiminto Kernestille.

# -havainnollista saarella sitä, miten ojan kaivuu edistyy, eli sitä, 
# miten "ojamatriisi" muuttuu havainnollisesti näyttöruudulla sitä mukaa kun apinat kaivavat 
# ojiaan kohti merta.
 
# Kun nämä edellä kuvatut vaiheet on tehty, olet ansainnut tehtävästä yhteensä kolme pistettä.

def k_hakee_apinan(apina_id):
    global apinoiden_tiedot
    # Etsitään satunnainen y-koordinaatti
    y_koordinaatti = random.randint(0, 249)
    y_koordinaatti_oja = round(y_koordinaatti // 2.5)
    
    # Tarkistetaan, ettei samaa koordinaattia ole jo listassa
    while any(apina['y_koordinaatti'] == y_koordinaatti and apina['y_koordinaatti_oja'] == y_koordinaatti_oja for apina in apinoiden_tiedot):
        y_koordinaatti = random.randint(0, 249)
        y_koordinaatti_oja = round(y_koordinaatti // 2.5)
        while oja_kernesti[y_koordinaatti_oja][0] == 0:
            y_koordinaatti = random.randint(0, 249)
            y_koordinaatti_oja = round(y_koordinaatti // 2.5)
            print("Arvotaan uusi koordinaatti!")
        
    # Määritetään x-koordinaatti Ernestin ojan varrelle
    x_koordinaatti = 0

    # Poistetaan apina metsästä (jos metsässä on apinoita)
    apina_loytynyt = False
    for i in range(20):
        for j in range(60):
            if metsa[i][j] == 0:  # Apina löytyy metsästä
                metsa[i][j] = 1 # Poistetaan apina metsästä
                paivita_metsa(i, j, 1) # Päivitetään metsä  

                autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 540, y_koordinaatti, 545, y_koordinaatti + 5) 
                
                # Päivitetään apinan tiedot
                apina = apinoiden_tiedot[apina_id]
                apina['henkilo'] = "Kernesti"
                apina['y_koordinaatti'] = y_koordinaatti
                apina['y_koordinaatti_oja'] = y_koordinaatti_oja
                apina['tila'] = 1
                print("Apinan päivitetyt tiedot:", apina)
                apina_loytynyt = True
                break
        if apina_loytynyt:
            break

    if not apina_loytynyt:
        print("Metsässä ei ole apinoita!")

def k_apina_kaivaa_ojaa(apina_id):
    global apinoiden_tiedot
    if len(apinoiden_tiedot) == 0:
        print("Ei apinoita kaivamassa!")
        return
    # Apinan sijainti ojan varrella ja ojassa
    apina_sijainti_ojalla = apinoiden_tiedot[apina_id]['y_koordinaatti']
    apina_sijainti_ojassa = apinoiden_tiedot[apina_id]['y_koordinaatti_oja']
    y_sijainti = apina_sijainti_ojalla  # Apinan sijainti ojan varrella
    apinoiden_tiedot[apina_id]['tila'] = 2  # Apina on kaivamassa
    kaivamis_nopeus = 1  # Kaivamisnopeus sekunteina
    kaivamis_kohta = apina_sijainti_ojassa 
    print(f"Apina aloittaa kaivamisen kohdasta: {kaivamis_kohta}")

    while kaivamis_kohta >= 0:  # Kaivetaan kunnes oja on kaivettu tai apina on kaivanut koko ojan
        if oja_kernesti[kaivamis_kohta][0] == 1:  # Jos ojaa ei ole vielä kaivettu tässä kohtaa
            oja_kernesti[kaivamis_kohta][0] = 0  # Kaiva kohta
            print(f"Apina kaivoi kohdan: {kaivamis_kohta}")
            
            # Soitetaan kaivamisääniefekti
            winsound.Beep(500, 10)  # Soitetaan kaivamisääniefekti

            # Siirretään apinaa ylöspäin ja piirretään apina
            y_sijainti = apina_sijainti_ojalla - (apina_sijainti_ojassa - kaivamis_kohta) * 2.5  # Päivitetään apinan sijainti
            autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 540, y_sijainti, 545, y_sijainti + 5)  # Piirretään apina
            time.sleep(kaivamis_nopeus)
            paivita_oja(oja_kernesti, 545, kaivamis_kohta)
            apina = apinoiden_tiedot[apina_id]
            apina['y_koordinaatti_oja'] = kaivamis_kohta
            print("Apinan päivitetyt tiedot:", apina)  
            kaivamis_kohta -= 1
            kaivamis_nopeus *= 2
        else:  # Jos oja on jo kaivettu tässä kohtaa
            oja_kernesti[kaivamis_kohta][0] -= 1  # Kaiva kohta
            print(f"Oja on jo kaivettu tässä kohtaa! Vähennettiin arvosta yksi, uusi arvo: {oja_kernesti[kaivamis_kohta][0]}")
            break
    print(oja_kernesti)

def k_hakee_satunnainen_apina():
    if apinoiden_tiedot:  # Varmistetaan, että listassa on apinoita
        satunnainen_apina_id = random.choice([apina['id'] for apina in apinoiden_tiedot if apina.get('henkilo') == None])
        k_hakee_apinan(satunnainen_apina_id)
    else:
        print("Ei apinoita saatavilla!")

def apina_kaivaa_kernestin_ojaa():
    # Suodatetaan ne apinat, joiden tila on 1 eli valmiita kaivamaan
    apinat_ojalla = [apina['id'] for apina in apinoiden_tiedot if apina.get('tila') == 1]
    
    if apinat_ojalla:  # Varmistetaan, että on apinoita ojalla
        satunnainen_apina_id = random.choice(apinat_ojalla)
        print(f"Apina {satunnainen_apina_id} aloittaa kaivamisen.")
        k_apina_kaivaa_ojaa(satunnainen_apina_id)
    else:
        print("Ei apinoita kaivamassa ojaa!")

# Luodaan funktio, joka tarkistaa, onko oja kaivettu tästä kohdasta
def tarkista_oja(oja, kaivamis_kohta):
    if oja[kaivamis_kohta][0] == 1:  # Jos ojaa ei ole vielä kaivettu tässä kohtaa
        return True
    else:
        return False

# Luodaan painike, jolla Kernesti hakee apinan
kernesti_hakee_apinan = tk.Button(ikkuna, text="Kernesti hakee apinan", command=lambda: threading.Thread(target=k_hakee_satunnainen_apina).start(), **painikkeiden_tyyli)
kernesti_hakee_apinan.place(x=693, y=100)

# Luodaan painike, jolla apina alkaa kaivamaan ojaa
k_apina_kaivamaan_ojaa = tk.Button(ikkuna, text="Apina kaivaa kernestin ojaa", command=lambda: threading.Thread(target=apina_kaivaa_kernestin_ojaa).start(), **painikkeiden_tyyli)
k_apina_kaivamaan_ojaa.place(x=693, y=150)

# Luodaan painike, joka tulostaa Kernestin ojan tilan
kernestin_ojan_tila = tk.Button(ikkuna, text="Kernestin ojan tila", command=lambda: print(oja_kernesti), **painikkeiden_tyyli)
kernestin_ojan_tila.place(x=693, y=200)

# Käynnistä ohjelma
ikkuna.mainloop()

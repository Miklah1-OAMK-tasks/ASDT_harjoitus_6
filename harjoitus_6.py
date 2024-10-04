# Tehty 4/5

# Videolinkki: https://youtu.be/eYAP9dAxsu4
# Github: https://github.com/Miklah1-OAMK-tasks/ASDT_harjoitus_6

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
autiosaari = tk.Canvas(ikkuna, width=800, height=600, bg='#eab676', highlightthickness=0)  # Luodaan autiosaari
autiosaari.place(anchor='center', relx=0.5, rely=0.5) # Asetetaan autiosaari keskelle ikkunaa

# Määritellään uima-allas (20x60), aluksi täynnä nollia (tyhjä)
uima_allas = [[0 for _ in range(60)] for _ in range(20)]

# Määritellään ojat (100x1), aluksi täynnä ykkösiä (hiekkaa)
oja_ernesti = [[1] for _ in range(100)]
oja_kernesti = [[1] for _ in range(100)]

# Määritellään metsäalue (20x60) numpytaulukkona, täynnä ykkösiä (metsää)
metsa = np.ones((20, 60), dtype=int)

# Funktio, joka piirtää uima-altaan
def piirra_uima_allas():
    ruudun_koko = 5     # Yhden ruudun koko 5x5 pikseliä
    for i in range(20): # luodaan taulukko 20x60
        for j in range(60):  
            x0, y0 = j * ruudun_koko, i * ruudun_koko   # Ruudun vasemman yläkulman koordinaatit
            x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko # Ruudun oikean alakulman koordinaatit
            väri = "#eab676" if uima_allas[i][j] == 0 else "blue" # Hiekka = ruskea, vesi = sininen  
            autiosaari.create_rectangle(x0 + 250, y0 + 250, x1 + 250, y1 + 250, fill=väri, outline='grey') # Piirretään uima-allas

# Funktio, joka piirtää ojat ja ottaa parametreina ojan (ernestin tai kernestin) ja aloituspisteen x- ja y-koordinaatit
def piirra_oja(oja, x_alku, y_alku):
    ruudun_koko = 2.5       # Yhden ruudun koko 2.5x2.5 pikseliä
    for i in range(100):    # luodaan taulukko 100x1
        x0, y0 = x_alku, y_alku - i * ruudun_koko   # Ruudun vasemman yläkulman koordinaatit
        x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko # Ruudun oikean alakulman koordinaatit 
        autiosaari.create_rectangle(x0, y0, x1, y1, fill="#eab676", outline='grey') # Piirretään oja

# Funktio, joka piirtää metsäalueen
def piirra_metsa():
    ruudun_koko = 5         # Yhden ruudun koko 5x5 pikseliä
    for i in range(20):     # luodaan taulukko 20x60
        for j in range(60):
            if metsa[i][j] == 1:  # Piirretään vain metsäruudut
                x0, y0 = j * ruudun_koko, i * ruudun_koko   # Ruudun vasemman yläkulman koordinaatit
                x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko # Ruudun oikean alakulman koordinaatit
                autiosaari.create_rectangle(x0 + 250, y0 + 400, x1 + 250, y1 + 400, fill="green", outline='green') # Piirretään metsä

# Piirretään aluksi uima-allas ja ojat (täynnä hiekkaa), sekä metsäalue
piirra_uima_allas() # Piirretään uima-allas
piirra_oja(oja_ernesti, 250, 246)  # Ernestin oja
piirra_oja(oja_kernesti, 545, 246)  # Kernestin oja
piirra_metsa()  # Piirretään metsäalue

# SUUNNITELMA TURVALLISESTA UIMA-ALTAASTA (1 PISTETTÄ) PÄÄTTYY TÄHÄN

# RAKENTAMISEEN TARVITTAVAN TYÖVOIMAN HANKINTA (2 PISTETTÄ) ALKAA TÄSTÄ

apinoiden_tiedot = []   # Lista apinoiden tiedoista 

# Funktio, jolla luodaan apinoita satunnaisiin paikkoihin metsään
def luo_apina():
    for i in range(10):  # Lisätään 10 apinaa
        apina_id = len(apinoiden_tiedot) # Luodaan apinan id
        apina_x = random.randint(0, 59)  # Arvotaan apinan x-koordinaatti
        apina_y = random.randint(0, 19)  # Arvotaan apinan y-koordinaatti
        metsa[apina_y][apina_x] = 0      # Asetetaan apina metsään
        
        ruudun_koko = 5 # Yhden ruudun koko 5x5 pikseliä
        x0, y0 = apina_x * ruudun_koko, apina_y * ruudun_koko   # Ruudun vasemman yläkulman koordinaatit
        x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko             # Ruudun oikean alakulman koordinaatit
        apinan_kuva = autiosaari.create_oval(x0 + 250, y0 + 400, x1 + 250, y1 + 400, fill='brown', outline='black') # Piirretään apina

        # Tallennetaan apinan tiedot listaan
        apinoiden_tiedot.append({
            "id": apina_id,             # Apinan id
            "tila": 0,                  # 0 = joutilaana, 1 = valmiina kaivamaan, 2 = kaivamassa
            "henkilo": None,            # Apinan omistaja
            "x": apina_x,               # Apinan x-koordinaatti
            "y": apina_y,               # Apinan y-koordinaatti
            "kuva": apinan_kuva,        # Apinan kuva
            "y_koordinaatti": None,     # Apinan y-koordinaatti ojan varrella
            "y_koordinaatti_oja": None, # Apinan y-koordinaatti ojassa
            "säie": None,                # Apinan säie
        })
        paivita_metsa(apina_y, apina_x, 0)  # Päivitetään metsä
    print("10 apinaa lisätty metsään!")     # Tulostetaan viesti

# Funktio, jolla Ernesti hakee apinan metsästä ja siirtää sen ojan varrelle
def e_hakee_apinan(apina_id):
    global apinoiden_tiedot
    # Etsitään satunnainen y-koordinaatti Ernestin ojan varrelta
    y_koordinaatti = random.randint(0, 249)             # Arvotaan y-koordinaatti (0-249) ojan varrelta
    y_koordinaatti_oja = round(y_koordinaatti // 2.5)   # Muutetaan y-koordinaatti ojan y-koordinaatiksi (0-99) 
    
    # Tarkistetaan, ettei samaa koordinaattia ole jo listassa ja jos on, arvotaan uusi koordinaatti
    while any(apina['y_koordinaatti'] == y_koordinaatti and apina['y_koordinaatti_oja'] == y_koordinaatti_oja for apina in apinoiden_tiedot):
        y_koordinaatti = random.randint(0, 249)
        y_koordinaatti_oja = round(y_koordinaatti // 2.5)

    # Poistetaan apina metsästä (jos metsässä on apinoita)
    apina_loytynyt = False
    for i in range(20):
        for j in range(60):
            if metsa[i][j] == 0:        # Apina löytyy metsästä
                metsa[i][j] = 1         # Poistetaan apina metsästä
                paivita_metsa(i, j, 1)  # Päivitetään metsä
                apina_loytynyt = True   # Apina löytyi

                # Piirretään apina ojan varrelle
                autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 245, y_koordinaatti, 250, y_koordinaatti + 5)
                
                # Päivitetään apinan tiedot
                apina = apinoiden_tiedot[apina_id]                  # Haetaan apinan id
                apina['henkilo'] = "Ernesti"                        # Asetetaan apinan omistajaksi Ernesti
                apina['y_koordinaatti'] = y_koordinaatti            # Asetetaan apinan y-koordinaatti
                apina['y_koordinaatti_oja'] = y_koordinaatti_oja    # Asetetaan apinan y-koordinaatti ojan varrella
                apina['tila'] = 1                                   # Asetetaan apinan tilaksi 1 (valmiina kaivamaan)
                print("Apinan päivitetyt tiedot:", apina)           # Tulostetaan apinan päivitetyt tiedot
                break                                               # Lopetetaan silmukka, kun apina on löytynyt
        if apina_loytynyt:
            break

    if not apina_loytynyt:                  # Jos apinaa ei löydy metsästä
        print("Metsässä ei ole apinoita!")  # Tulostetaan viesti

# Funktio, joka päivittää metsän tilan
def paivita_metsa(i, j, arvo):  # Ottaa parametreina i ja j (apinan sijainti) ja arvon (0 = apina, 1 = metsä)
    metsa[i][j] = arvo 
    ruudun_koko = 5             # Yhden ruudun koko 5x5 pikseliä
    x0, y0 = j * ruudun_koko, i * ruudun_koko   # Ruudun vasemman yläkulman koordinaatit
    x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko # Ruudun oikean alakulman koordinaatit
    väri = "brown" if arvo == 0 else "green"    # Apina = ruskea, metsä = vihreä
    autiosaari.create_rectangle(x0 + 250, y0 + 400, x1 + 250, y1 + 400, fill=väri, outline='green') # Piirretään metsä

# Funktio, joka siirtää apinan ojan varrelle ja aloittaa kaivamisen
def e_apina_kaivaa_ojaa(apina_id):          # Ottaa parametrina apinan id:n
    global apinoiden_tiedot                 # Otetaan käyttöön globaali muuttuja apinoiden_tiedot   
    if len(apinoiden_tiedot) == 0:          # Jos apinoita ei ole
        print("Ei apinoita kaivamassa!")    # Tulostetaan viesti
        return                              # Poistutaan funktiosta
    
    # Apinan sijainti ojan varrella ja ojassa
    apina_sijainti_ojalla = apinoiden_tiedot[apina_id]['y_koordinaatti']        # Apinan sijainti ojan varrella
    kaivamisen_aloituskohta_ojassa = apinoiden_tiedot[apina_id]['y_koordinaatti_oja']    # Apinan sijainti ojassa
    y_sijainti = apina_sijainti_ojalla  # Apinan sijainti ojan varrella
    apinoiden_tiedot[apina_id]['tila'] = 2  # Apina on kaivamassa

    kaivamis_nopeus = 1  # Kaivamisnopeus sekunteina

    kaivamis_kohta_nyt = kaivamisen_aloituskohta_ojassa # Kaivamisen aloituskohta
    print(f"Apina aloittaa kaivamisen kohdasta: {kaivamis_kohta_nyt}") # Tulostetaan aloituskohta

    while kaivamis_kohta_nyt >= 0 and apinoiden_tiedot[apina_id]['tila'] == 2 :  # Kaivetaan kunnes oja on kaivettu tai apina on kaivanut koko ojan
        if oja_ernesti[kaivamis_kohta_nyt][0] == 1: # Jos ojaa ei ole vielä kaivettu tässä kohtaa
            oja_ernesti[kaivamis_kohta_nyt][0] = 0  # Kaiva kohta
            
            print(f"Apina {apinoiden_tiedot[apina_id]['id']} kaivoi kohdan: {kaivamis_kohta_nyt}")
            
            # Soitetaan kaivamisääniefekti
            winsound.Beep(500, 10)  # Soitetaan kaivamisääniefekti

            # Siirretään apinaa ylöspäin seuraavaan kaivamiskohtaan ja piirretään apina
            y_sijainti = apina_sijainti_ojalla - (kaivamisen_aloituskohta_ojassa - kaivamis_kohta_nyt) * 2.5  # Päivitetään apinan sijainti
            autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 245, y_sijainti, 250, y_sijainti + 5) # Piirretään apina
            time.sleep(kaivamis_nopeus)  # Apina pitää tauon kaivamisnopeuden mukaan

            paivita_oja(oja_ernesti, 250, kaivamis_kohta_nyt)  # Päivitetään oja visuaalisesti
            kaivamis_kohta_nyt -= 1  # Siirrytään seuraavaan kaivamiskohtaan
            kaivamis_nopeus *= 2 # Väsymys: Kaivaminen hidastuu kaksinkertaiseksi joka kerta

        else:  # Jos oja on jo kaivettu tässä kohtaa
            oja_ernesti[kaivamis_kohta_nyt][0] -= 1  # Kaiva kohta
            print(f"Oja on jo kaivettu tässä kohtaa! Uusi arvo: {oja_ernesti[kaivamis_kohta_nyt][0]}")
            break

# Funktio, joka päivittää ojan visuaalisesti
def paivita_oja(oja, x_alku, kaivamis_kohta_nyt):   # Ottaa parametreina ojan, aloituspisteen x-koordinaatin ja kaivamiskohdan
    ruudun_koko = 2.5                           # Yhden ruudun koko 2.5x2.5 pikseliä
    x0 = x_alku                                 # Ojan vasemman yläkulman x-koordinaatti
    y0 = kaivamis_kohta_nyt * ruudun_koko           # Ojan vasemman yläkulman y-koordinaatti
    x1, y1 = x0 + ruudun_koko, y0 + ruudun_koko # Ojan oikean alakulman koordinaatit
    
    if oja[kaivamis_kohta_nyt][0] == 0:     # Jos oja on kaivettu, väri on keltainen
        väri = "yellow"
        ulkoreuna = "yellow"
    elif oja[kaivamis_kohta_nyt][0] == 1:   # Jos oja on kaivamaton, väri on ruskea
        väri="#eab676"
        ulkoreuna = "grey"
    elif oja[kaivamis_kohta_nyt][0] == 2:   # Jos oja on täytetty vedellä, väri on sininen
        väri = "blue"
        ulkoreuna = "blue"
    elif oja[kaivamis_kohta_nyt][0] < 0:    # Jos ojaa on kaivettu liikaa, väri on punainen 
        väri = "red"
        ulkoreuna = "red"

    # Päivitetään kaivamiskohta
    autiosaari.create_rectangle(x0, y0, x1, y1, fill=väri, outline=ulkoreuna)

# Funktio, joka hakee satunnaisen apinan ja siirtää sen ojan varrelle
def e_hakee_satunnainen_apina():
    if apinoiden_tiedot:  # Varmistetaan, että listassa on apinoita
        satunnainen_apina_id = random.choice([apina['id'] for apina in apinoiden_tiedot if apina.get('henkilo') == None]) # Valitaan satunnainen apina, joka ei ole vielä valittu
        e_hakee_apinan(satunnainen_apina_id) # Kutsutaan funktiota, joka siirtää apinan ojan varrelle
    else:
        print("Ei apinoita saatavilla!")

# Funktio, jolla apina alkaa kaivamaan ojaa
def apina_kaivaa_ernestin_ojaa():
    # Suodatetaan ne apinat, joiden tila on 1 eli valmiita kaivamaan ja omistaja on Ernesti
    apinat_ojalla = [apina['id'] for apina in apinoiden_tiedot if apina.get('tila') == 1 and apina.get('henkilo') == "Ernesti"]
    
    if apinat_ojalla:  # Varmistetaan, että on apinoita ojalla
        satunnainen_apina_id = random.choice(apinat_ojalla) # Valitaan satunnainen Ernestin apina, joka on valmiina kaivamaan
        print(f"Apina {satunnainen_apina_id} aloittaa kaivamisen.") # Tulostetaan viesti
        e_apina_kaivaa_ojaa(satunnainen_apina_id) # Kutsutaan funktiota, jolla aloitetaan kaivaminen
    else:
        print("Ei apinoita kaivamassa ojaa!") # Tulostetaan viesti, jos apinoita ei ole ojalla

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

def ojan_tila_e():
    print(f"Ernestin oja: {oja_ernesti}")   # Tulostetaan Ernestin ojan tila

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
ernestin_ojan_tila = tk.Button(ikkuna, text="Ernestin ojan tila", command= ojan_tila_e, **painikkeiden_tyyli)   
ernestin_ojan_tila.place(x=100, y=200)

# RAKENTAMISEEN TARVITTAVAN TYÖVOIMAN HANKINTA (2 PISTETTÄ) PÄÄTTYY TÄHÄN

# YHDESSÄ ENEMMÄN (3 PISTETTÄ) ALKAA TÄSTÄ

# Funktio, joka hakee apinan metsästä ja siirtää sen ojan varrelle
def k_hakee_apinan(apina_id):
    global apinoiden_tiedot # Otetaan käyttöön globaali muuttuja apinoiden_tiedot
    # Etsitään satunnainen y-koordinaatti
    y_koordinaatti = random.randint(0, 249)             # Arvotaan y-koordinaatti (0-249) ojan varrelta
    y_koordinaatti_oja = round(y_koordinaatti // 2.5)   # Muutetaan y-koordinaatti ojan y-koordinaatiksi (0-99)
    
    # Tarkistetaan, ettei samaa koordinaattia ole jo listassa ja jos on, arvotaan uusi koordinaatti
    while any(apina['y_koordinaatti'] == y_koordinaatti and apina['y_koordinaatti_oja'] == y_koordinaatti_oja for apina in apinoiden_tiedot): 
        y_koordinaatti = random.randint(0, 249) 
        y_koordinaatti_oja = round(y_koordinaatti // 2.5)
        
    # Poistetaan apina metsästä (jos metsässä on apinoita)
    apina_loytynyt = False
    for i in range(20):
        for j in range(60):
            if metsa[i][j] == 0:  # Apina löytyy metsästä
                metsa[i][j] = 1 # Poistetaan apina metsästä
                paivita_metsa(i, j, 1) # Päivitetään metsä 
                apina_loytynyt = True 

                autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 540, y_koordinaatti, 545, y_koordinaatti + 5) 
                
                # Päivitetään apinan tiedot
                apina = apinoiden_tiedot[apina_id]                  # Haetaan apinan id
                apina['henkilo'] = "Kernesti"                       # Asetetaan apinan omistajaksi Kernesti
                apina['y_koordinaatti'] = y_koordinaatti            # Asetetaan apinan y-koordinaatti
                apina['y_koordinaatti_oja'] = y_koordinaatti_oja    # Asetetaan apinan y-koordinaatti ojan varrella
                apina['tila'] = 1                                   # Asetetaan apinan tilaksi 1 (valmiina kaivamaan)
                print("Apinan päivitetyt tiedot:", apina)           # Tulostetaan apinan päivitetyt tiedot
                break                                               # Lopetetaan silmukka, kun apina on löytynyt
        if apina_loytynyt:
            break

    if not apina_loytynyt:                 # Jos apinaa ei löydy metsästä
        print("Metsässä ei ole apinoita!") # Tulostetaan viesti

# Funktio, joka siirtää apinan ojan varrelle ja aloittaa kaivamisen
def k_apina_kaivaa_ojaa(apina_id):
    global apinoiden_tiedot                 # Otetaan käyttöön globaali muuttuja apinoiden_tiedot
    if len(apinoiden_tiedot) == 0:          # Jos apinoita ei ole
        print("Ei apinoita kaivamassa!")    # Tulostetaan viesti
        return                              # Poistutaan funktiosta
    # Apinan sijainti ojan varrella ja ojassa
    apina_sijainti_ojalla = apinoiden_tiedot[apina_id]['y_koordinaatti']        # Apinan sijainti ojan varrella
    kaivamisen_aloituskohta_ojassa = apinoiden_tiedot[apina_id]['y_koordinaatti_oja']    # Kaivamiskohta ojassa
    y_sijainti = apina_sijainti_ojalla  # Apinan sijainti ojan varrella
    apinoiden_tiedot[apina_id]['tila'] = 2  # Apina on kaivamassa
    kaivamis_nopeus = 1  # Kaivamisnopeus sekunteina
    kaivamis_kohta_nyt = kaivamisen_aloituskohta_ojassa # Kaivamisen aloituskohta
    print(f"Apina aloittaa kaivamisen kohdasta: {kaivamis_kohta_nyt}")

    while kaivamis_kohta_nyt >= 0 and apinoiden_tiedot[apina_id]['tila'] == 2 :  # Kaivetaan kunnes oja on kaivettu tai apina on kaivanut koko ojan
        if oja_kernesti[kaivamis_kohta_nyt][0] == 1:  # Jos ojaa ei ole vielä kaivettu tässä kohtaa
            oja_kernesti[kaivamis_kohta_nyt][0] = 0  # Kaiva kohta
            print(f"Apina {apinoiden_tiedot[apina_id]['id']} kaivoi kohdan: {kaivamis_kohta_nyt}")
            
            # Soitetaan kaivamisääniefekti
            winsound.Beep(500, 10)  # Soitetaan kaivamisääniefekti

            # Siirretään apinaa ylöspäin ja piirretään apina
            y_sijainti = apina_sijainti_ojalla - (kaivamisen_aloituskohta_ojassa - kaivamis_kohta_nyt) * 2.5  # Päivitetään apinan sijainti
            autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 540, y_sijainti, 545, y_sijainti + 5)  # Piirretään apina
            time.sleep(kaivamis_nopeus) # Apina pitää tauon kaivamisnopeuden mukaan
            paivita_oja(oja_kernesti, 545, kaivamis_kohta_nyt) # Päivitetään oja visuaalisesti
            apina = apinoiden_tiedot[apina_id] # Haetaan apinan id
            apina['y_koordinaatti_oja'] = kaivamis_kohta_nyt # Päivitetään apinan y-koordinaatti ojan varrella
            print("Apinan päivitetyt tiedot:", apina)      # Tulostetaan apinan päivitetyt tiedot
            kaivamis_kohta_nyt -= 1 # Siirrytään seuraavaan kaivamiskohtaan
            kaivamis_nopeus *= 2 # Väsymys: Kaivaminen hidastuu kaksinkertaiseksi joka kerta
        else:  # Jos oja on jo kaivettu tässä kohtaa
            oja_kernesti[kaivamis_kohta_nyt][0] -= 1  # Kaiva kohta
            print(f"Oja on jo kaivettu tässä kohtaa! Uusi arvo: {oja_kernesti[kaivamis_kohta_nyt][0]}")
            break

def k_hakee_satunnainen_apina():
    if apinoiden_tiedot:  # Varmistetaan, että listassa on apinoita
        satunnainen_apina_id = random.choice([apina['id'] for apina in apinoiden_tiedot if apina.get('henkilo') == None]) # Valitaan satunnainen apina, joka ei ole vielä valittu
        k_hakee_apinan(satunnainen_apina_id) # Kutsutaan funktiota, joka siirtää apinan ojan varrelle
    else:
        print("Ei apinoita saatavilla!")

def apina_kaivaa_kernestin_ojaa():
    # Suodatetaan ne apinat, joiden tila on 1 eli valmiita kaivamaan
    apinat_ojalla = [apina['id'] for apina in apinoiden_tiedot if apina.get('tila') == 1 and apina.get('henkilo') == "Kernesti"] # Valitaan apinat, jotka ovat valmiina kaivamaan ja omistaja on Kernesti
    
    if apinat_ojalla:  # Varmistetaan, että on apinoita ojalla
        satunnainen_apina_id = random.choice(apinat_ojalla) # Valitaan satunnainen Kernestin apina, joka on valmiina kaivamaan
        print(f"Apina {satunnainen_apina_id} aloittaa kaivamisen.") # Tulostetaan viesti
        k_apina_kaivaa_ojaa(satunnainen_apina_id) # Kutsutaan funktiota, jolla aloitetaan kaivaminen
    else:
        print("Ei apinoita kaivamassa ojaa!") # Tulostetaan viesti, jos apinoita ei ole ojalla

def ojan_tila_k():
    print(f"Kernestin oja: {oja_kernesti}")   # Tulostetaan Kernestin ojan tila

# Luodaan painike, jolla Kernesti hakee apinan
kernesti_hakee_apinan = tk.Button(ikkuna, text="Kernesti hakee apinan", command=lambda: threading.Thread(target=k_hakee_satunnainen_apina).start(), **painikkeiden_tyyli)
kernesti_hakee_apinan.place(x=693, y=100)

# Luodaan painike, jolla apina alkaa kaivamaan ojaa
k_apina_kaivamaan_ojaa = tk.Button(ikkuna, text="Apina kaivaa kernestin ojaa", command=lambda: threading.Thread(target=apina_kaivaa_kernestin_ojaa).start(), **painikkeiden_tyyli)
k_apina_kaivamaan_ojaa.place(x=693, y=150)

# Luodaan painike, joka tulostaa Kernestin ojan tilan
kernestin_ojan_tila = tk.Button(ikkuna, text="Kernestin ojan tila", command=ojan_tila_k, **painikkeiden_tyyli)
kernestin_ojan_tila.place(x=693, y=200)

# YHDESSÄ ENEMMÄN (3 PISTETTÄ) PÄÄTTYY TÄHÄN

# OPTIMAALINEN RESURSSIEN KÄYTTÖ (4 PISTETTÄ) ALKAA TÄSTÄ

# Funktio, joka täyttää ojan uudelleen ja pysäyttää apinoiden säikeet
def tayta_oja(oja):
    poista_apinat_ojasta()  # Poistetaan apinat ojasta
    # Täytetään oja hiekalla
    if oja == oja_ernesti:    
        for i in range(100):
            oja_ernesti[i][0] = 1  # Asetetaan ojan arvoksi 1
            piirra_oja(oja_ernesti, 250, 246)  # Ernestin oja
    elif oja == oja_kernesti:
        for i in range(100):
            oja_kernesti[i][0] = 1  # Asetetaan ojan arvoksi 1
            piirra_oja(oja_kernesti, 545, 246)

# Funktio, joka sijoittaa apinan ojan varrelle ja välittömästi töihin sekunnin välein 10 apinaan asti
def apinat_toihin(oja, x_alku, henkilo):
    global apinoiden_tiedot

    def laheta_apina_tyohon(apina_id, henkilo):
        if henkilo == "Ernesti":
            e_apina_kaivaa_ojaa2(apina_id)  # Ernestin toiminto
        elif henkilo == "Kernesti":
            k_apina_kaivaa_ojaa2(apina_id)  # Kernestin toiminto

    # Sijoitetaan ensimmäinen apina satunnaisesti
    time.sleep(1)  # Odotetaan sekunti ennen ensimmäisen apinan sijoittamista
    apina_id = random.choice([apina['id'] for apina in apinoiden_tiedot if apina.get('henkilo') is None])
    
    if henkilo == "Ernesti":
        e_hakee_apinan2(apina_id)  # Ernestin toiminto
    elif henkilo == "Kernesti":
        k_hakee_apinan2(apina_id)  # Kernestin toiminto

    # Laita ensimmäinen apina töihin omassa säikeessään ja tallenna säie apinan tietoihin
    apinoiden_tiedot[apina_id]['säie'] = threading.Thread(target=laheta_apina_tyohon, args=(apina_id, henkilo))
    apinoiden_tiedot[apina_id]['säie'].start()
    print(apinoiden_tiedot[apina_id])   

    # Sijoitetaan seuraavat 9 apinaa kiinteisiin paikkoihin
    for apina_numero in range(1, 10):
        time.sleep(1)  # Odotetaan sekunti ennen seuraavan apinan sijoittamista
        apina_id = random.choice([apina['id'] for apina in apinoiden_tiedot if apina.get('henkilo') is None])  # Valitaan satunnainen apina
        
        if henkilo == "Ernesti":
            e_hakee_apinan2(apina_id)  # Ernestin toiminto
        elif henkilo == "Kernesti":
            k_hakee_apinan2(apina_id)  # Kernestin toiminto

        # Määritellään kaivamispaikka
        kaivamispaikka = 110 - (apina_numero * 11)  # Sijoitetaan yhdentoista välein alkaen 99:stä

        # Asetetaan apinan sijainti ojan varrelle
        apinoiden_tiedot[apina_id]['y_koordinaatti_oja'] = kaivamispaikka  # Määritellään apinan sijainti
        apinoiden_tiedot[apina_id]['y_koordinaatti'] = kaivamispaikka * 2.5  # Määritellään apinan sijainti ojan varrella

        if henkilo == "Ernesti":
            # Piirretään apina oikeaan kohtaan
            y_koordinaatti = apinoiden_tiedot[apina_id]['y_koordinaatti']  # Lasketaan y-koordinaatti
            autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 245, y_koordinaatti, 250, y_koordinaatti + 5)
        elif henkilo == "Kernesti":
            # Piirretään apina oikeaan kohtaan
            y_koordinaatti = apinoiden_tiedot[apina_id]['y_koordinaatti']  # Lasketaan y-koordinaatti
            autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 540, y_koordinaatti, 545, y_koordinaatti + 5)

        # Laita apina töihin omassa säikeessään ja tallenna säie apinan tietoihin
        apinoiden_tiedot[apina_id]['säie'] = threading.Thread(target=laheta_apina_tyohon, args=(apina_id, henkilo))
        apinoiden_tiedot[apina_id]['säie'].start()
        print(apinoiden_tiedot[apina_id])

# Funktio, jolla Ernesti hakee apinan metsästä ja siirtää sen ojan varrelle
def e_hakee_apinan2(apina_id):
    global apinoiden_tiedot
    # Etsitään satunnainen y-koordinaatti Ernestin ojan varrelta
    y_koordinaatti = random.randint(0, 249)             # Arvotaan y-koordinaatti (0-249) ojan varrelta
    y_koordinaatti_oja = round(y_koordinaatti // 2.5)   # Muutetaan y-koordinaatti ojan y-koordinaatiksi (0-99) 
    
    # Tarkistetaan, ettei samaa koordinaattia ole jo listassa ja jos on, arvotaan uusi koordinaatti
    while any(apina['y_koordinaatti'] == y_koordinaatti and apina['y_koordinaatti_oja'] == y_koordinaatti_oja for apina in apinoiden_tiedot):
        y_koordinaatti = random.randint(0, 249)
        y_koordinaatti_oja = round(y_koordinaatti // 2.5)

    # Poistetaan apina metsästä (jos metsässä on apinoita)
    apina_loytynyt = False
    for i in range(20):
        for j in range(60):
            if metsa[i][j] == 0:        # Apina löytyy metsästä
                metsa[i][j] = 1         # Poistetaan apina metsästä
                paivita_metsa(i, j, 1)  # Päivitetään metsä
                apina_loytynyt = True   # Apina löytyi

                # Piirretään apina ojan varrelle
                autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 245, y_koordinaatti, 250, y_koordinaatti + 5)
                
                # Päivitetään apinan tiedot
                apina = apinoiden_tiedot[apina_id]                  # Haetaan apinan id
                apina['henkilo'] = "Ernesti"                        # Asetetaan apinan omistajaksi Ernesti
                apina['y_koordinaatti'] = y_koordinaatti            # Asetetaan apinan y-koordinaatti
                apina['y_koordinaatti_oja'] = y_koordinaatti_oja    # Asetetaan apinan y-koordinaatti ojan varrella
                apina['tila'] = 1                                   # Asetetaan apinan tilaksi 1 (valmiina kaivamaan)
                print("Apinan päivitetyt tiedot:", apina)           # Tulostetaan apinan päivitetyt tiedot
                break                                               # Lopetetaan silmukka, kun apina on löytynyt
        if apina_loytynyt:
            break

    if not apina_loytynyt:                  # Jos apinaa ei löydy metsästä
        print("Metsässä ei ole apinoita!")  # Tulostetaan viesti

# Funktio, joka siirtää apinan ojan varrelle ja aloittaa kaivamisen
def e_apina_kaivaa_ojaa2(apina_id):  # Ottaa parametrina apinan id:n
    global apinoiden_tiedot
    if len(apinoiden_tiedot) == 0:  # Jos apinoita ei ole
        print("Ei apinoita kaivamassa!")  # Tulostetaan viesti
        return  # Poistutaan funktiosta
    
    # Apinan sijainti ojan varrella ja ojassa
    apina_sijainti_ojalla = apinoiden_tiedot[apina_id]['y_koordinaatti']  # Apinan sijainti ojan varrella
    kaivamisen_aloituskohta_ojassa = apinoiden_tiedot[apina_id]['y_koordinaatti_oja']  # Apinan sijainti ojassa
    y_sijainti = apina_sijainti_ojalla  # Apinan sijainti ojan varrella
    apinoiden_tiedot[apina_id]['tila'] = 2  # Apina on kaivamassa

    kaivamis_nopeus = 1  # Kaivamisnopeus sekunteina
    kaivamis_kohta_nyt = kaivamisen_aloituskohta_ojassa  # Kaivamisen aloituskohta

    print(f"Apina aloittaa kaivamisen kohdasta: {kaivamis_kohta_nyt}")  # Tulostetaan aloituskohta
        # Etsitään seuraava kohta, jossa ojaa ei ole vielä kaivettu (arvo on 1)
    while kaivamis_kohta_nyt >= 0:  # Kaivetaan kunnes oja on kaivettu tai apina on kaivanut koko ojan
        if oja_ernesti[kaivamis_kohta_nyt][0] == 1:  # Jos kohdassa on kaivettavaa
            oja_ernesti[kaivamis_kohta_nyt][0] = 0  # Kaiva kohta
            print(f"Apina {apinoiden_tiedot[apina_id]['id']} kaivoi kohdan: {kaivamis_kohta_nyt}")
            
            # Soitetaan kaivamisääniefekti
            winsound.Beep(500, 10)  # Soitetaan kaivamisääniefekti

            # Siirretään apinaa ylöspäin seuraavaan kaivamiskohtaan ja piirretään apina
            y_sijainti = apina_sijainti_ojalla - (kaivamisen_aloituskohta_ojassa - kaivamis_kohta_nyt) * 2.5  # Päivitetään apinan sijainti
            autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 245, y_sijainti, 250, y_sijainti + 5)  # Piirretään apina
            time.sleep(kaivamis_nopeus)  # Apina pitää tauon kaivamisnopeuden mukaan

            # Päivitetään oja visuaalisesti
            paivita_oja(oja_ernesti, 250, kaivamis_kohta_nyt)
            
            # Apina väsyy, joten kaivamisnopeus hidastuu
            kaivamis_nopeus *= 2
        else:
            # Jos kohdassa on jo kaivettu, siirrytään seuraavaan kohtaan
            if oja_ernesti[kaivamis_kohta_nyt][0] == 0:    
                print(f"Kohdassa {kaivamis_kohta_nyt} on jo kaivettu, siirrytään eteenpäin.")
                break
        
        # Siirrytään seuraavaan kaivamiskohtaan
        kaivamis_kohta_nyt -= 1

# Funktio, jolla apina alkaa kaivamaan ojaa
def apina_kaivaa_ernestin_ojaa2():
    # Suodatetaan ne apinat, joiden tila on 1 eli valmiita kaivamaan ja omistaja on Ernesti
    apinat_ojalla = [apina['id'] for apina in apinoiden_tiedot if apina.get('tila') == 1 and apina.get('henkilo') == "Ernesti"]
    
    if apinat_ojalla:  # Varmistetaan, että on apinoita ojalla
        satunnainen_apina_id = random.choice(apinat_ojalla) # Valitaan satunnainen Ernestin apina, joka on valmiina kaivamaan
        print(f"Apina {satunnainen_apina_id} aloittaa kaivamisen.") # Tulostetaan viesti
        e_apina_kaivaa_ojaa2(satunnainen_apina_id) # Kutsutaan funktiota, jolla aloitetaan kaivaminen
    else:
        print("Ei apinoita kaivamassa ojaa!") # Tulostetaan viesti, jos apinoita ei ole ojalla

# Funktio, joka siirtää apinan ojan varrelle ja aloittaa kaivamisen
def k_apina_kaivaa_ojaa2(apina_id):  # Ottaa parametrina apinan id:n
    global apinoiden_tiedot
    
    if len(apinoiden_tiedot) == 0:  # Jos apinoita ei ole
        print("Ei apinoita kaivamassa!")  # Tulostetaan viesti
        return  # Poistutaan funktiosta
    
    # Apinan sijainti ojan varrella ja ojassa
    apina_sijainti_ojalla = apinoiden_tiedot[apina_id]['y_koordinaatti']  # Apinan sijainti ojan varrella
    kaivamisen_aloituskohta_ojassa = apinoiden_tiedot[apina_id]['y_koordinaatti_oja']  # Apinan sijainti ojassa
    y_sijainti = apina_sijainti_ojalla  # Apinan sijainti ojan varrella
    apinoiden_tiedot[apina_id]['tila'] = 2  # Apina on kaivamassa

    kaivamis_nopeus = 1  # Kaivamisnopeus sekunteina
    kaivamis_kohta_nyt = kaivamisen_aloituskohta_ojassa  # Kaivamisen aloituskohta

    print(f"Apina aloittaa kaivamisen kohdasta: {kaivamis_kohta_nyt}")  # Tulostetaan aloituskohta

    # Etsitään seuraava kohta, jossa ojaa ei ole vielä kaivettu (arvo on 1)
    while kaivamis_kohta_nyt >= 0 and apinoiden_tiedot[apina_id]['tila'] == 2: 
        if oja_kernesti[kaivamis_kohta_nyt][0] == 1:  # Jos kohdassa on kaivettavaa
            oja_kernesti[kaivamis_kohta_nyt][0] = 0  # Kaiva kohta
            print(f"Apina {apinoiden_tiedot[apina_id]['id']} kaivoi kohdan: {kaivamis_kohta_nyt}")
            
            # Soitetaan kaivamisääniefekti
            winsound.Beep(500, 10)  # Soitetaan kaivamisääniefekti

            # Siirretään apinaa ylöspäin seuraavaan kaivamiskohtaan ja piirretään apina
            y_sijainti = apina_sijainti_ojalla - (kaivamisen_aloituskohta_ojassa - kaivamis_kohta_nyt) * 2.5  # Päivitetään apinan sijainti
            autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 540, y_sijainti, 545, y_sijainti + 5)  # Piirretään apina
            time.sleep(kaivamis_nopeus)  # Apina pitää tauon kaivamisnopeuden mukaan

            # Päivitetään oja visuaalisesti
            paivita_oja(oja_kernesti, 545, kaivamis_kohta_nyt)
            
            # Apina väsyy, joten kaivamisnopeus hidastuu
            kaivamis_nopeus *= 2
        else:
            # Jos kohdassa on jo kaivettu, siirrytään seuraavaan kohtaan
            if oja_kernesti[kaivamis_kohta_nyt][0] == 0:
                print(f"Kohdassa {kaivamis_kohta_nyt} on jo kaivettu, siirrytään eteenpäin.")
                break
        
        # Siirrytään seuraavaan kaivamiskohtaan
        kaivamis_kohta_nyt -= 1

# Funktio, joka hakee apinan metsästä ja siirtää sen ojan varrelle
def k_hakee_apinan2(apina_id):
    global apinoiden_tiedot # Otetaan käyttöön globaali muuttuja apinoiden_tiedot
    # Etsitään satunnainen y-koordinaatti
    y_koordinaatti = random.randint(0, 249)             # Arvotaan y-koordinaatti (0-249) ojan varrelta
    y_koordinaatti_oja = round(y_koordinaatti // 2.5)   # Muutetaan y-koordinaatti ojan y-koordinaatiksi (0-99)
    
    # Tarkistetaan, ettei samaa koordinaattia ole jo listassa ja jos on, arvotaan uusi koordinaatti
    while any(apina['y_koordinaatti'] == y_koordinaatti and apina['y_koordinaatti_oja'] == y_koordinaatti_oja for apina in apinoiden_tiedot): 
        y_koordinaatti = random.randint(0, 249) 
        y_koordinaatti_oja = round(y_koordinaatti // 2.5)
        
    # Poistetaan apina metsästä (jos metsässä on apinoita)
    apina_loytynyt = False
    for i in range(20):
        for j in range(60):
            if metsa[i][j] == 0:  # Apina löytyy metsästä
                metsa[i][j] = 1 # Poistetaan apina metsästä
                paivita_metsa(i, j, 1) # Päivitetään metsä 
                apina_loytynyt = True 

                autiosaari.coords(apinoiden_tiedot[apina_id]['kuva'], 540, y_koordinaatti, 545, y_koordinaatti + 5) 
                
                # Päivitetään apinan tiedot
                apina = apinoiden_tiedot[apina_id]                  # Haetaan apinan id
                apina['henkilo'] = "Kernesti"                       # Asetetaan apinan omistajaksi Kernesti
                apina['y_koordinaatti'] = y_koordinaatti            # Asetetaan apinan y-koordinaatti
                apina['y_koordinaatti_oja'] = y_koordinaatti_oja    # Asetetaan apinan y-koordinaatti ojan varrella
                apina['tila'] = 1                                   # Asetetaan apinan tilaksi 1 (valmiina kaivamaan)
                print("Apinan päivitetyt tiedot:", apina)           # Tulostetaan apinan päivitetyt tiedot
                break                                               # Lopetetaan silmukka, kun apina on löytynyt
        if apina_loytynyt:
            break

    if not apina_loytynyt:                 # Jos apinaa ei löydy metsästä
        print("Metsässä ei ole apinoita!") # Tulostetaan viesti

# Funktio, joka aloittaa apinan kaivamaan ojaa
def apina_kaivaa_kernestin_ojaa2():
    # Suodatetaan ne apinat, joiden tila on 1 eli valmiita kaivamaan
    apinat_ojalla = [apina['id'] for apina in apinoiden_tiedot if apina.get('tila') == 1 and apina.get('henkilo') == "Kernesti"] # Valitaan apinat, jotka ovat valmiina kaivamaan ja omistaja on Kernesti
    
    if apinat_ojalla:  # Varmistetaan, että on apinoita ojalla
        satunnainen_apina_id = random.choice(apinat_ojalla) # Valitaan satunnainen Kernestin apina, joka on valmiina kaivamaan
        print(f"Apina {satunnainen_apina_id} aloittaa kaivamisen.") # Tulostetaan viesti
        k_apina_kaivaa_ojaa(satunnainen_apina_id) # Kutsutaan funktiota, jolla aloitetaan kaivaminen
    else:
        print("Ei apinoita kaivamassa ojaa!") # Tulostetaan viesti, jos apinoita ei ole ojalla

# Funktio, joka poistaa apinat ojan varrelta
def poista_apinat_ojasta():
    for apina in apinoiden_tiedot:
        if apina.get('henkilo') == "Ernesti":
            autiosaari.delete(apina['kuva'])
            apina['henkilo'] = None
            apina['y_koordinaatti'] = None
            apina['y_koordinaatti_oja'] = None
            apina['tila'] = 0
        elif apina.get('henkilo') == "Kernesti":
            autiosaari.delete(apina['kuva'])
            apina['henkilo'] = None
            apina['y_koordinaatti'] = None
            apina['y_koordinaatti_oja'] = None
            apina['tila'] = 0
    print("Apinat poistettu ojan varrelta!")

# Luodaan painike, joka täyttää ojan uudelleen
tayta_oja_e = tk.Button(ikkuna, text="Täytä oja", command=lambda: tayta_oja(oja_ernesti), **painikkeiden_tyyli)
tayta_oja_e.place(x=100, y=250)

tayta_oja_k = tk.Button(ikkuna, text="Täytä oja", command=lambda: tayta_oja(oja_kernesti), **painikkeiden_tyyli)
tayta_oja_k.place(x=693, y=250)

# Luodaan painike, joka poistaa apinat ojan varrelta
poista_apinat = tk.Button(ikkuna, text="Poista apinat", command=lambda: poista_apinat_ojasta(), **painikkeiden_tyyli)
poista_apinat.place(x=400, y=250)

# Luo painike, joka käynnistää 10 apinan sijoittamisen töihin Ernestille
sijoita_apina_e = tk.Button(ikkuna, text="10 apinaa Ernestin töihin", command=lambda: threading.Thread(target=apinat_toihin, args=(oja_ernesti, 245, "Ernesti")).start(), **painikkeiden_tyyli)
sijoita_apina_e.place(x=100, y=300)

# Luo painike, joka käynnistää 10 apinan sijoittamisen töihin Kernestille
sijoita_apina_k = tk.Button(ikkuna, text="10 apinaa Kernestin töihin", command=lambda: threading.Thread(target=apinat_toihin, args=(oja_kernesti, 540, "Kernesti")).start(), **painikkeiden_tyyli)
sijoita_apina_k.place(x=693, y=300)

# Käynnistä ohjelma
ikkuna.mainloop()
import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import tkinter as tk
from tkinter import ttk
import time

from klasy import Rockman, Bramka, Bramka_plecak, Kolejka
from rozklad import przyjscia_w_czasie, T_max
#       DANE        #
Ile_bramek = 24 # musi byc parzysta mamy tyle samo bramek nie plecakowych ile plecakowych
max_ludzi = 5000

T_max = T_max
T_start_koncertu = 5/2 * 3600
T_delta = 1/2 * 3600
T_dodatkowy_czas = 1/2 * 3600


#--- co symulacje ---
czas_aktualny = 0
Ludzie_za_bramkami = 0
Ludzie_za_bramkami_w_chwili_t_start = 0
ludzie = []

Lista_czasow_czekania = []
Lista_czasow_czekania_w_chwili_t_start = []

bramki = []
bramki_plecakowe=[]

kolejki = []


# Funckja dla resetowania parametrow co interacje sumluacji zeby nie drukowac tych samych wynikow

def ustaw_parametry_na_start():
    global czas_aktualny
    global Ludzie_za_bramkami
    global Ludzie_za_bramkami_w_chwili_t_start
    global ludzie
    global Lista_czasow_czekania
    global Lista_czasow_czekania_w_chwili_t_start
    global bramki
    global bramki_plecakowe
    global kolejki

    czas_aktualny = 0
    Ludzie_za_bramkami = 0
    Ludzie_za_bramkami_w_chwili_t_start = 0
    ludzie = []

    Lista_czasow_czekania = []
    Lista_czasow_czekania_w_chwili_t_start = []

    bramki = []
    bramki_plecakowe = []

    kolejki = []


#rozklad plecakarzy jako uniform 0,10 i jesli >8 to ma plecak

# Parametry weibulla
lambda_val = 8
k_val = 10

#zmienna kontrolna
Nr_rockmana = 1

'''
'''


def stworz_bramki_kolejki():
    nr_kol =0
    for i in range(Ile_bramek // 2):
        kolejka = Kolejka(f'Kolejka_{nr_kol + 1}')
        nr_kol+=1
        kolejki.append(kolejka)

    for i in range(Ile_bramek // 2):
        kolejka = Kolejka(f'Kolejka(p){nr_kol + 1}')
        nr_kol+=1
        kolejki.append(kolejka)

    for i in range(Ile_bramek // 2):
        bramka = Bramka(f'Bramka_{i + 1}')
        bramki.append(bramka)
        kolejka = kolejki[i]
        bramka.Set_kolejka(kolejka)

    for i in range(Ile_bramek // 2):
        bramka_plecak = Bramka_plecak(f'Bramka_Plecak_{i + 1}')
        bramki_plecakowe.append(bramka_plecak)
        kolejka_plecakowa = kolejki[i + Ile_bramek // 2]
        bramka_plecak.Set_kolejka(kolejka_plecakowa)

def dodawanie_zgodne_z_czasem():
    global Nr_rockmana
    global czas_aktualny
    x = ludzie
    liczba_ludzi = x.count(czas_aktualny)
    j = 0
    while j < liczba_ludzi:
        Rozklad_plecakarzy = np.random.uniform(0, 10)

        if Rozklad_plecakarzy > 8:
            rockman_plecak = Rockman(f"Rockman_{Nr_rockmana}", plecak=True)
            wybrana_kolejka = wybierz_najkrotsza_kolejke_zwykla(kolejki)
            wybrana_kolejka.Dodaj_element(rockman_plecak)
        else:
            rockman = Rockman(f"Rockman_{Nr_rockmana}")
            wybrana_kolejka = wybierz_najkrotsza_kolejke_zwykla(kolejki)
            wybrana_kolejka.Dodaj_element(rockman)

        j += 1
        Nr_rockmana += 1

def rozgrzewanie_modelu():
    global czas_aktualny
    while czas_aktualny < T_delta:
        dodawanie_zgodne_z_czasem()
        czas_aktualny += 1
    for bramka in bramki:
        bramka.Set_czy_bramka_otwarta(True)
    for bramka in bramki_plecakowe:
        bramka.Set_czy_bramka_otwarta(True)
    #wyprintuj_ludzi_w_kolejkach() #jesli chcesz zobaczyc co jest po rozgrzaniu odhashuj
    return 0

def iteracja_bramka_zwykla(bramki):
    global Ludzie_za_bramkami
    for i in range(Ile_bramek // 2):
        # sprawdz czy otwarta
        if bramki[i].Get_czy_bramka_otwarta() == True:
            # otwarta wiec sprawdz czy kolejka istnieje
            if bramki[i].kolejka_bramki.Rozmiar() >= 1:
                # kolejka istnieje wiec sprawdz czy ma plecak
                if bramki[i].kolejka_bramki.Get_pierwszy().Get_czy_plecak() == True:
                    # ma plecak czyli dajemy go do kolejki plecakowej
                    rockman = bramki[i].kolejka_bramki.Get_pierwszy()
                    bramki_plecakowe[i].kolejka_bramki.Dodaj_element(rockman)
                    bramki[i].kolejka_bramki.Usun_rockmana()
                else:
                    # nie ma plecaka wiec zaczynamy sprawdzanie
                    bramki[i].Set_czy_bramka_otwarta(False)
                    bramki[i].Set_czas_sprawdzania(0)
                    bramki[i].Przypisz_osobe_do_bramki(bramki[i].kolejka_bramki.Get_pierwszy())
            else:
                # nie ma kolejki wiec idz dalej
                pass
        else:
            # zamknieta wiec sprawdzamy czy juz finish sprawdzania
            if (bramki[i].Get_czas_sprawdzania() == bramki[i].max_czas_sprawdzania):
                # tak to juz finish wiec uwalniamy rockmana i dodajemy 1 do ludzi za bramkami
                bramki[i].Set_czy_bramka_otwarta(True)
                Lista_czasow_czekania.append(bramki[i].kolejka_bramki.Get_pierwszy().Get_t_w_kolejce())
                Ludzie_za_bramkami += 1
                r = bramki[i].kolejka_bramki.Get_pierwszy()
                del r
                bramki[i].kolejka_bramki.Usun_rockmana()
            else:
                # to nie finish dodajemy czas sprawdzania
                bramki[i].Dodaj_czas_sprawdzania(1)

        for rockman in bramki[i].kolejka_bramki.kolejka:
            rockman.Dodaj_t_w_kolejce(1)

def iteracja_bramka_plecakowa(bramki_plecakowe):
    global Ludzie_za_bramkami
    for i in range(Ile_bramek // 2):
        # sprawdz czy bramka otwarta
        if bramki_plecakowe[i].Get_czy_bramka_otwarta() == True:
            # bramka otwarta, sprawdz czy jest ktos w kolejce
            if bramki_plecakowe[i].kolejka_bramki.Rozmiar() >= 1:
                # jest kolejka wiec zaczynamy sprawdzanie
                bramki_plecakowe[i].Set_czy_bramka_otwarta(False)
                bramki_plecakowe[i].Set_czas_sprawdzania(0)
                bramki_plecakowe[i].Przypisz_osobe_do_bramki(bramki_plecakowe[i].kolejka_bramki.Get_pierwszy())
            else:
                # nie ma kolejki wiec idz dalej
                pass
        else:
            # zamknieta wiec sprawdzamy czy juz finish sprawdzania
            if (bramki_plecakowe[i].Get_czas_sprawdzania() == bramki_plecakowe[i].max_czas_sprawdzania):
                # tak to juz finish wiec uwalniamy rockmana i dodajemy 1 do ludzi za bramkami
                bramki_plecakowe[i].Set_czy_bramka_otwarta(True)
                Lista_czasow_czekania.append(bramki_plecakowe[i].kolejka_bramki.Get_pierwszy().Get_t_w_kolejce())
                Ludzie_za_bramkami += 1
                r = bramki_plecakowe[i].kolejka_bramki.Get_pierwszy()
                del r
                bramki_plecakowe[i].kolejka_bramki.Usun_rockmana()
            else:
                # to nie finish dodajemy czas sprawdzania
                bramki_plecakowe[i].Dodaj_czas_sprawdzania(1)

        for rockman in bramki_plecakowe[i].kolejka_bramki.kolejka:
            rockman.Dodaj_t_w_kolejce(1)

def symulacja_glowna_czesc():
    global czas_aktualny
    global Lista_czasow_czekania_w_chwili_t_start
    global Ludzie_za_bramkami_w_chwili_t_start
    while czas_aktualny < T_max:

        #dodawanie jak wczesniej
        dodawanie_zgodne_z_czasem()

        # dla kazdej bramki nie plecakowej
        iteracja_bramka_zwykla(bramki)

        # dla kazdej bramki plecakowej
        iteracja_bramka_plecakowa(bramki_plecakowe)

        if (czas_aktualny == T_start_koncertu):
            Lista_czasow_czekania_w_chwili_t_start = Lista_czasow_czekania
            Ludzie_za_bramkami_w_chwili_t_start = Ludzie_za_bramkami

        czas_aktualny+=1


def wybierz_najkrotsza_kolejke_zwykla(kolejki):
    najkrotsza_kolejka = kolejki[0]
    for i in range(len(kolejki)//2):
        kolejka = kolejki[i]
        if kolejka.Rozmiar() < najkrotsza_kolejka.Rozmiar():
            najkrotsza_kolejka = kolejka
    return najkrotsza_kolejka

def wybierz_najkrotsza_kolejke_plecakowa(kolejki):
    najkrotsza_kolejka = kolejki[len(kolejki)//2]
    for i in range(len(kolejki)//2, len(kolejki)):
        kolejka = kolejki[i]
        if kolejka.Rozmiar() < najkrotsza_kolejka.Rozmiar():
            najkrotsza_kolejka = kolejka
    return najkrotsza_kolejka


def zrob_ludzi():
    global ludzie
    ludzie = przyjscia_w_czasie(max_ludzi)
    # Wyświetlenie wygenerowanych danych
    #print(ludzie)
    print(f'Jest: {len(ludzie)} ludzi')

def symulacja():
    ustaw_parametry_na_start()
    zrob_ludzi()
    stworz_bramki_kolejki()
    rozgrzewanie_modelu()
    symulacja_glowna_czesc()

# TESTY #
def test_bramek():
    for i in range(Ile_bramek // 2):
        kolejka_bramki = bramki[i].kolejka_bramki
        kolejka_bramki_plecakowej = bramki_plecakowe[i].kolejka_bramki
        print(f"{kolejka_bramki.imie if kolejka_bramki else 'brak kolejki'} przypisana do Bramki {i + 1}")
        print(f"{kolejka_bramki_plecakowej.imie if kolejka_bramki else 'brak kolejki'} przypisana do Bramki plecakowej {i + 1}")

def wyprintuj_ludzi_w_kolejkach():
    for i in range(Ile_bramek // 2):
        kolejka = bramki[i].kolejka_bramki
        kolejka_plecakowa = bramki_plecakowe[i].kolejka_bramki

        print(f"\nkole {i + 1}:\n")

        print("rockmani:")
        for j, rockman in enumerate(kolejka.kolejka):
            print(f"{rockman.imie}, Czy plecak: {rockman.Get_czy_plecak()}, Czas w kolejce: {rockman.Get_t_w_kolejce()}")
        print('\n')

        print("rockmani (plecaki):")
        for j, rockman in enumerate(kolejka_plecakowa.kolejka):
            print(
                f"{rockman.imie}, Czy plecak: {rockman.Get_czy_plecak()}, Czas w kolejce: {rockman.Get_t_w_kolejce()}")
        print('\n')

'''
window = tk.Tk()

text0 = ttk.Label(window, text="ile razy chcesz zasymulowac dla wybranych nizej parametrow? (polecam nie ogromna liczbe)")
text0.pack()

tk_Ile_symulacji = tk.IntVar(value = 1)
entry0 = ttk.Entry(window, textvariable=tk_Ile_symulacji)
entry0.pack()

text1 = ttk.Label(window, text="ustaw liczbe max_ludzi")
text1.pack()

tk_max_ludzi = tk.IntVar(value=5000)
entry1 = ttk.Entry(window, textvariable=tk_max_ludzi)
entry1.pack()

text2 = ttk.Label(window,text="ustaw liczbe bramek (bramki plecakowe + bramki nie plecakowe ) (CZYLI MUSI BYC PARZYSTA!!!) (Ile_bramek) ")
text2.pack()

tk_Ile_bramek = tk.IntVar(value=24)
entry2 = ttk.Entry(window, textvariable=tk_Ile_bramek)
entry2.pack()

text3 = ttk.Label(window, text="Jak długo model ma się rozgrzewać? (Delta_T) (Nie przekraczaj 9000 (bo to start koncertu))")
text3.pack()

tk_delta_t = tk.IntVar(value = int(1/2 * 3600))
entry3 = ttk.Entry(window, textvariable= tk_delta_t)
entry3.pack()
skala_delta_t = ttk.Scale(window, from_= 0, to= T_start_koncertu, variable= tk_delta_t )
skala_delta_t.pack()

'''

Ile_symulacji = 1
nr_sumulacji = [i+1 for i in range(125*Ile_symulacji)]
lista_ludzie_za_bramkami_t_start = []
lista_ludzie_za_bramkami_koniec = []
lista_srednia_czsow = []
lista_procenty = []
lista_ludzie = []
lista_bramki = []
lista_t = []

def Set_start():
    global Ile_symulacji
    global max_ludzi
    global Ile_bramek
    global T_delta

    lista_max_ludzi = [500, 10250, 20000]
    lista_ile_bramek = [10, 56, 100]
    litsa_T_delta = [1800, 3900, 6000]





    '''
    max_ludzi = tk_max_ludzi.get()
    Ile_bramek = tk_Ile_bramek.get()
    Ile_symulacji = tk_Ile_symulacji.get()
    T_delta = tk_delta_t.get()
    '''

    for i in range(Ile_symulacji):

        for x in range(3):
            max_ludzi = lista_max_ludzi[x]
            for y in range(3):
                Ile_bramek = lista_ile_bramek[y]
                for z in range(3):
                    T_delta = litsa_T_delta[z]

                    symulacja()

                    print("Jest:", Ile_bramek, "bramek")
                    print(f'Czas rozgrzewania modelu równy: {T_delta}\n')
                    print(f'liczba ludzi za bramkami na t_start_koncertu: {Ludzie_za_bramkami_w_chwili_t_start}\n')
                    #print(f'czasy czekania: {Lista_czasow_czekania_w_chwili_t_start}\n')

                    print(f'liczba ludzi za bramkami na koniec symulacji: {Ludzie_za_bramkami}\n')
                    #print(f'czasy czekania: {Lista_czasow_czekania}\n')

                    suma = 0
                    for i in range(len(Lista_czasow_czekania)):
                        suma += Lista_czasow_czekania[i]
                    srednia = suma / len(Lista_czasow_czekania)
                    srednia = round(srednia, 2)
                    print(f'średnia czasów czekania dla tego przebiegu symulacji: {srednia}')
                    procenty = round((Ludzie_za_bramkami_w_chwili_t_start / max_ludzi) * 100, 2)
                    print(f'{procenty}% ludzi weszło do t_start_koncertu\n')


                    lista_ludzie_za_bramkami_t_start.append(Ludzie_za_bramkami_w_chwili_t_start)
                    lista_ludzie_za_bramkami_koniec.append(Ludzie_za_bramkami)
                    lista_srednia_czsow.append(srednia)
                    lista_procenty.append(procenty)

                    lista_t.append(T_delta)
                    lista_ludzie.append(max_ludzi)
                    lista_bramki.append(Ile_bramek)


                    print('\n\n\n')


    return 0


def Set_start2():
    global Ile_symulacji
    global max_ludzi
    global Ile_bramek
    global T_delta

    start_time = time.time()

    lista_max_ludzi = [x for x in range(20000) if x % 2000 == 0]
    lista_max_ludzi = [500, 5375, 10250, 15125, 20000]
    lista_ile_bramek = [x for x in range(100) if x % 10 == 0]
    lista_ile_bramek = [10, 31, 56, 78, 100]
    litsa_T_delta = [x for x in range(6000) if x % 600 == 0]
    litsa_T_delta = [1800, 2850, 3900, 4950, 6000]



    '''
    max_ludzi = tk_max_ludzi.get()
    Ile_bramek = tk_Ile_bramek.get()
    Ile_symulacji = tk_Ile_symulacji.get()
    T_delta = tk_delta_t.get()
    '''

    for i in range(Ile_symulacji):

        for x in range(len(lista_max_ludzi)):
            max_ludzi = lista_max_ludzi[x]
            for y in range(len(lista_ile_bramek)):
                Ile_bramek = lista_ile_bramek[y]
                for z in range(len(litsa_T_delta)):
                    T_delta = litsa_T_delta[z]

                    symulacja()

                    print("Jest:", Ile_bramek, "bramek")
                    print(f'Czas rozgrzewania modelu równy: {T_delta}\n')
                    print(f'liczba ludzi za bramkami na t_start_koncertu: {Ludzie_za_bramkami_w_chwili_t_start}\n')
                    #print(f'czasy czekania: {Lista_czasow_czekania_w_chwili_t_start}\n')

                    print(f'liczba ludzi za bramkami na koniec symulacji: {Ludzie_za_bramkami}\n')
                    #print(f'czasy czekania: {Lista_czasow_czekania}\n')

                    suma = 0
                    for i in range(len(Lista_czasow_czekania)):
                        suma += Lista_czasow_czekania[i]
                    srednia = suma / len(Lista_czasow_czekania)
                    srednia = round(srednia, 2)
                    print(f'średnia czasów czekania dla tego przebiegu symulacji: {srednia}')
                    procenty = round((Ludzie_za_bramkami_w_chwili_t_start / max_ludzi) * 100, 2)
                    print(f'{procenty}% ludzi weszło do t_start_koncertu\n')


                    lista_ludzie_za_bramkami_t_start.append(Ludzie_za_bramkami_w_chwili_t_start)
                    lista_ludzie_za_bramkami_koniec.append(Ludzie_za_bramkami)
                    lista_srednia_czsow.append(srednia)
                    lista_procenty.append(procenty)

                    lista_t.append(T_delta)
                    lista_ludzie.append(max_ludzi)
                    lista_bramki.append(Ile_bramek)


                    print('\n\n\n')
    end_time = time.time()
    elapsed_time = end_time - start_time



    return 0

#Set_start()

Set_start2()
'''
guzik_start = ttk.Button(window, text="Symuluj!", command=Set_start)
guzik_start.pack()

window.mainloop()

'''
print(nr_sumulacji)

print(lista_ludzie_za_bramkami_t_start)
print(lista_ludzie_za_bramkami_koniec)
print(lista_srednia_czsow)
print(lista_procenty)

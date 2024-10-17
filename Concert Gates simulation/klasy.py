class Rockman:

    #standardowe wartosci
    def __init__(self, imie, plecak=False):
        self.czy_plecak = plecak
        self.t_w_kolejce = 0
        self.bramka = None
        self.imie = imie

    # basic info (potrzebuje do testow pozniej mozna wywalic)
    def __str__(self):
        return f"Czy plecak: {self.czy_plecak}, Czas w kolejce: {self.t_w_kolejce}"

    # przypisanie bramki
    def Set_bramka(self, bramka):
        self.bramka = bramka

    # usuwanie siebie samego z relacji z bramka
    def Usun_sie_z_bramki(self):
        if self.bramka:
            self.bramka.Usun_osobe_z_bramki(self)


    # pobieranie wartosci Czy_plecak
    def Get_czy_plecak(self):
        return(self.czy_plecak)

    #ustalanie wartosci Czy plecak MUSI BYC TRUE/FALSE
    #moim zdaniem ta funkcja jest nie potrzebna ale to tylko dla tego, że można to ustalić przy tworzeniu danej osoby
    def Set_czy_plecak(self,TF):
        if isinstance(TF, bool):
            self.czy_plecak = TF
        else:
            raise ValueError("TF to True/False, musi byc Boolem")

    #pobieranie wartosci ile juz stoi w kolejce
    def Get_t_w_kolejce(self):
        return(self.t_w_kolejce)

    # dodawanie 1 sekundy do czasu jak juz stoi w kolejce
    def Dodaj_t_w_kolejce(self,ile = 0):
        if isinstance(ile, int):
            self.t_w_kolejce += ile or 1
        else:
            raise ValueError("ile to int, musi byc liczba")

class Bramka():

    def __init__(self, imie, kolejka_bramki = None):
        self.czy_bramka_otwarta = False
        self.czas_sprawdzania = 0
        self.max_czas_sprawdzania = 10 # tutaj jeszcze do ustalenie (to jest constant ile sprawdzamy jedna bramke)
        self.osoba_sprawdzana = None
        self.kolejka_bramki = kolejka_bramki
        self.imie = imie

    # pobieranie infromacji czy bramka jest otwarta
    def Get_czy_bramka_otwarta(self):
        return(self.czy_bramka_otwarta)

    #ustalanie wartosci Czy bramka jest otwarta MUSI BYC TRUE/FALSE
    def Set_czy_bramka_otwarta(self,TF):
        if isinstance(TF, bool):
            self.czy_bramka_otwarta = TF
        else:
            raise ValueError("TF to True/False, musi byc Boolem")

    # pobieranie czasu sprawdzania
    def Get_czas_sprawdzania(self):
        return (self.czas_sprawdzania)

    # ustawianie czasu sprawdzania
    def Set_czas_sprawdzania(self, ile = 0):
        if isinstance(ile, int):
            self.czas_sprawdzania = ile or 0
        else:
            raise ValueError("ile to int, musi byc liczba")

    # dodawanie czasu sprawdzania, bazowa wartosc to 1 jednostka czasu (sekunda)
    def Dodaj_czas_sprawdzania(self, ile=1):
        if isinstance(ile, int):
            self.czas_sprawdzania += ile or 1
        else:
            raise ValueError("ile to int, musi byc liczba")

    # przypisywanie Rockmana ( osoby) do bramki
    def Przypisz_osobe_do_bramki(self, osoba):
        if isinstance(osoba, Rockman):
            self.osoba_sprawdzana = osoba
            osoba.Set_bramka(self)
        else:
            raise ValueError("nie przypisales Rockmana")
    # usuwanie osoby z bramki
    def Usun_osobe_z_bramki(self, osoba):
        if osoba == self.osoba_sprawdzana:
            self.osoba_sprawdzana = None

    # pobieranie osoby przypisanej
    def Get_przypisana_osoba(self):
        return(self.osoba_sprawdzana)

    # ustawianie swojej kolejki
    def Set_kolejka(self, kolejka):
        self.kolejka_bramki = kolejka

# klasa bramek dla plecakarzy
class Bramka_plecak(Bramka):
    def __init__(self,imie):
        super().__init__(imie=imie)
        self.max_czas_sprawdzania = 30  # tutaj jeszcze do ustalenie (to jest constant ile sprawdzamy jedna bramke)


#kolejka na zasadzie FIFO
class Kolejka():
    def __init__(self, imie, bramka_kolejki = None):
        self.kolejka = []
        self.bramka_kolejki = bramka_kolejki
        self.imie = imie

    def Dodaj_element(self, element):
        self.kolejka.append(element)

    def Get_element(self,nr = 0):
        return(self.kolejka[nr])

    def Usun_element(self):
        if not self.Czy_pusta():
            return self.kolejka.pop(0)
        else:
            print("Kolejka jest juz pusta")

    def Czy_pusta(self):
        return(len(self.kolejka) == 0)

    def Rozmiar(self):
        return(len(self.kolejka))

    # interakcja z usuwaniem rockmana
    def Usun_rockmana(self):
        rockman = self.Get_element(0)
        if rockman in self.kolejka:
            self.kolejka.remove(rockman)
            rockman.Usun_sie_z_bramki()

    # ustawianie swojej bramki
    def Set_kolejka(self, bramka):
        self.bramka_kolejki = bramka
    # wez pierwszy element kolejki
    def Get_pierwszy(self):
        return(self.kolejka[0])

#przyklad dzialania

'''
osoba1 = Rockman('os1',plecak=True)
print(osoba1.Get_t_w_kolejce())
osoba1.Dodaj_t_w_kolejce()
print(osoba1.Get_t_w_kolejce())
bramka2 = Bramka_plecak('br1')
bramka2.Przypisz_osobe_do_bramki(osoba1)
print(bramka2.Get_przypisana_osoba().Get_czy_plecak())
'''





#przyklad dodwania i usuwania osoby

'''
osoba1 = Rockman('osoba1')
osoba2 = Rockman('osoba2')
osoba3 = Rockman('osoba3',plecak=True)


q = Kolejka('kolejka1')
q.Dodaj_element(osoba1)
q.Dodaj_element(osoba2)

for e in range(q.Rozmiar()):
    print(q.Get_element(e))
print('\n')

b1 = Bramka('bramka1')

b1.Przypisz_osobe_do_bramki(q.Get_element(0))
print(b1.Get_przypisana_osoba(),'1')
q.Usun_rockmana()
del osoba1
print(b1.Get_przypisana_osoba(),'2')
print(osoba1.Get_czy_plecak()) # osoba1 zostala usunieta (tak ma byc)
'''

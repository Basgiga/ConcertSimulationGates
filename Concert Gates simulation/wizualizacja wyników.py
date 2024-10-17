

from MainPetlaB import (lista_srednia_czsow, lista_procenty,
                        lista_ludzie_za_bramkami_t_start,
                        lista_ludzie_za_bramkami_koniec, nr_sumulacji,
                        lista_bramki, lista_ludzie, lista_t)


# Ustal maksymalną długość obu list
max_dlugosc = max(len(lista_ludzie_za_bramkami_koniec), len(lista_ludzie_za_bramkami_t_start), len(lista_srednia_czsow))


# Utwórz nową listę, w której obie listy zostaną złączone w taki sposób, aby były pod sobą
zlaczone_listy = [(f"{nr_sumulacji[i]:<5} {lista_ludzie[i]:<7}  {lista_bramki[i]:<7} {lista_t[i]:<7} "
                    f"{lista_ludzie_za_bramkami_t_start[i]:<7} {lista_ludzie_za_bramkami_koniec[i]:<7} {lista_srednia_czsow[i]:<7} {lista_procenty[i]:<7}%") for i in range(max_dlugosc)]

# Wydrukuj złączoną listę
for element in zlaczone_listy:
    print(element)






#-------------------------------------------
#wykres 3d
def wykres_3D():
    import matplotlib.pyplot as plt


    # Przykładowe dane
    x = lista_ludzie
    y = lista_bramki
    z = lista_procenty

    # Tworzenie wykresu punktowego 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, c='blue', marker='o')

    # Ustawienia osi i etykiet
    ax.set_xlabel('Il ludzi jaka miała przyjść na koncert')
    ax.set_ylabel('Il otwrtych bramek')
    ax.set_zlabel('Il procent ludzi jakim udałó się wejść przed startem koncertu')
    ax.set_title('Wykres punktowy 3D')

    # Wyświetlanie wykresu
    plt.show()


#-------------------------------------------


#wykresy połączone
def wykres_p_start():
    import matplotlib.pyplot as plt
    import numpy as np

    piecsetki = [[],[],[]]
    dziesiectysiecy = [[],[],[]]
    dwadziescia = [[],[],[]]

    for i in range(len(lista_ludzie)):
        if lista_ludzie[i] == 500 and lista_bramki[i] == 10:
            piecsetki[0].append(lista_procenty[i])
        elif lista_ludzie[i] == 500 and lista_bramki[i] == 56:
            piecsetki[1].append(lista_procenty[i])
        elif lista_ludzie[i] == 500 and lista_bramki[i] == 100:
            piecsetki[2].append(lista_procenty[i])
        elif lista_ludzie[i] == 10250 and lista_bramki[i] == 10:
            dziesiectysiecy[0].append(lista_procenty[i])
        elif lista_ludzie[i] == 10250 and lista_bramki[i] == 56:
            dziesiectysiecy[1].append(lista_procenty[i])
        elif lista_ludzie[i] == 10250 and lista_bramki[i] == 100:
            dziesiectysiecy[2].append(lista_procenty[i])
        elif lista_ludzie[i] == 20000 and lista_bramki[i] == 10:
            dwadziescia[0].append(lista_procenty[i])
        elif lista_ludzie[i] == 20000 and lista_bramki[i] == 56:
            dwadziescia[1].append(lista_procenty[i])
        elif lista_ludzie[i] == 20000 and lista_bramki[i] == 100:
            dwadziescia[2].append(lista_procenty[i])


    # Ustawienia rozmiaru i podziału obszaru dla trzech wykresów obok siebie
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))


    # Wykres 1
    axs[0].boxplot(piecsetki, labels=['10', '56', '100'])
    axs[0].set_title('il. ludzi = 500')
    axs[0].set_ylim([0, 100])


    # Wykres 2
    axs[1].boxplot(dziesiectysiecy, labels=['10', '56', '100'])
    axs[1].set_title('il. ludzi = 10250')
    axs[0].set_ylim([0, 100])

    # Wykres 3
    axs[2].boxplot(dwadziescia, labels=['10', '56', '100'])
    axs[2].set_title('il. ludzi = 20000')
    axs[0].set_ylim([0, 100])

    fig.text(0.04, 0.5, 'Procentowa ilość ludzi którym udało się wejść do startu koncertu [%]', va='center', rotation='vertical')

    # Uniwersalna etykieta dla osi x
    fig.text(0.5, 0.02, 'Ilości otwartych bramek', ha='center')

    # Dostosowanie układu i wyświetlanie wykresów
    plt.tight_layout()
    plt.show()



#-------------------------------------
def wykres_p_il_bramek():

    import matplotlib.pyplot as plt
    import numpy as np

    import matplotlib.pyplot as plt
    import numpy as np

    x = [[], [], []]
    y = [[], [], []]
    z = [[], [], []]
    #gdzie x, y, z oznaczaja kolejno 10, 54, 100

    for i in range(len(lista_ludzie)):
        if lista_ludzie[i] == 500 and lista_t[i] == 1800:
            x[0].append(lista_procenty[i])
        elif lista_ludzie[i] == 500 and lista_t[i] == 3900:
            x[1].append(lista_procenty[i])
        elif lista_ludzie[i] == 500 and lista_t[i] == 6000:
            x[2].append(lista_procenty[i])
        elif lista_ludzie[i] == 10250 and lista_t[i] == 1800:
            y[0].append(lista_procenty[i])
        elif lista_ludzie[i] == 10250 and lista_t[i] == 3900:
            y[1].append(lista_procenty[i])
        elif lista_ludzie[i] == 10250 and lista_t[i] == 6000:
            y[2].append(lista_procenty[i])
        elif lista_ludzie[i] == 20000 and lista_t[i] == 1800:
            z[0].append(lista_procenty[i])
        elif lista_ludzie[i] == 20000 and lista_t[i] == 3900:
            z[1].append(lista_procenty[i])
        elif lista_ludzie[i] == 20000 and lista_t[i] == 6000:
            z[2].append(lista_procenty[i])

    # Ustawienia rozmiaru i podziału obszaru dla trzech wykresów obok siebie
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    # Wykres 1
    axs[0].boxplot(x, labels=['1800', '3900', '6000'])
    axs[0].set_title('il. ludzi = 500')
    axs[0].set_ylim([0, 100])

    # Wykres 2
    axs[1].boxplot(y, labels=['1800', '3900', '6000'])
    axs[1].set_title('il. ludzi = 10250')
    axs[0].set_ylim([0, 100])

    # Wykres 3
    axs[2].boxplot(z, labels=['1800', '3900', '6000'])
    axs[2].set_title('il. ludzi = 20000')
    axs[0].set_ylim([0, 100])

    fig.text(0.04, 0.5, 'Procentowa ilość ludzi którym udało się wejść do startu koncertu [%]', va='center',
             rotation='vertical')

    # Uniwersalna etykieta dla osi x
    fig.text(0.5, 0.02, 'Czasy startu koncertu od rozpoczęcia symulacji', ha='center')

    # Dostosowanie układu i wyświetlanie wykresów
    plt.tight_layout()
    plt.show()

#-----------------------------------------------------------------------------------

def wykres_p_il_ludzi():

    import matplotlib.pyplot as plt
    import numpy as np

    import matplotlib.pyplot as plt
    import numpy as np

    x = [[], [], []]
    y = [[], [], []]
    z = [[], [], []]
    #gdzie x, y, z oznaczaja kolejno 10, 54, 100

    for i in range(len(lista_ludzie)):
        if lista_bramki[i] == 10 and lista_t[i] == 1800:
            x[0].append(lista_procenty[i])
        elif lista_bramki[i] == 10 and lista_t[i] == 3900:
            x[1].append(lista_procenty[i])
        elif lista_bramki[i] == 10 and lista_t[i] == 6000:
            x[2].append(lista_procenty[i])
        elif lista_bramki[i] == 56 and lista_t[i] == 1800:
            y[0].append(lista_procenty[i])
        elif lista_bramki[i] == 56 and lista_t[i] == 3900:
            y[1].append(lista_procenty[i])
        elif lista_bramki[i] == 56 and lista_t[i] == 6000:
            y[2].append(lista_procenty[i])
        elif lista_bramki[i] == 100 and lista_t[i] == 1800:
            z[0].append(lista_procenty[i])
        elif lista_bramki[i] == 100 and lista_t[i] == 3900:
            z[1].append(lista_procenty[i])
        elif lista_bramki[i] == 100 and lista_t[i] == 6000:
            z[2].append(lista_procenty[i])

    # Ustawienia rozmiaru i podziału obszaru dla trzech wykresów obok siebie
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    # Wykres 1
    axs[0].boxplot(x, labels=['1800', '3900', '6000'])
    axs[0].set_title('il. bramek = 10')
    axs[0].set_ylim([0, 100])

    # Wykres 2
    axs[1].boxplot(y, labels=['1800', '3900', '6000'])
    axs[1].set_title('il. bramek = 56')
    axs[0].set_ylim([0, 100])

    # Wykres 3
    axs[2].boxplot(z, labels=['1800', '3900', '6000'])
    axs[2].set_title('il. bramk = 100')
    axs[0].set_ylim([0, 100])

    fig.text(0.04, 0.5, 'Procentowa ilość ludzi którym udało się wejść do startu koncertu [%]', va='center',
             rotation='vertical')

    # Uniwersalna etykieta dla osi x
    fig.text(0.5, 0.02, 'Czasy startu koncertu od rozpoczęcia symulacji', ha='center')

    # Dostosowanie układu i wyświetlanie wykresów
    plt.tight_layout()
    plt.show()

wykres_p_il_ludzi()

#---------------------------------------------
def trzy_wykreesy_po_kolei_stałe():
    import matplotlib.pyplot as plt

    fig, axs = plt.subplots(1, 3, figsize=(15, 5))

    #zmienne czasy otwarć
    x_vals = []
    y_vals = []
    for i in range(len(lista_t)):
        if lista_ludzie[i] == 20000 and lista_bramki[i] == 56:
            x_vals.append(lista_t[i])
            y_vals.append(lista_procenty[i])
    axs[0].scatter(x_vals, y_vals, color='green', label='wartości dla il.ludzi = 20000 i il.bramek = 56')
    axs[0].set_xlabel('Czasy otwarcia bramek')
    axs[0].set_ylim([0, 100])


    #zmienne liczby bramek
    x_vals = [lista_bramki[i] for i in range(len(lista_t)) if lista_ludzie[i] == 20000 and lista_t[i] == 3900]
    y_vals = [lista_procenty[i] for i in range(len(lista_procenty)) if lista_ludzie[i] == 20000 and lista_t[i] == 3900]
    axs[1].scatter(x_vals, y_vals, color='red', label='wartości dla il.ludzi = 20000 i czasu otwarcia koncertu = 3900')
    axs[1].set_xlabel('Dostępne bramki')
    axs[1].set_ylim([0, 100])

    # zmienne liczby ludzi
    x_vals = [lista_ludzie[i] for i in range(len(lista_t)) if lista_bramki[i] == 56 and lista_t[i] == 3900]
    y_vals = [lista_procenty[i] for i in range(len(lista_procenty)) if lista_bramki[i] == 56 and lista_t[i] == 3900]
    axs[2].scatter(x_vals, y_vals, label='wartości dla il.ludzi = 20000 i czasu otwarcia koncertu = 3900')
    axs[2].set_xlabel('Ilości ludzi')
    axs[2].set_ylim([0, 100])

    fig.text(0.02, 0.98, '[%] Oś Y opisuje procentową ilość ludzi którym udało się wejść do startu koncertu. Dla każdego wykresu mamy ustawione stałe parametry równe il.ludzi = 20000, czas otwarcia bramek = 3900, il. bramek = 56.', va='center',)
    fig.text(0.05, 0.02,'Zmienia się tylko to co opisane na dole', va='center')
    # Dostosowanie układu i wyświetlanie wykresów
    #axs[0].legend()
    #axs[1].legend()
    #axs[2].legend()
    plt.tight_layout()
    plt.show()




#---------------------------------------------
trzy_wykreesy_po_kolei_stałe()








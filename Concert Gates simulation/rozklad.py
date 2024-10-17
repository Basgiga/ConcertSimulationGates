import random
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
# rozkładu Weibulla
def weibull_pdf(x, l_p, k_p):
    if x < 0:
        return 0
    else:
        return (k_p / l_p) * (x / l_p)**(k_p - 1) * np.exp(-(x / l_p)**k_p) + 0.001

# Parametry weibulla
lambda_val = 8
k_val = 10
max_ludzi = 5000
T_max = 3 * 3600

# funkcja dla PDF'a i rysowanie jego
def ostat():
    ilosc = 15000
    lambda_vals = 10
    k_vals = 6
    tablica = []
    # Generowanie wartości PDF rozkładu Weibulla i zapisywanie ich w tablicy
    for i in range(ilosc):
        x = i / 1000
        result = weibull_pdf(x, lambda_vals, k_vals)
        tablica.append(result)

    x_vals = np.linspace(0, ilosc, ilosc)
    plt.plot(x_vals, tablica, label=f'Weibull PDF: λ={lambda_vals}, k={k_vals}')
    plt.legend()
    plt.show()

# rysowanie PDFa
#ostat()

# Generowanie losowych danych
def generowanie_ludzi(max_ludzi):
    ludzie = []
    while len(ludzie) != max_ludzi:
        x = random.randint(0, 15000)
        x = x/1000
        y = random.random()/4
        lambda_vals = 10
        k_vals = 6
        if y <= ((k_vals / lambda_vals) * (x / lambda_vals)**(k_vals - 1) * np.exp(-(x / lambda_vals)**k_vals) + 0.001):
            ludzie.append(x)
    return(ludzie)

# Wyświetlenie wygenerowanych danych
#print(ludzie)

# estymacja gestosci
def gestosc_ludzi(x):
    kde = stats.gaussian_kde(x)
    x_vals = np.linspace(min(x), max(x), 1000)
    y_vals = kde(x_vals)

    # Rysowanie estymacji gęstości jądrowej
    plt.plot(x_vals, y_vals, label='Estymator Gęstości Jądrowej')
    plt.scatter(x, np.zeros_like(x), color='red', marker='.', label='Punkty Estymatora')
    plt.fill_between(x_vals, y_vals, alpha=0.2)
    plt.xlabel('waga')
    plt.ylabel('Estymowana Gęstość')
    plt.title('Estymator Gęstości Jądrowej wagi danej płci')
    plt.show()

#gestosc_ludzi(ludzie)


#generowanie przychodzenia w czasie
#to zanczy, że tutaj jest to już podzieliłem odpowiednio. Tylko, że bez wizualizacji
def przyjscia_w_czasie(max_ludzi):
    ludzie = generowanie_ludzi(max_ludzi)
    parametr = T_max/max(ludzie)
    for x in range(len(ludzie)):
        ludzie[x] = ludzie[x] * parametr
        ludzie[x] = round(ludzie[x])

    return ludzie

#print('nobas')
#ludzie_2 = przyjscia_w_czasie(max_ludzi)

#wizualizacja gestosc_vs_czas
def wizaulizacja_w_czasie():
    x = przyjscia_w_czasie(max_ludzi)
    kde = stats.gaussian_kde(x)

    x_vals = np.linspace(min(x), max(x), 1000)
    y_vals = kde(x_vals)

    plt.axvline(x=9000, color='green', linestyle=':', label='Początek koncertu')
    plt.plot(x_vals, y_vals, label='Estymator Gęstości Jądrowej')
    plt.scatter(x, np.zeros_like(x), color='red', marker='.', label='Ludzie')
    plt.fill_between(x_vals, y_vals, alpha=0.2)  # Wypełnij obszar pod krzywą

    plt.legend(loc='upper right')
    plt.xlabel('Czas')
    plt.ylabel('Estymowana Gęstość ludzi')
    plt.title('Estymator Gęstości przychodzenia ludzi w czasie')

    plt.show()
#wizaulizacja_w_czasie()

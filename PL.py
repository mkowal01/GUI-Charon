import math

# Dane
f_mhz = 868  # Częstotliwość w MHz
d_km = 1  # Odległość w kilometrach
h_t = 1  # Wysokość anteny nadawczej (m)
h_r = 1 # Wysokość anteny odbiorczej (m)

# Funkcja dla korekcji a(h_r) w środowisku miejskim
def a_hr_urban(h_r):
    return 3.2 * (math.log10(11.75 * h_r))**2 - 4.97

a_hr = a_hr_urban(h_r)  # Korekcja a(h_r) dla miast

# PL dla miast (teren miejski)
PL_urban_test = (
    69.55 +
    26.16 * math.log10(f_mhz) -
    13.82 * math.log10(h_t) -
    a_hr +
    (44.9 - 6.55 * math.log10(h_t)) * math.log10(d_km)
)

# PL dla terenów podmiejskich
PL_suburban_test = PL_urban_test - 2 * (math.log10(f_mhz / 28))**2 - 5.4

# PL dla terenów wiejskich
PL_rural_test = PL_urban_test - 4.78 * (math.log10(f_mhz))**2 + 18.33 * math.log10(f_mhz) - 40.94

# Wynik
print(PL_urban_test, PL_suburban_test, PL_rural_test)

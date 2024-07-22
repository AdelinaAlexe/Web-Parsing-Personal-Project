Abordarea mea pentru aceasta solutie este sa folosesc metoda de "web scraping".
Am folosit o biblioteca care imi permite accesul catre datele din fisierul sursa.
Am extras adresele web intr-un tabel, iar pentru fiecare in parte am verificat daca este o adresa valida sau nu.
In cazul in care adresa este valida, apelez functia "find_address", care cauta in toate paginile website-ului o
adresa de Google Maps. Catre aceasta adresa este trimisa o cerere pentru a obtine un url din care extrag coordonatele
locatiei. Folosind aceste coordonate si o cheie API generata, accesez codul html al paginii adresei fizice pe care o caut.
Adresa o voi extrage de la linia ce incepe cu "formatted_address" si o prelucrez pentru a o aduce la forma finala.
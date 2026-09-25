# Predykcja-decyzji-kredytowej-analiza-por-wnawcza-modeli-ML

Projekt zaliczeniowy z przedmiotu **Podstawy Sztucznej Inteligencji** (Uniwersytet Ekonomiczny w Katowicach, kierunek Analityka Finansowa 2.0).

Autor: Emilia Walczak

## Opis projektu

Celem projektu jest opracowanie i porównanie skuteczności czterech modeli uczenia maszynowego (Drzewo Decyzyjne, Random Forest, Regresja Logistyczna, Sieć Neuronowa) w klasyfikacji wniosków kredytowych na podstawie zbioru danych **Loan Prediction Problem Dataset** (Kaggle, 614 wniosków, 13 atrybutów).

Projekt wykorzystuje podejście hybrydowe:
- **Python (Pandas, Seaborn, Matplotlib)** – wstępny audyt danych: identyfikacja braków, detekcja wartości odstających metodą IQR, macierz korelacji.
- **Orange Data Mining** – czyszczenie i transformacja danych, budowa i ewaluacja modeli uczenia maszynowego (opis pełnego pipeline'u poniżej).

## Workflow uczenia maszynowego w Orange (`model_kredytowy.ows`)

Plik `.ows` to zapis wizualnego pipeline'u Orange – każdy "widget" to blok przetwarzania danych lub model, połączony strzałkami z kolejnymi krokami. Pipeline w tym projekcie przebiega następująco:

**1. Wczytanie i przygotowanie danych**
- `File` → wczytuje zbiór Loan Prediction Dataset.
- `Select Columns` → wybór zmiennych do analizy, odrzucenie identyfikatora `Loan_ID`.
- `Edit Domain` → korekta typów zmiennych (np. `Credit_History` ręcznie zmieniona z liczby na zmienną kategoryczną).
- `Impute` → uzupełnienie braków danych: średnią dla zmiennych numerycznych, wartością najczęstszą (modą) dla kategorycznych. To centralny węzeł – zasila niemal wszystkie kolejne widgety.

**2. Eksploracja i diagnostyka danych**
- `Outliers` → automatyczne wykrywanie wartości odstających (uzupełnia analizę z Pythona).
- `Box Plot` i `Distributions` → wizualizacja rozkładów zmiennych i potwierdzenie obecności outlierów w obu klasach decyzyjnych (Y/N).
- `Scatter Plot` → wykres punktowy dochód–kwota kredytu, obarwiony statusem decyzji i wykształceniem; pokazuje m.in. przypadek klienta o dochodzie 81 000, któremu mimo to odmówiono kredytu.
- `Rank` → ranking zmiennych wg mocy predykcyjnej (Information Gain, Gini Decrease) – wskazuje `Credit_History` jako najważniejszą cechę.
- `Mosaic Display` → wizualizacja zależności między zmiennymi kategorycznymi a decyzją kredytową.

**3. Budowa modeli klasyfikacyjnych**
Dane (po `Data Sampler` i, dla sieci neuronowej i lasu losowego, dodatkowym `Preprocess` – normalizacji) trafiają równolegle do czterech algorytmów:
- `Tree` (Drzewo Decyzyjne) – model bazowy, wysoka interpretowalność.
- `Random Forest` (Las Losowy) – model zespołowy, odporny na outliery i braki danych.
- `Logistic Regression` (Regresja Logistyczna) – model liniowy, punkt odniesienia.
- `Neural Network` (Sieć Neuronowa) – model nieliniowy typu "czarna skrzynka".
- dodatkowo `SVM` trenowany na danych oczyszczonych z outlierów.

**4. Ewaluacja modeli**
- `Test and Score` → walidacja krzyżowa (10-krotna, k=10), obliczanie metryk AUC, CA (accuracy), Precision dla każdego modelu.
- `ROC Analysis` → krzywe ROC porównujące modele.
- `Tree Viewer` → wizualizacja struktury wytrenowanego drzewa decyzyjnego (pokazuje, że `Credit_History` jest węzłem korzenia).
- `Nomogram` → graficzne przedstawienie wag regresji logistycznej – ile "punktów" dodaje każda wartość każdej zmiennej do szansy na przyznanie kredytu.

### Wyniki ewaluacji modeli

| Model | AUC | CA (dokładność) | Precision | Wniosek |
|---|---|---|---|---|
| **Random Forest** | 0,756 | 0,806 | 0,829 | Najlepszy model – dobrze radzi sobie z nieliniowością i outlierami |
| Logistic Regression | 0,754 | 0,804 | 0,822 | Wysoki wynik dzięki silnej liniowej korelacji dochodu z kwotą kredytu |
| Neural Network | 0,739 | 0,791 | 0,791 | Wynik dobry, ale wymagał silniejszej normalizacji danych |
| Tree | 0,671 | 0,708 | 0,711 | Najsłabszy wynik spośród testowanych modeli |

### Główne wnioski

- **Credit_History** to najsilniejszy predyktor decyzji kredytowej (korelacja 0,56 z Loan_Status).
- Sam poziom dochodu wnioskodawcy praktycznie nie koreluje liniowo z decyzją (dochód i decyzja mają charakter nieliniowy), co tłumaczy przewagę modeli nieliniowych (Random Forest) nad regresją liniową.
- Cechy demograficzne (wykształcenie, stan cywilny, samozatrudnienie) mają marginalny wpływ na decyzję.

## Struktura repozytorium

```
├── Analiza/
│   ├── raport.analiza.py                              # skrypt Python – audyt danych, outliery, macierz korelacji
│   ├── raport_output.txt                               # wynik działania skryptu (braki danych, outliery)
│   ├── correlation_matrix.png                           # wygenerowana macierz korelacji (heatmapa)
│   └── outliers_applicant_income.csv                    # lista wykrytych outlierów (eksport z pliku xlsx)
├── Loan Prediction Dataset.xlsx                         # zbiór danych źródłowych (Kaggle)
├── Raport_koncowy_Emilia_Walczak.pdf                     # pełny raport końcowy z opisem metodologii i wyników
├── model_kredytowy.ows                                   # workflow Orange Data Mining (modele + ewaluacja)
└── README.md
```

## Wymagania (dla skryptu Python)

```
pandas
seaborn
matplotlib
openpyxl
```

## Jak uruchomić

1. Otwórz `Analiza/raport.analiza.py` i zaktualizuj ścieżkę do pliku `Loan Prediction Dataset.xlsx`.
2. Uruchom skrypt – wygeneruje `raport_output.txt`, `outliers_applicant_income.csv` oraz `correlation_matrix.png`.
3. Plik `model_kredytowy.ows` otwórz w [Orange Data Mining](https://orangedatamining.com/), aby zobaczyć pełny workflow modelowania (imputacja, selekcja cech, drzewa decyzyjne, Random Forest, regresja logistyczna, sieć neuronowa oraz ewaluacja AUC).

## Źródło danych

[Loan Prediction Problem Dataset – Kaggle](https://www.kaggle.com/datasets/ninzaami/loan-predication)

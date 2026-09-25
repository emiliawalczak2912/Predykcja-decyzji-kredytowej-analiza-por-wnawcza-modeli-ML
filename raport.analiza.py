import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

# Wczytanie pliku Excel (używamy pełnej ścieżki i sprawdzamy dostępność)
file_name = r'C:\Users\emiw2\OneDrive\Pulpit\Analiza\LOAN PREDICTION DATA.xlsx'
sheet = 'Loan Prediction Problem Dataset'

if not os.path.exists(file_name):
	folder = os.path.dirname(file_name)
	print(f"Plik nie znaleziony pod ścieżką: {file_name}")
	print(f"Sprawdzam zawartość folderu: {folder}\n")
	try:
		for f in os.listdir(folder):
			print(f)
	except Exception as e:
		print(f"Nie udało się odczytać folderu: {e}")
	raise SystemExit("Proszę upewnić się, że plik Excel istnieje i ma poprawną nazwę (razem z rozszerzeniem).")

df = pd.read_excel(file_name, sheet_name=sheet)

# Identyfikacja braków
print("--- LICZBA BRAKÓW W KOLUMNACH ---")
missing = df.isnull().sum()
print(missing[missing > 0]) # Wyświetla tylko kolumny z brakami

# Wyświetlenie konkretnych rekordów z brakami w LoanAmount (np. LP001002)
print("\n--- PRZYKŁADOWE REKORDY Z BRAKAMI (NaN) ---")
print(df[df['LoanAmount'].isnull()][['Loan_ID', 'ApplicantIncome', 'LoanAmount']].head())

# Obliczanie kwartyli
Q1 = df['ApplicantIncome'].quantile(0.25)
Q3 = df['ApplicantIncome'].quantile(0.75)
IQR = Q3 - Q1

# Definiowanie granic
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

# Wyświetlenie rekordów będących outlierami
outliers = df[df['ApplicantIncome'] > upper_bound]

print(f"Granica górna: {upper_bound}")
print(f"Liczba zidentyfikowanych outlierów: {len(outliers)}")
print(df[['Loan_ID', 'ApplicantIncome']].sort_values(by='ApplicantIncome', ascending=False).head())

# Zapis wyników do plików (łatwiejsze podglądanie w VS Code)
output_folder = os.path.dirname(file_name)
txt_path = os.path.join(output_folder, 'raport_output.txt')
outliers_csv = os.path.join(output_folder, 'outliers_applicant_income.csv')

# Zapis wyników do plików (obsługa błędów dostępu)
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
try:
	with open(txt_path, 'w', encoding='utf-8') as f:
		f.write('--- LICZBA BRAKÓW W KOLUMNACH ---\n')
		f.write(missing[missing > 0].to_string())
		f.write('\n\n--- PRZYKŁADOWE REKORDY Z BRAKAMI (NaN) ---\n')
		f.write(df[df['LoanAmount'].isnull()][['Loan_ID', 'ApplicantIncome', 'LoanAmount']].head().to_string())
		f.write('\n\n--- OUTLIERY ApplicantIncome ---\n')
		f.write(f'Granica górna: {upper_bound}\n')
		f.write(f'Liczba zidentyfikowanych outlierów: {len(outliers)}\n')
		f.write(df[['Loan_ID', 'ApplicantIncome']].sort_values(by='ApplicantIncome', ascending=False).head().to_string())
	try:
		outliers.to_csv(outliers_csv, index=False)
		print(f"Wyniki zapisane do: {txt_path}")
		print(f"Outliery zapisane do: {outliers_csv}")
	except PermissionError:
		# fallback: zapis z timestampem
		alt_csv = os.path.join(output_folder, f'outliers_applicant_income_{timestamp}.csv')
		outliers.to_csv(alt_csv, index=False)
		print(f"Nie można zapisać do {outliers_csv} (brak uprawnień). Zapisano do: {alt_csv}")
except PermissionError:
	alt_txt = os.path.join(output_folder, f'raport_output_{timestamp}.txt')
	try:
		with open(alt_txt, 'w', encoding='utf-8') as f:
			f.write('--- LICZBA BRAKÓW W KOLUMNACH ---\n')
			f.write(missing[missing > 0].to_string())
			f.write('\n\n--- PRZYKŁADOWE REKORDY Z BRAKAMI (NaN) ---\n')
			f.write(df[df['LoanAmount'].isnull()][['Loan_ID', 'ApplicantIncome', 'LoanAmount']].head().to_string())
			f.write('\n\n--- OUTLIERY ApplicantIncome ---\n')
			f.write(f'Granica górna: {upper_bound}\n')
			f.write(f'Liczba zidentyfikowanych outlierów: {len(outliers)}\n')
			f.write(df[['Loan_ID', 'ApplicantIncome']].sort_values(by='ApplicantIncome', ascending=False).head().to_string())
		alt_csv = os.path.join(output_folder, f'outliers_applicant_income_{timestamp}.csv')
		outliers.to_csv(alt_csv, index=False)
		print(f"Brak uprawnień do zapisu do domyślnych plików. Wyniki zapisane do: {alt_txt} i {alt_csv}")
	except Exception as e:
		print(f"Nie udało się zapisać wyników: {e}")
		print("Upewnij się, że pliki nie są otwarte w Excelu i spróbuj ponownie.")

# 6. Macierz korelacji zmiennych numerycznych (heatmap)
# Konwersja Loan_Status na wartości numeryczne dla korelacji
if 'Loan_Status' in df.columns:
	df['Loan_Status_Num'] = df['Loan_Status'].map({'Y': 1, 'N': 0})

numeric_cols = df.select_dtypes(include=['number'])
corr_matrix = numeric_cols.corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title("Macierz korelacji zmiennych")
plt.tight_layout()

# Zapis wykresu do pliku, żeby można go łatwo podejrzeć
corr_img = os.path.join(output_folder, 'correlation_matrix.png')
plt.savefig(corr_img)
plt.close()
print(f"Macierz korelacji zapisana do: {corr_img}")
import csv

# Onde ficarão funções auxiliares que poderão ser reutilizadas futuramente.

def ler_csv (csv_file:str)->list:
    try:
        with open(csv_file,"r",newline="",encoding="utf-8") as arquivo:
            leitor= csv.DictReader(arquivo)
            animais = list(leitor)

        return animais
    except FileNotFoundError:
        return []
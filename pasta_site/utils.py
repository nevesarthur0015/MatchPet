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
    

# Cria um diretório dentro de "imagens/", cujo nome é o id de um pet, ao adicioná-lo para doação. Contém as imagens do pet.
def upload_img(pet_id)
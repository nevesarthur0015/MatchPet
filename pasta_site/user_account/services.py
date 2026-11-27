import os
import csv
from pathlib import Path

CSV_PATH = Path("data/pets.csv")
fieldnames = ['nome', 'idade', 'sexo', 'raca', 'mensagem', 'id_pet', 'user_id', 'tipo', 'imagens']

def salvar_alteracao(pets):
    with CSV_PATH.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(pets)
        
def deletar_arquivos(id_pet):
    pasta_imagens = os.path.join("pasta_site", "static", "imagens", str(id_pet))
    
    if not os.path.exists(pasta_imagens):
        return
    
    for arquivo in os.listdir(pasta_imagens):
        arq = os.path.join(pasta_imagens, arquivo)
        os.remove(arq)
        
    
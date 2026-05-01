import os
import re
import pdfplumber
import shutil

# Configurações de pastas
PASTA_ENTRADA = './entrada'
PASTA_SAIDA = './saida'

# Cria as pastas se não existirem
os.makedirs(PASTA_ENTRADA, exist_ok=True)
os.makedirs(PASTA_SAIDA, exist_ok=True)

def extrair_nome_paciente(caminho_pdf):
    try:
        with pdfplumber.open(caminho_pdf) as pdf:
            primeira_pagina = pdf.pages[0]
            texto = primeira_pagina.extract_text()
            
            # --- O PRINT VEM AQUI ---
            print(f"\n--- Conteúdo lido do arquivo: {os.path.basename(caminho_pdf)} ---")
            print(texto) # Isso vai mostrar tudo que o Python "enxergou" dentro do PDF
            print("---------------------------------------------------\n")
            
            if not texto:
                return None
            
            padrao = re.compile(r'(?:Paciente|Nome):\s*([A-Za-zÀ-ÿ\s]+)', re.IGNORECASE)
            resultado = padrao.search(texto)
            
            if resultado:
                nome_extraido = resultado.group(1).strip()
                print(f"✅ Nome encontrado pela Regex: {nome_extraido}")
                return nome_extraido # Fim da função com sucesso
                
    except Exception as e:
        print(f"❌ Erro ao ler {caminho_pdf}: {e}")
    
    return None # Fim da função se nada for encontrado

def processar_laudos():
    print("Iniciando processamento de laudos...")
    arquivos = [f for f in os.listdir(PASTA_ENTRADA) if f.lower().endswith('.pdf')]
    
    if not arquivos:
        print("Nenhum PDF encontrado na pasta de entrada.")
        return

    for arquivo in arquivos:
        caminho_antigo = os.path.join(PASTA_ENTRADA, arquivo)
        nome_paciente = extrair_nome_paciente(caminho_antigo)
        
        if nome_paciente:
            # Cria o novo nome do arquivo
            novo_nome_arquivo = f"{nome_paciente}.pdf"
            caminho_novo = os.path.join(PASTA_SAIDA, novo_nome_arquivo)
            
            # Move e renomeia
            shutil.move(caminho_antigo, caminho_novo)
            print(f"[SUCESSO] '{arquivo}' renomeado para '{novo_nome_arquivo}'")
        else:
            print(f"[FALHA] Não foi possível encontrar o nome no arquivo '{arquivo}'")

if __name__ == '__main__':
    processar_laudos()

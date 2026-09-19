import os
import json
from dotenv import load_dotenv
from gemini_processor import analisar_texto

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()


def processar_texto(caminho_entrada: str, caminho_saida: str):
    """
    Lê um arquivo de texto, envia para a API do Gemini e salva a análise em JSON.
    """
    if not os.path.exists(caminho_entrada):
        print(f"Erro: O arquivo '{caminho_entrada}' não foi encontrado.")
        return

    with open(caminho_entrada, "r", encoding="utf-8") as f:
        conteudo_texto = f.read()

    print("Enviando texto para análise na API do Gemini...")

    try:
        dados_json = analisar_texto(conteudo_texto)

        with open(caminho_saida, "w", encoding="utf-8") as f_out:
            json.dump(dados_json, f_out, ensure_ascii=False, indent=2)

        print(f"✅ Análise concluída com sucesso! Resultado salvo em: '{caminho_saida}'")
        print("\nConteúdo gerado:")
        print(json.dumps(dados_json, ensure_ascii=False, indent=2))

    except json.JSONDecodeError:
        print("Erro: A resposta da API não veio em formato JSON válido.")
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento: {e}")


if __name__ == "__main__":
    ARQUIVO_ENTRADA = "input.txt"
    ARQUIVO_SAIDA = "resultado_analise.json"

    processar_texto(ARQUIVO_ENTRADA, ARQUIVO_SAIDA)
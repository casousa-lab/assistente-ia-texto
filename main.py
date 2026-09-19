import os
import json
from dotenv import load_dotenv
from google import genai

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa o cliente do Gemini com a chave do .env
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env")

client = genai.Client(api_key=api_key)

def processar_texto(caminho_entrada: str, caminho_saida: str):
    """
    Lê um arquivo de texto, envia para a API do Gemini e salva a análise em JSON.
    """
    if not os.path.exists(caminho_entrada):
        print(f"Erro: O arquivo '{caminho_entrada}' não foi encontrado.")
        return

    # 1. Leitura do arquivo de entrada
    with open(caminho_entrada, "r", encoding="utf-8") as f:
        conteudo_texto = f.read()

    print("Enviando texto para análise na API do Gemini...")

    # 2. Prompt com instrução de saída estrita em JSON
    prompt_completo = (
        "Você é um assistente especialista em processamento de dados e análise de texto corporativo.\n"
        "Sua tarefa é analisar o texto fornecido e retornar ESTRITAMENTE um objeto JSON válido, sem qualquer texto introdutório ou marcadores markdown (como ```json).\n\n"
        "O formato da resposta deve ser rigorosamente o seguinte:\n"
        "{\n"
        '  "resumo": "Um resumo claro e conciso do texto em até 2 frases.",\n'
        '  "categoria": "A categoria principal do texto (Ex: Operações, Financeiro, Tecnologia, RH, Vendas)",\n'
        '  "palavras_chave": ["tag1", "tag2", "tag3"],\n'
        '  "nivel_prioridade": "Alta / Média / Baixa",\n'
        '  "acao_recomendada": "Uma sugestão curta de próxima ação baseada no texto."\n'
        "}\n\n"
        f"Texto para análise:\n{conteudo_texto}"
    )

    try:
        # 3. Chamada via Interactions API usando o modelo exigido gemini-3.6-flash
        interaction = client.interactions.create(
            model="gemini-3.6-flash",
            input=prompt_completo
        )

        # 4. Extração do texto e limpeza de formatação markdown caso o modelo inclua
        resposta_texto = interaction.output_text.strip()
        if resposta_texto.startswith("```"):
            resposta_texto = resposta_texto.split("\n", 1)[-1].rsplit("\n", 1)[0].replace("json", "").strip()

        # 5. Validação do JSON e salvamento
        dados_json = json.loads(resposta_texto)

        with open(caminho_saida, "w", encoding="utf-8") as f_out:
            json.dump(dados_json, f_out, ensure_ascii=False, indent=2)

        print(f"✅ Análise concluída com sucesso! Resultado salvo em: '{caminho_saida}'")
        print("\nConteúdo gerado:")
        print(json.dumps(dados_json, ensure_ascii=False, indent=2))

    except json.JSONDecodeError:
        print("Erro: A resposta da API não veio em formato JSON válido.")
        print("Resposta recebida:\n", resposta_texto)
    except Exception as e:
        print(f"Ocorreu um erro durante o processamento: {e}")

if __name__ == "__main__":
    ARQUIVO_ENTRADA = "input.txt"
    ARQUIVO_SAIDA = "resultado_analise.json"
    
    processar_texto(ARQUIVO_ENTRADA, ARQUIVO_SAIDA)
import os
import json
from google import genai
from google.genai import types

# Nome do modelo configurável via .env (GEMINI_MODEL), com fallback padrão
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")

PROMPT_BASE = (
    "Você é um assistente especialista em processamento de dados e análise de texto corporativo.\n"
    "Analise o texto fornecido e extraia as informações no formato JSON definido pelo schema.\n\n"
    "Campos esperados:\n"
    "- resumo: um resumo claro e conciso do texto em até 2 frases.\n"
    "- categoria: a categoria principal do texto (Ex: Operações, Financeiro, Tecnologia, RH, Vendas).\n"
    "- palavras_chave: lista de 3 a 5 palavras-chave relevantes.\n"
    "- nivel_prioridade: Alta, Média ou Baixa.\n"
    "- acao_recomendada: uma sugestão curta de próxima ação baseada no texto.\n\n"
    "Texto para análise:\n{texto}"
)


def _get_client() -> genai.Client:
    """
    Cria o cliente do Gemini a partir da variável de ambiente GEMINI_API_KEY.
    Levanta ValueError se a chave não estiver configurada.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("A chave GEMINI_API_KEY não foi encontrada no arquivo .env")
    return genai.Client(api_key=api_key)


def analisar_texto(texto: str) -> dict:
    """
    Envia um texto para a API do Gemini e retorna a análise já validada como dict.
    Usa response_mime_type="application/json" para forçar saída JSON nativa,
    eliminando a necessidade de limpar blocos ```json manualmente.
    """
    client = _get_client()

    prompt_completo = PROMPT_BASE.format(texto=texto)

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt_completo,
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )

    return json.loads(response.text)
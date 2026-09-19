# Assistente de Processamento de Texto com IA

Aplicação em Python desenvolvida para automatizar a leitura, categorização e sumarização de textos corporativos utilizando a API do Google Gemini com técnicas avançadas de Prompt Engineering para saída estrita em JSON estruturado. O projeto conta tanto com um script CLI para execução local quanto com uma interface web interativa em Streamlit no estilo Soft UI / SaaS Minimalista.

## Problema

A análise manual de relatórios, chamados operacionais e briefings consome um tempo operacional significativo da equipe de BizOps. Esse processo manual atrasa a tomada de decisões estratégicas e gera riscos de erro humano (como duplicidades de pagamentos ou falhas de comunicação em incidentes graves).

## Solução

Um motor automatizado que processa textos não estruturados (e-mails, relatórios, propostas), consome a API do Google Gemini e extrai resumo executivo, categoria, nível de prioridade, palavras-chave e ações recomendadas em formato JSON limpo e validado — pronto para ser integrado a bancos de dados, workflows no n8n ou sistemas ERP/CRM.

## Tecnologias Utilizadas

* Linguagem: Python 3.10+
* IA Generativa / LLM: Google Gemini API (`google-genai` SDK) — Modelo `gemini-3.5-flash`
* Interface Web: Streamlit (com estilização customizada via CSS Injection)
* Prompt Engineering: Instrução estrita para validação e resposta em formato JSON Schema
* Segurança & Gestão de Variáveis: `python-dotenv`
* Versionamento: Git & GitHub

## Estrutura do Projeto

```
assistente-ia-texto/
├── app.py                  # Aplicação Web Streamlit (Interface Soft UI)
├── main.py                 # Script CLI para processamento de arquivos locais
├── input.txt               # Arquivo de texto de entrada para testes via CLI
├── resultado_analise.json  # Resultado gerado pela execução do script local
├── .env                    # Variáveis de ambiente (chave GEMINI_API_KEY)
├── .gitignore              # Proteção de credenciais e ambiente virtual
└── requirements.txt        # Dependências do projeto
```

## 🚀 Como Executar o Projeto

### 1. Clonar o repositório

```bash
git clone https://github.com/casousa-lab/assistente-ia-texto.git
cd assistente-ia-texto
```

### 2. Criar e ativar um ambiente virtual

```bash
# No Windows:
python -m venv venv
.\venv\Scripts\activate

# No Linux/Mac:
source venv/bin/activate
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar a chave de API

Crie um arquivo `.env` na raiz do projeto com a sua chave obtida gratuitamente no Google AI Studio:

```
GEMINI_API_KEY=sua_chave_api_do_gemini_aqui
```

## ⚙️ Modos de Uso

### Modo 1: Aplicação Web Interativa (Streamlit)

Para rodar a interface gráfica com abas de navegação, histórico de sessão e design moderno:

```bash
streamlit run app.py
```

Acesse no navegador através do endereço local fornecido (geralmente `http://localhost:8501`).

### Modo 2: Execução via Linha de Comando (CLI)

Para processar o arquivo `input.txt` e gerar o `resultado_analise.json`:

1. Cole o texto desejado dentro do arquivo `input.txt`.
2. Execute o comando:

```bash
python main.py
```

## 📊 Exemplo de Saída (resultado_analise.json)

```json
{
  "resumo": "A equipe de operações identificou um gargalo no processamento manual de faturas e propõe a automação da rotina via scripts e APIs.",
  "categoria": "Operações",
  "palavras_chave": [
    "automação",
    "faturas",
    "eficiência"
  ],
  "nivel_prioridade": "Alta",
  "acao_recomendada": "Iniciar projeto de automação para liberar 15h semanais da equipe."
}
```

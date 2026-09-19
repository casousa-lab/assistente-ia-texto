import html
import streamlit as st
from dotenv import load_dotenv
from gemini_processor import analisar_texto

# Configuração da página
st.set_page_config(
    page_title="BizOps Engine",
    page_icon="✨",
    layout="wide"
)

# Injeção de CSS para recriar o visual SaaS Minimalista (Inspirado no Framer/Linear/Acme)
st.markdown("""
    <style>
    /* Fundo Geral da Aplicação */
    .stApp {
        background-color: #F8F9FA !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif !important;
        color: #1F2123 !important;
    }
    
    #MainMenu, footer {visibility: hidden;}

    /* BREADCRUMB SUPERIOR (BARRA TOPO) */
    .top-breadcrumb {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 14px;
        color: #6B7280;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid #E5E7EB;
    }
    .top-breadcrumb strong {
        color: #111827;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .badge-status {
        background-color: #E0F2FE;
        color: #0369A1;
        font-size: 12px;
        font-weight: 500;
        padding: 2px 10px;
        border-radius: 20px;
    }

    /* MENU DE ABAS EM FORMATO DE PÍLULA (PILL SWITCHER) NO CONTEÚDO */
    div[data-testid="stRadio"] > div {
        background-color: #E5E7EB !important;
        padding: 4px !important;
        border-radius: 12px !important;
        gap: 4px !important;
        display: inline-flex !important;
        flex-direction: row !important;
        margin-bottom: 24px !important;
    }

    div[data-testid="stRadio"] label {
        background-color: transparent !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 6px 16px !important;
        color: #4B5563 !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        cursor: pointer !important;
        transition: all 0.2s ease !important;
    }

    div[data-testid="stRadio"] label:hover {
        color: #111827 !important;
    }

    /* ABA SELECIONADA (PILL ELEVADA BRANCA) */
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] {
        background-color: #FFFFFF !important;
        color: #111827 !important;
        font-weight: 600 !important;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.06) !important;
    }

    /* CAIXA DE TEXTO (TEXTAREA) */
    [data-testid="stTextArea"] div,
    [data-testid="stTextArea"] div > div,
    [data-testid="stTextArea"] textarea {
        background-color: #FAFAFA !important;
        color: #111827 !important;
        border-radius: 14px !important;
    }

    [data-testid="stTextArea"] textarea {
        border: 1px solid #E5E7EB !important;
        font-size: 14px !important;
        font-weight: 400 !important;
        line-height: 1.6 !important;
        padding: 14px !important;
    }

    [data-testid="stTextArea"] textarea:focus {
        background-color: #FFFFFF !important;
        border-color: #9CA3AF !important;
        box-shadow: none !important;
    }

    /* BOTÃO PROPORCIONAL ESCURO */
    div.stButton {
        display: flex !important;
        justify-content: flex-start !important;
    }

    div.stButton > button {
        background-color: #111827 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        padding: 8px 18px !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        border: none !important;
        width: auto !important;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.08) !important;
    }
    
    div.stButton > button:hover {
        background-color: #1F2937 !important;
    }

    /* CARDS DE RESULTADO */
    .custom-card {
        background-color: #FFFFFF;
        border: 1px solid #E5E7EB;
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 12px;
        box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.015);
    }

    .card-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #6B7280;
        margin-bottom: 6px;
    }

    .card-value {
        font-size: 16px;
        font-weight: 600;
        color: #111827;
    }

    /* BADGES */
    .tag-badge {
        display: inline-block;
        background-color: #F3F4F6;
        color: #374151;
        border: 1px solid #E5E7EB;
        border-radius: 6px;
        padding: 3px 8px;
        font-size: 12px;
        font-weight: 500;
        margin-right: 4px;
        margin-bottom: 4px;
    }

    .priority-alta { background-color: #FEE2E2; color: #991B1B; border-color: #FCA5A5; }
    .priority-media { background-color: #FEF3C7; color: #92400E; border-color: #FCD34D; }
    .priority-baixa { background-color: #E0F2FE; color: #075985; border-color: #7DD3FC; }
    </style>
""", unsafe_allow_html=True)

# Carrega as variáveis de ambiente
load_dotenv()

# Estado de sessão para armazenar o histórico
if "historico" not in st.session_state:
    st.session_state.historico = []

# --- 1. BREADCRUMB SUPERIOR ---
st.markdown("""
    <div class='top-breadcrumb'>
        <strong>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#111827" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/></svg>
            BizOps Automation
        </strong> 
        <span>/</span> 
        <span style='color: #111827; font-weight: 500;'>Text Engine</span>
        <span class='badge-status'>Active</span>
    </div>
""", unsafe_allow_html=True)

# --- 2. MENU DE NAVEGAÇÃO EM ABAS (ESTILO ACME / WEBCORE ELEMENTS & SYMBOL) ---
menu_selecionado = st.radio(
    label="Menu",
    options=["Elements", "Symbol / History", "Platform Specs"],
    label_visibility="collapsed"
)

# --- ABA 1: ELEMENTS (PROCESSAMENTO DE TEXTO) ---
if menu_selecionado == "Elements":
    col_input, col_output = st.columns([1, 1], gap="large")

    with col_input:
        st.markdown("<div class='card-label'>INPUT DOCUMENT</div>", unsafe_allow_html=True)
        texto_usuario = st.text_area(
            label="Input",
            label_visibility="collapsed",
            height=280,
            placeholder="Cole aqui o e-mail, relatório ou texto de operações..."
        )
        
        botao_processar = st.button("Process with AI", use_container_width=False)

    with col_output:
        st.markdown("<div class='card-label'>JSON STRUCTURED OUTPUT</div>", unsafe_allow_html=True)
        
        if botao_processar:
            if not texto_usuario.strip():
                st.warning("Insira um texto para analisar.")
            else:
                with st.spinner("Processing..."):
                    try:
                        dados_json = analisar_texto(texto_usuario)
                        st.session_state.historico.append(dados_json)

                        # Escapa tudo que vem do modelo antes de injetar em HTML (proteção contra XSS)
                        categoria = html.escape(str(dados_json.get("categoria", "N/A")))
                        prioridade_raw = str(dados_json.get("nivel_prioridade", "Baixa"))
                        prioridade = html.escape(prioridade_raw)
                        resumo = html.escape(str(dados_json.get("resumo", "")))
                        acao = html.escape(str(dados_json.get("acao_recomendada", "")))

                        classe_prioridade = "priority-baixa"
                        if "alta" in prioridade_raw.lower():
                            classe_prioridade = "priority-alta"
                        elif "média" in prioridade_raw.lower() or "media" in prioridade_raw.lower():
                            classe_prioridade = "priority-media"

                        st.markdown(f"""
                            <div class='custom-card'>
                                <div style='display: flex; justify-content: space-between; align-items: center;'>
                                    <div>
                                        <div class='card-label'>Categoria</div>
                                        <div class='card-value'>{categoria}</div>
                                    </div>
                                    <div style='text-align: right;'>
                                        <div class='card-label'>Prioridade</div>
                                        <span class='tag-badge {classe_prioridade}'>{prioridade}</span>
                                    </div>
                                </div>
                            </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                            <div class='custom-card'>
                                <div class='card-label'>Resumo Executivo</div>
                                <div style='font-size: 14px; color: #374151; line-height: 1.6;'>{resumo}</div>
                            </div>
                        """, unsafe_allow_html=True)

                        st.markdown(f"""
                            <div class='custom-card'>
                                <div class='card-label'>Ação Recomendada</div>
                                <div style='font-size: 14px; color: #111827; font-weight: 500; line-height: 1.6;'>{acao}</div>
                            </div>
                        """, unsafe_allow_html=True)

                        tags_html = "".join([
                            f"<span class='tag-badge'>{html.escape(str(tag))}</span>"
                            for tag in dados_json.get("palavras_chave", [])
                        ])
                        st.markdown(f"""
                            <div class='custom-card'>
                                <div class='card-label'>Palavras-chave</div>
                                <div>{tags_html}</div>
                            </div>
                        """, unsafe_allow_html=True)

                        with st.expander("Ver JSON bruto"):
                            st.json(dados_json)

                    except Exception as e:
                        st.error(f"Erro no processamento: {e}")

# --- ABA 2: SYMBOL / HISTORY ---
elif menu_selecionado == "Symbol / History":
    st.markdown("<div class='card-label'>SESSION HISTORY</div>", unsafe_allow_html=True)
    if not st.session_state.historico:
        st.info("Nenhuma análise registrada na sessão atual.")
    else:
        for idx, item in enumerate(reversed(st.session_state.historico), 1):
            with st.expander(f"Record #{len(st.session_state.historico) - idx + 1} — {item.get('categoria', 'N/A')}"):
                st.json(item)

# --- ABA 3: PLATFORM SPECS ---
elif menu_selecionado == "Platform Specs":
    st.markdown("<div class='card-label'>ARCHITECTURE</div>", unsafe_allow_html=True)
    st.markdown("""
        <div class='custom-card'>
            <div class='card-label'>Propósito</div>
            <p style='font-size: 14px; color: #374151;'>
                Engine automatizado para conversão de texto não-estruturado corporativo em JSON estrito para consumo em rotinas de BizOps e ERPs.
            </p>
        </div>
    """, unsafe_allow_html=True)
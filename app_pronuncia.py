import streamlit as st
import json
import re
from gtts import gTTS
import io
import base64
import random

# Configuração da página
st.set_page_config(
    page_title=" Aruak _ Vozes do Terena",
    page_icon="🗣️",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #2E8B57;
        font-size: 2.5rem;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .translation-box {
        background: linear-gradient(135deg, #000 0%, #006464 100%);
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        border-left: 5px solid #2E8B57;
    }
    .cultural-info {
        background: #fff3cd;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #ffc107;
        margin: 15px 0;
    }
    .audio-section {
        background: #e8f5e8;
        padding: 15px;
        border-radius: 8px;
        margin: 15px 0;
    }
    .word-match {
        background-color: #90EE90;
        padding: 2px 4px;
        border-radius: 3px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def carregar_dicionario():
    """Carrega o dicionário do arquivo JSON"""
    try:
        with open('dicionario_terena.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("Arquivo dicionario_terena.json não encontrado!")
        return 

def remover_acentos(texto):
    # Mantida sua função original, que já cobre letras acentuadas comuns
    return re.sub(r'[àáâãäçèéêëìíîïòóôõöùúûü]', lambda match: {'à': 'a', 'á': 'a', 'â': 'a', 'ã': 'a', 'ä': 'a',
                                                              'ç': 'c',
                                                              'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e',
                                                              'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i',
                                                              'ò': 'o', 'ó': 'o', 'ô': 'o', 'õ': 'o', 'ö': 'o',
                                                              'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u',
                                                              'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A',
                                                              'Ç': 'C',
                                                              'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E',
                                                              'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I',
                                                              'Ò': 'O', 'Ó': 'O', 'Ô': 'O', 'Õ': 'O', 'Ö': 'O',
                                                              'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U'}[match.group(0)], texto)

# >>> NOVO: helper para escolher o texto que vai para o áudio (pronuncia -> terena_completo -> terena)
def texto_para_audio(item):
    bruto = (item.get('pronuncia')
             or item.get('terena_completo')
             or item.get('terena')
             or '')
    # remove diacríticos via sua função e também sinais que fazem o TTS falar "acento ..."
    texto = remover_acentos(bruto)
    texto = re.sub(r"[’'`´^~¨]", "", texto)   # remove marcas e apóstrofos
    texto = re.sub(r"\s+", " ", texto).strip()
    return texto

def buscar_traducoes(frase, vocabulario):
    """Busca traduções para palavras na frase"""
    frase_lower = frase.lower()
    traducoes_encontradas = []
    palavras_traduzidas = []
    frase_limpa = remover_acentos(frase_lower)
    
    # Ordenar por tamanho decrescente para pegar expressões maiores primeiro
    for entrada in vocabulario:
        palavra_pt = entrada['portugues']
        palavra_pt_lower = palavra_pt.lower()
        palavra_limpa = remover_acentos(palavra_pt_lower)
        
        if palavra_limpa in frase_limpa and palavra_limpa not in palavras_traduzidas:
            traducoes_encontradas.append(entrada)

        
           
    return traducoes_encontradas

def gerar_audio_terena(texto_terena):
    """Gera áudio em português para simular pronúncia do Terena"""
    try:
        # >>> AJUSTE: reforçar higienização antes do gTTS
        texto_adaptado = texto_terena or ""
        # adaptações simples já existentes:
        texto_adaptado = texto_adaptado.replace("'", "").replace("ã", "an").replace("ẽ", "en")
        # remoção de acentos/sinais que fazem o TTS falar "acento ..."
        texto_adaptado = remover_acentos(texto_adaptado)
        texto_adaptado = re.sub(r"[’'`´^~¨]", "", texto_adaptado)
        texto_adaptado = re.sub(r"\s+", " ", texto_adaptado).strip()

        tts = gTTS(text=texto_adaptado, lang='pt', slow=False)
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)

        # Converter para base64 para reprodução no Streamlit
        audio_base64 = base64.b64encode(audio_buffer.read()).decode()
        return audio_base64
    except Exception as e:
        st.error(f"Erro ao gerar áudio: {e}")
        return None

def obter_contexto_cultural(palavra):
    """Retorna informações culturais sobre palavras específicas"""
    contextos = {
        
    }

    for palavra, contexto in contextos.items():
        if palavra in palavra.lower():
            return contexto

    return "Esta palavra faz parte do rico vocabulário Terena, língua falada por comunidades indígenas do Estado de Mato Grosso do Sul."

def main():
    # Cabeçalho
    st.markdown('<h1 class="main-header">🗣️  Vozes do povo Terena</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Tradutor audiovisual e cultural Português ↔ Terena</p>', unsafe_allow_html=True)

    # Carregar dicionário
    vocabulario = carregar_dicionario()

    if not vocabulario:
        st.error("Não foi possível carregar o dicionário. Verifique se o arquivo está presente.")
        return

    # Sidebar com informações
    with st.sidebar:
        st.header(st.logo(
            LOGO_URL_LARGE,
            link="https://streamlit.io/gallery",
            icon_image=LOGO_URL_SMALL,
             "Sobre o Projeto"))
        st.write("""
        Este tradutor utiliza o vocabulário bilíngue Terena ↔ Português 
        estruturado com fontes de pesquisa confiáveis
        """)

        st.header("🎯 Como usar")
        st.write("""
        1. Digite uma frase em português
        2. Clique em "Traduzir"
        3. Ouça a pronúncia em Terena
        4. Leia o contexto cultural
        """)

        st.header("📊 Estatísticas")
        st.metric("Palavras no dicionário", 830 )

        # Palavra do dia
        st.header("🎲 Palavra aleatória")
        palavra_dia = random.choice(vocabulario)
        st.write(f"**{palavra_dia['portugues'].title()}**")
        st.write(f"*{palavra_dia['terena']}*")

    # Interface principal
    col1, col2 = st.columns([2, 1])

    with col1:
        st.header("💬 Tradutor")

        # Entrada de texto
        frase_input = st.text_input(
            "Digite uma frase em português:",
            placeholder="Ex: Enxada",
            help="Digite palavras ou frases curtas para melhor resultado"
        )

        # Botões
        col_btn1, col_btn2, col_btn3 = st.columns(3)

        with col_btn1:
            traduzir = st.button("🔄 Traduzir", type="primary")

        with col_btn3:
            if st.button("🗑️ Limpar"):
                frase_input = ""
                st.rerun()

    with col2:
        st.header("🔍 Busca Rápida")
        busca = st.text_input("Buscar palavra:", placeholder="Ex: água")

        if busca:
            resultados = [v for v in vocabulario if busca.lower() in v['portugues'].lower()]
            if resultados:
                for resultado in resultados[:5]:  
                    st.write(f"**{resultado['portugues']}** → *{resultado['terena']}*")
            else:
                st.write("Nenhuma palavra encontrada.")

    # Processamento da tradução
    if traduzir and frase_input:
        st.markdown("---")

        # Buscar traduções
        traducoes = buscar_traducoes(frase_input, vocabulario)

        if traducoes:
            # Construir tradução (EXIBIÇÃO mantém acentos)
            palavras_terena_significado = [t['explicacao'] for t in traducoes]
            traducao_completa_significado = ' '.join(palavras_terena_significado)
            palavras_terena_exibir = [t['terena'] for t in traducoes]
            traducao_completa_exibir = ' '.join(palavras_terena_exibir)
            pronuncia_terena_exibir = [t['pronuncia'] for t in traducoes]
            pronuncia_completa_exibir = ' '.join(pronuncia_terena_exibir)

            # >>> AJUSTE: TEXTO DO ÁUDIO usa pronuncia -> terena_completo -> terena, higienizado
            palavras_terena_som = [texto_para_audio(t) for t in traducoes]
            traducao_completa_som = ' '.join(palavras_terena_som)

            # Exibir resultado
            st.markdown(f"""
            <div class="translation-box">
                <h3>🎯 Tradução</h3>
                <p><strong>Português:</strong> {frase_input}</p>
                <p><strong>Terena:</strong> <span style="font-size: 1.3em; color: #2E8B57;">{traducao_completa_exibir}</span></p>
                <p><span style="font-size: 0.8em;"><strong>pronúncia: </strong></span><span style="font-size: 0.8em; color: #2E8B57;">{pronuncia_completa_exibir}</span></p>
            </div>
            """, unsafe_allow_html=True)

            # Seção de áudio
            st.markdown('<div class="audio-section">', unsafe_allow_html=True)
            st.subheader("🔊 Pronúncia")

            audio_base64 = gerar_audio_terena(traducao_completa_som)
            if audio_base64:
                audio_html = f"""
                <audio controls>
                    <source src="data:audio/mp3;base64,{audio_base64}" type="audio/mp3">
                    Seu navegador não suporta áudio.
                </audio>
                """
                st.markdown(audio_html, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # Palavras encontradas
            st.subheader("📝 Palavras Traduzidas")
            cols = st.columns(min(len(traducoes), 3))

            for i, traducao in enumerate(traducoes):
                with cols[i % 3]:
                    st.info(f"**{traducao['portugues']}** → *{traducao['terena']}*")

            # Contexto cultural
            st.markdown('<div class="cultural-info">', unsafe_allow_html=True)
            st.subheader("🌿 Contexto Cultural")
            st.markdown(f"""
            <div class="contexto_cultural">
                <p><strong>Palavra:</strong> {traducao_completa_exibir}</p>
                <p><strong>Significado:</strong> <span style="font-size: 1em; color: #2E8B57;">{traducao_completa_significado}</span></p>
            </div>
            """, unsafe_allow_html=True)
            # Pegar contexto da primeira palavra traduzida
            contexto = obter_contexto_cultural(traducoes[0]['portugues'])
            st.write(contexto)

            # Informações adicionais sobre variações dialetais
            if any('[' in t['terena'] for t in traducoes):
                st.write("💡 **Nota:** Algumas palavras possuem variações dialetais entre as aldeias ([BA] Bananal, [PI] Piaçaguera, [PY] Pyhau).")

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.warning("⚠️ Nenhuma palavra foi encontrada no dicionário. Tente palavras mais simples ou consulte o vocabulário disponível.")

            # Sugestões
            st.subheader("💡 Sugestões")
            sugestoes = random.sample(vocabulario, 6)
            cols = st.columns(3)

            for i, sugestao in enumerate(sugestoes):
                with cols[i % 3]:
                    st.write(f"• {sugestao['portugues']} → *{sugestao['terena']}*")

    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 2rem;">
        <p>📚 Baseado no Vocabulário Bilíngue Terenas – Português</p>
        <p>🏛️ IFMS Nova Andradina</p>
        <p>🌿 Preservando e valorizando as línguas indígenas</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

import streamlit as st
from datetime import datetime
import pytz

# ============================================
# CONFIG PAGE
# ============================================
st.set_page_config(
    page_title="Gerador de Sobreaviso DRV/DEIC",
    page_icon="📅",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# DADOS (Constants)
# ============================================
PEOPLE = [
    {"val": "Cau", "label": "Insp. Acauã"},
    {"val": "Saraiva", "label": "Esc. Anderson Saraiva"},
    {"val": "Brozoza", "label": "Insp. Alexandre Brozoza"},
    {"val": "Cátia", "label": "Esc. Cátia Fortunato"},
    {"val": "Cristiano", "label": "Insp. Cristiano Soletti"},
    {"val": "César", "label": "Esc. César da Costa"},
    {"val": "Dago", "label": "Esc. Dagoberto O. das Virgens"},
    {"val": "Melo", "label": "Insp. Edmilson Melo"},
    {"val": "Edna", "label": "Insp. Edna Moraes"},
    {"val": "Piazza", "label": "Esc. Fernanda Piazza"},
    {"val": "Gui Mello", "label": "Insp. Guilherme Mello"},
    {"val": "Jeff", "label": "Esc. Jefferson Antoniol"},
    {"val": "Juliana", "label": "Insp. Juliana Tremper"},
    {"val": "Bona", "label": "Insp. Juliano Bonacina"},
    {"val": "Luciana", "label": "Esc. Luciana Bortoli"},
    {"val": "Loss", "label": "Insp. Lucas Loss"},
    {"val": "Tais", "label": "Insp. Tais Boesing"},
    {"val": "Teresinha", "label": "Insp. Teresinha Carivali"},
    {"val": "Thiago", "label": "Insp. Thiago Meireles"},
    {"val": "Thássia", "label": "Insp. Thássia Guterres"},
    {"val": "Vanessa", "label": "Insp. Vanessa Trindade"}
]

NAME_MAP = {p["val"]: p["label"] for p in PEOPLE}

PHONE_MAP = {
    "Cau": "(51) 986859065", "Piazza": "(51) 993605744", "Cristiano": "(51) 995659880",
    "Teresinha": "(51) 999829606", "Thiago": "(79) 988080613", "César": "(51) 998911160",
    "Vanessa": "(55) 984278960", "Bona": "(51) 989276060", "Gui Mello": "(51) 981354933",
    "Tais": "(51) 980549435", "Jeff": "(24) 981002933", "Luciana": "(51) 993935552",
    "Edna": "(53) 981339654", "Saraiva": "(51) 993879343", "Loss": "(51) 991055571",
    "Brozoza": "(51) 996500506", "Dago": "(51) 999920066", "Thássia": "(51) 996499862",
    "Juliana": "(51) 993337587", "Cátia": "(51) 985744501", "Melo": "(51) 983190815"
}

SCHEDULE = {
    "01/11/2025": ["Cristiano", "Vanessa", "Thiago"],
    "02/11/2025": ["Cristiano", "Vanessa", "Thiago"],
    "03/11/2025": ["Piazza", "César", "Vanessa"],
    "04/11/2025": ["Bona", "Vanessa", "Saraiva"],
    "05/11/2025": ["Dago", "Thássia", "Thiago"],
    "06/11/2025": ["Jeff", "Teresinha", "Saraiva"],
    "07/11/2025": ["Cristiano", "Teresinha", "Thiago"],
    "08/11/2025": ["Jeff", "Juliana", "Tais"],
    "09/11/2025": ["Jeff", "Luciana", "Edna"],
    "10/11/2025": ["Gui Mello", "Bona", "Tais"],
    "11/11/2025": ["Brozoza", "Loss", "Saraiva"],
    "12/11/2025": ["Cau", "Luciana", "Edna"],
    "13/11/2025": ["Melo", "Cátia", "Jeff"],
    "14/11/2025": ["Piazza", "Bona", "Saraiva"],
    "15/11/2025": ["Gui Mello", "Thássia", "Saraiva"],
    "16/11/2025": ["Gui Mello", "Loss", "Saraiva"],
    "17/11/2025": ["César", "Teresinha", "Jeff"],
    "18/11/2025": ["Dago", "Cátia", "Edna"],
    "19/11/2025": ["Jeff", "Thássia", "Saraiva"],
    "20/11/2025": ["Cristiano", "Juliana", "Thiago"],
    "21/11/2025": ["Gui Mello", "Melo", "Thiago"],
    "22/11/2025": ["Brozoza", "Loss", "Thiago"],
    "23/11/2025": ["Brozoza", "Loss", "Thiago"],
    "24/11/2025": ["Cau", "Luciana", "Saraiva"],
    "25/11/2025": ["Brozoza", "Loss", "Vanessa"],
    "26/11/2025": ["Melo", "Vanessa", "Jeff"],
    "27/11/2025": ["Piazza", "Gui Mello", "Tais"],
    "28/11/2025": ["César", "Juliana", "Vanessa"],
    "29/11/2025": ["Cau", "Luciana", "Edna"],
    "30/11/2025": ["Cau", "Juliana", "Edna"],
    "01/12/2025": ["Dago", "Cátia", ""],
    "02/12/2025": ["Jeff", "Vanessa", ""],
    "03/12/2025": ["Cristiano", "Juliana", ""],
    "04/12/2025": ["Gui Mello", "Jeff", ""],
    "05/12/2025": ["Brozoza", "Loss", ""],
    "06/12/2025": ["Melo", "Thássia", ""],
    "07/12/2025": ["Melo", "Thássia", ""],
    "08/12/2025": ["Cau", "Luciana", ""],
    "09/12/2025": ["Melo", "Thássia", ""],
    "10/12/2025": ["Piazza", "Bona", ""],
    "11/12/2025": ["César", "Teresinha", ""],
    "12/12/2025": ["Dago", "Cátia", ""],
    "13/12/2025": ["Piazza", "Bona", ""],
    "14/12/2025": ["Piazza", "Bona", ""],
    "15/12/2025": ["Jeff", "Vanessa", ""],
    "16/12/2025": ["Cristiano", "Juliana", ""],
    "17/12/2025": ["Gui Mello", "Teresinha", ""],
    "18/12/2025": ["Brozoza", "Loss", ""],
    "19/12/2025": ["Cau", "Luciana", ""],
    "20/12/2025": ["César", "Teresinha", ""],
    "21/12/2025": ["César", "Teresinha", ""],
    "22/12/2025": ["Melo", "Thássia", ""],
    "23/12/2025": ["Piazza", "Bona", ""],
    "24/12/2025": ["César", "Teresinha", ""],
    "25/12/2025": ["Dago", "Cátia", ""],
    "26/12/2025": ["Jeff", "Vanessa", ""],
    "27/12/2025": ["Dago", "Cátia", ""],
    "28/12/2025": ["Dago", "Cátia", ""],
    "29/12/2025": ["Cristiano", "Juliana", ""],
    "30/12/2025": ["Gui Mello", "Brozoza", ""],
    "31/12/2025": ["Brozoza", "Loss", ""]
}

DATES = sorted(SCHEDULE.keys(), key=lambda x: datetime.strptime(x, "%d/%m/%Y"))

# ============================================
# FUNÇÕES AUXILIARES
# ============================================

def get_day_of_week(date_str: str) -> str:
    """Retorna o dia da semana em português"""
    date_obj = datetime.strptime(date_str, "%d/%m/%Y")
    days = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira",
            "sexta-feira", "sábado", "domingo"]
    return days[date_obj.weekday()]

def get_today_brasilia():
    """Retorna a data de hoje em Brasília"""
    tz = pytz.timezone('America/Sao_Paulo')
    today = datetime.now(tz).strftime("%d/%m/%Y")
    return today

def build_message(date: str, custom_schedule=None, include_weekday: bool = False) -> str:
    """Constrói a mensagem de sobreaviso"""
    escala = custom_schedule if custom_schedule is not None else SCHEDULE.get(date)
    
    if not escala:
        return "Nenhum sobreaviso encontrado para essa data ou seleção."
    
    sa01 = escala[0] if len(escala) > 0 else ""
    sa02 = escala[1] if len(escala) > 1 else ""
    sa_nac = escala[2] if len(escala) > 2 else ""
    
    weekday_str = f" ({get_day_of_week(date)})" if include_weekday else ""
    
    text = f"*Sobreaviso DRV/DEIC*\nData: {date}{weekday_str}\n\n"
    
    if sa01 and sa01 in NAME_MAP:
        text += f"{NAME_MAP[sa01]}\n{PHONE_MAP.get(sa01, '-')}\n\n"
    
    if sa02 and sa02 in NAME_MAP:
        text += f"{NAME_MAP[sa02]}\n{PHONE_MAP.get(sa02, '-')}\n\n"
    
    if sa_nac and sa_nac in NAME_MAP:
        text += f"NAC: {NAME_MAP[sa_nac]}\n{PHONE_MAP.get(sa_nac, '-')}\n\n"
    
    text += "Chefe de SI: Com. Bruna Caldeira\n(51) 99139-9403\n\nAutoridade Policial:\nDel. Jeiselaure de Souza\n(51) 99145-8919"
    
    return text

# ============================================
# INICIALIZAR SESSION STATE
# ============================================

if "output_text" not in st.session_state:
    st.session_state.output_text = ""

if "active_tab" not in st.session_state:
    st.session_state.active_tab = "data"

if "today" not in st.session_state:
    st.session_state.today = get_today_brasilia()

# ============================================
# HEADER
# ============================================

st.markdown("""
<style>
    .main-header {
        text-align: center;
        font-size: 2.5em;
        font-weight: bold;
        margin-bottom: 0.5em;
        color: #1f2937;
    }
    .subheader {
        text-align: center;
        font-size: 0.9em;
        color: #6b7280;
        margin-bottom: 2em;
    }
    .tab-button {
        padding: 12px 24px;
        font-size: 1em;
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
        margin: 0 5px;
        font-weight: 600;
    }
    .tab-active {
        background-color: #3b82f6;
        color: white;
        box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
    }
    .tab-inactive {
        background-color: #e5e7eb;
        color: #374151;
    }
    .tab-inactive:hover {
        background-color: #d1d5db;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<p class="main-header">📅 Gerador de Sobreaviso</p>', unsafe_allow_html=True)
    st.markdown('<p class="main-header" style="font-size: 1.8em; margin-top: -0.5em;">DRV/DEIC</p>', unsafe_allow_html=True)
    st.markdown('<p class="subheader">Hoje: ' + st.session_state.today + ' (' + get_day_of_week(st.session_state.today) + ')</p>', unsafe_allow_html=True)

st.markdown("---")

# ============================================
# TABS
# ============================================

tab1, tab2, tab3 = st.tabs(["📅 Buscar por Data", "👤 Buscar por Pessoa", "🔄 Trocas"])

# ============================================
# TAB 1: BUSCAR POR DATA
# ============================================

with tab1:
    st.subheader("📅 Buscar por Data")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Tentar colocar data de hoje como padrão
        today_date = st.session_state.today
        if today_date in DATES:
            default_index = DATES.index(today_date)
        else:
            default_index = 0
        
        selected_date = st.selectbox(
            "Selecione a data:",
            DATES,
            index=default_index,
            key="date_select"
        )
    
    with col2:
        if st.button("🔄 Mostrar", key="btn_date"):
            pass
    
    if selected_date:
        st.session_state.output_text = build_message(selected_date)

# ============================================
# TAB 2: BUSCAR POR PESSOA
# ============================================

with tab2:
    st.subheader("👤 Buscar por Pessoa")
    
    col1, col2 = st.columns([3, 1])
    
    person_names = [p["label"] for p in PEOPLE]
    
    with col1:
        selected_person_label = st.selectbox(
            "Selecione uma pessoa:",
            person_names,
            key="person_select"
        )
    
    with col2:
        if st.button("🔄 Mostrar", key="btn_person"):
            pass
    
    if selected_person_label:
        selected_person = next((p["val"] for p in PEOPLE if p["label"] == selected_person_label), None)
        
        if selected_person:
            result = ""
            nov_count = 0
            dec_count = 0
            dates_found = []
            
            for date in DATES:
                if selected_person in SCHEDULE[date]:
                    dates_found.append(date)
                    if "/11/" in date:
                        nov_count += 1
                    elif "/12/" in date:
                        dec_count += 1
            
            if not dates_found:
                result = "❌ Nenhum sobreaviso encontrado para essa pessoa."
            else:
                result = f"📊 **Novembro:** {nov_count} sobreavisos\n"
                result += f"📊 **Dezembro:** {dec_count} sobreavisos\n\n"
                result += "════════════════════════════════════════\n\n"
                
                for i, date in enumerate(dates_found):
                    if i > 0:
                        result += "\n\n════════════════════════════════════════\n\n"
                    result += build_message(date, include_weekday=True)
            
            st.session_state.output_text = result

# ============================================
# TAB 3: TROCAS
# ============================================

with tab3:
    st.subheader("🔄 Fazer Trocas")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        swap_date = st.selectbox(
            "Selecione a data da troca:",
            DATES,
            key="swap_date_select"
        )
    
    with col2:
        if st.button("🔄 Mostrar", key="btn_swap"):
            pass
    
    if swap_date:
        original_escala = SCHEDULE[swap_date]
        st.info(f"**Escala original para {swap_date}:**\n" +
                "\n".join([f"Posição {i+1}: {NAME_MAP.get(p, '(vago)')}" for i, p in enumerate(original_escala)]))
        
        swaps = {}
        
        for i in range(3):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                original = original_escala[i] if i < len(original_escala) else ""
                original_label = NAME_MAP.get(original, "Vago")
                st.write(f"**Pos. {i+1}:** {original_label}")
            
            with col2:
                person_options = ["--- Manter Original ---"] + person_names
                selected_swap = st.selectbox(
                    f"Substituto para posição {i+1}:",
                    person_options,
                    key=f"swap_{i}"
                )
                
                if selected_swap != "--- Manter Original ---":
                    swaps[i] = next((p["val"] for p in PEOPLE if p["label"] == selected_swap), None)
        
        if st.button("📝 Gerar texto com trocas", key="apply_swaps"):
            custom_schedule = list(original_escala)
            for idx, person in swaps.items():
                if idx < len(custom_schedule):
                    custom_schedule[idx] = person
            
            st.session_state.output_text = build_message(swap_date, custom_schedule)

# ============================================
# OUTPUT AREA
# ============================================

st.markdown("---")

st.subheader("📋 Resultado")

output_text = st.text_area(
    "Texto gerado:",
    value=st.session_state.output_text,
    height=200,
    label_visibility="collapsed",
    key="output_area"
)

st.session_state.output_text = output_text

# ============================================
# ACTION BUTTONS
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("📋 Copiar Texto", use_container_width=True):
        st.success("✅ Copie o texto acima com Ctrl+C (ou Cmd+C)")

with col2:
    if st.button("💚 WhatsApp", use_container_width=True):
        if output_text:
            wa_link = f"https://wa.me/?text={output_text.replace(chr(10), '%0A')}"
            st.markdown(f"[Abrir WhatsApp]({wa_link})", unsafe_allow_html=True)
        else:
            st.warning("Gere um texto primeiro!")

with col3:
    if st.button("📱 Compartilhar", use_container_width=True):
        if output_text:
            st.info("Copie o texto acima e compartilhe via SMS ou Email")
        else:
            st.warning("Gere um texto primeiro!")

with col4:
    if st.button("🗑️ Limpar Tudo", use_container_width=True):
        st.session_state.output_text = ""
        st.rerun()

# ============================================
# FOOTER
# ============================================

st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #6b7280; font-size: 0.85em; margin-top: 2em;">
    🔒 <strong>Aplicação segura e protegida.</strong> Código não é acessível.<br>
    Desenvolvido especialmente para DRV/DEIC
</div>
""", unsafe_allow_html=True)

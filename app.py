import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random

# =====================
# 🔧 Grundkonfiguration
# =====================
st.set_page_config(
    page_title="VIA Charakterstärken Test",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS für Premium Design mit Farbverlauf und Animationen
st.markdown("""
<style>
    /* Haupt-Farbverlauf Hintergrund */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        background-attachment: fixed;
    }
    
    /* Container für weißen Content-Bereich */
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        min-height: 100vh;
    }
    
    /* Header mit Farbverlauf */
    .main-header {
        font-size: 3rem !important;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 800;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .sub-header {
        font-size: 1.5rem !important;
        color: #2e86ab;
        margin-bottom: 1.5rem;
        font-weight: 600;
        text-align: center;
    }
    
    /* Info Box mit Schatten und Animation */
    .info-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        border: none;
        animation: fadeIn 0.8s ease-in;
    }
    
    /* Progress Container */
    .progress-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        animation: slideIn 0.6s ease-out;
    }
    
    /* Question Cards mit Hover-Effekt */
    .question-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
        margin: 1.5rem 0;
        border: 1px solid #e9ecef;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        position: relative;
        overflow: hidden;
    }
    
    .question-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .question-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    /* Animierte Radio Buttons */
    .stRadio > div {
        flex-direction: row;
        align-items: center;
        gap: 8px;
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 12px;
        margin: 0.5rem 0;
    }
    
    .stRadio > div > label {
        flex: 1;
        margin-bottom: 0px;
        padding: 12px 20px;
        border-radius: 10px;
        border: 2px solid #e9ecef;
        background: white;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-align: center;
        font-weight: 500;
        cursor: pointer;
        position: relative;
        overflow: hidden;
    }
    
    .stRadio > div > label:hover {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border-color: transparent;
        transform: scale(1.02);
    }
    
    .stRadio > div > label:has(input:checked) {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-color: transparent;
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar Design */
    .sidebar-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1rem 0;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    
    .metric-box {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.08);
        text-align: center;
        border-left: 4px solid #667eea;
        transition: transform 0.2s ease;
    }
    
    .metric-box:hover {
        transform: translateY(-2px);
    }
    
    /* Button Design */
    .stButton button {
        width: 100%;
        border-radius: 12px;
        padding: 15px 30px;
        font-weight: 600;
        font-size: 1.1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.5);
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
    
    /* Animations */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    /* Success Message */
    .stSuccess {
        background: linear-gradient(135deg, #56ab2f 0%, #a8e6cf 100%) !important;
        color: white !important;
        border-radius: 15px !important;
        padding: 1.5rem !important;
        border: none !important;
        animation: pulse 2s infinite;
    }
    
    /* Tab Design */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: #f8f9fa;
        padding: 8px;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background: white;
        border-radius: 8px;
        border: 2px solid transparent;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border-radius: 8px !important;
        transform: scale(1.05);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 📚 Charakterstärken-Daten
# =========================
CHARACTER_STRENGTHS = {
    "Liebe zum Lernen": {"domain": "🧠 Weisheit & Wissen", "color": "#4E79A7", "questions": [
        "Ich lese regelmäßig Bücher oder Artikel, um Neues zu lernen",
        "Neue Themen wecken sofort mein Interesse",
        "Ich besuche häufig Kurse oder Workshops aus Interesse am Thema",
        "Das Gefühl, etwas dazugelernt zu haben, bereitet mir Freude"
    ]},
    "Urteilsvermögen": {"domain": "🧠 Weisheit & Wissen", "color": "#4E79A7", "questions": [
        "Ich hinterfrage Informationen, bevor ich sie akzeptiere",
        "Bei Entscheidungen wäge ich verschiedene Perspektiven ab",
        "Ich ändere meine Meinung, wenn neue Fakten vorliegen",
        "Komplexe Probleme analysiere ich gründlich"
    ]},
    "Neugier": {"domain": "🧠 Weisheit & Wissen", "color": "#4E79A7", "questions": [
        "Ich stelle oft Fragen, um Dinge besser zu verstehen",
        "Unbekannte Orte und Aktivitäten reizen mich",
        "Ich erkunde gerne neue Ideen und Konzepte",
        "Alltägliche Dinge betrachte ich oft mit Staunen"
    ]},
    "Kreativität": {"domain": "🧠 Weisheit & Wissen", "color": "#4E79A7", "questions": [
        "Ich habe oft originelle und einfallsreiche Ideen",
        "Ich suche nach neuen Wegen, um Aufgaben zu erledigen",
        "Kreative Lösungen machen mir besondere Freude",
        "Ich denke gerne über unkonventionelle Ansätze nach"
    ]},
    "Weisheit": {"domain": "🧠 Weisheit & Wissen", "color": "#4E79A7", "questions": [
        "Andere Menschen bitten mich oft um Rat",
        "Ich betrachte Situationen aus einer langfristigen Perspektive",
        "Meine Lebenserfahrung hilft mir bei schwierigen Entscheidungen",
        "Ich kann gut zwischen Wichtigem und Unwichtigem unterscheiden"
    ]},
    "Tapferkeit": {"domain": "💪 Mut", "color": "#F28E2B", "questions": [
        "Ich stehe für meine Überzeugungen ein, auch gegen Widerstand",
        "Angst hält mich nicht davon ab, das Richtige zu tun",
        "Ich konfrontiere schwierige Situationen direkt",
        "Bei Bedrohungen bewahre ich die Ruhe"
    ]},
    "Ausdauer": {"domain": "💪 Mut", "color": "#F28E2B", "questions": [
        "Ich gebe nicht auf, auch wenn Aufgaben schwierig werden",
        "Langfristige Projekte halte ich konsequent durch",
        "Rückschläge motivieren mich, es weiter zu versuchen",
        "Ich erledige Aufgaben stets bis zum Ende"
    ]},
    "Authentizität": {"domain": "💪 Mut", "color": "#F28E2B", "questions": [
        "Ich bin immer ich selbst, egal in welcher Situation",
        "Ich stehe zu meinen Werten und Prinzipien",
        "Meine Handlungen entsprechen meinen Überzeugungen",
        "Ich täusche nichts vor, um anderen zu gefallen"
    ]},
    "Enthusiasmus": {"domain": "💪 Mut", "color": "#F28E2B", "questions": [
        "Ich gehe Aufgaben mit großer Begeisterung an",
        "Meine Energie steckt oft andere an",
        "Ich betreibe Dinge mit vollem Einsatz",
        "Lebensfreude ist ein wichtiger Teil meines Wesens"
    ]},
    "Bindungsfähigkeit": {"domain": "🤝 Humanität", "color": "#E15759", "questions": [
        "Tiefe zwischenmenschliche Beziehungen sind mir wichtig",
        "Ich pflege enge Verbindungen zu meinen Liebsten",
        "Gegenseitiges Vertreuen ist die Basis meiner Beziehungen",
        "Ich investiere Zeit und Energie in meine wichtigsten Beziehungen"
    ]},
    "Freundlichkeit": {"domain": "🤝 Humanität", "color": "#E15759", "questions": [
        "Ich helfe anderen gerne ohne Gegenleistung",
        "Großzügigkeit macht mir Freude",
        "Ich bemerke, wenn andere Unterstützung brauchen",
        "Kleine Gefälligkeiten sind für mich selbstverständlich"
    ]},
    "Soziale Intelligenz": {"domain": "🤝 Humanität", "color": "#E15759", "questions": [
        "Ich erkenne schnell die Stimmungen anderer Menschen",
        "In sozialen Situationen weiß ich intuitiv, was angemessen ist",
        "Ich kann mich gut in andere hineinversetzen",
        "Zwischenmenschliche Dynamiken verstehe ich gut"
    ]},
    "Teamwork": {"domain": "⚖️ Gerechtigkeit", "color": "#76B7B2", "questions": [
        "In der Gruppe arbeite ich besonders effektiv",
        "Team-Erfolge sind mir wichtiger als Einzelleistungen",
        "Ich trage loyal zum Gruppenerfolg bei",
        "Gemeinsame Ziele motivieren mich besonders"
    ]},
    "Fairness": {"domain": "⚖️ Gerechtigkeit", "color": "#76B7B2", "questions": [
        "Ich behandle alle Menschen gleich, unabhängig von Herkunft oder Status",
        "Bei Entscheidungen lasse ich mich nicht von Sympathien leiten",
        "Gerechtigkeit ist mir ein wichtiges Anliegen",
        "Ich setze mich für faire Behandlung ein"
    ]},
    "Führungsvermögen": {"domain": "⚖️ Gerechtigkeit", "color": "#76B7B2", "questions": [
        "Ich kann Gruppen gut motivieren und leiten",
        "In Leitungsrollen fühle ich mich wohl",
        "Ich organisiere gerne Aktivitäten für Gruppen",
        "Andere folgen mir freiwillig"
    ]},
    "Vergebungsbereitschaft": {"domain": "🕊️ Mäßigung", "color": "#59A14F", "questions": [
        "Ich kann anderen leicht verzeihen",
        "Nach Konflikten gewähre ich eine zweite Chance",
        "Groll trage ich nicht lange mit mir herum",
        "Vergebung ist mir wichtiger als Rache"
    ]},
    "Bescheidenheit": {"domain": "🕊️ Mäßigung", "color": "#59A14F", "questions": [
        "Ich prahle nicht mit meinen Erfolgen",
        "Im Mittelpunkt stehen macht mir nichts aus",
        "Meine Fähigkeiten sprechen für sich selbst",
        "Ich sehe mich nicht als etwas Besonderes"
    ]},
    "Vorsicht": {"domain": "🕊️ Mäßigung", "color": "#59A14F", "questions": [
        "Ich überlege Konsequenzen, bevor ich handle",
        "Risiken schätze ich sorgfältig ab",
        "Impulsive Entscheidungen vermeide ich",
        "Sorgfältige Planung ist mir wichtig"
    ]},
    "Selbstregulation": {"domain": "🕊️ Mäßigung", "color": "#59A14F", "questions": [
        "Ich kann meine Gefühle gut kontrollieren",
        "Versuchungen widerstehe ich leicht",
        "Disziplin fällt mir nicht schwer",
        "Ich bleibe auch unter Stress gelassen"
    ]},
    "Sinn für das Schöne": {"domain": "✨ Spiritualität", "color": "#EDC948", "questions": [
        "Ich bewundere häufig Schönheit in Natur oder Kunst",
        "Ästhetische Erlebnisse berühren mich tief",
        "Ich nehme Schönheit im Alltag bewusst wahr",
        "Kunst, Musik oder Natur begeistern mich"
    ]},
    "Dankbarkeit": {"domain": "✨ Spiritualität", "color": "#EDC948", "questions": [
        "Ich bin dankbar für die guten Dinge in meinem Leben",
        "Oft halte ich inne, um meine Dankbarkeit auszudrücken",
        "Ich schätze bewusst, was ich habe",
        "Dankbarkeit ist ein täglicher Teil meines Lebens"
    ]},
    "Hoffnung": {"domain": "✨ Spiritualität", "color": "#EDC948", "questions": [
        "Ich blicke optimistisch in die Zukunft",
        "Auch in schwierigen Zeiten sehe ich Licht am Horizont",
        "Ich vertraue darauf, dass sich Dinge zum Guten wenden",
        "Positive Erwartungen prägen meine Haltung"
    ]},
    "Humor": {"domain": "✨ Spiritualität", "color": "#EDC948", "questions": [
        "Ich lache gerne und bringe andere zum Lachen",
        "Humor hilft mir in schwierigen Situationen",
        "Ich sehe oft die komische Seite des Lebens",
        "Spielerische Leichtigkeit ist mir wichtig"
    ]},
    "Spiritualität": {"domain": "✨ Spiritualität", "color": "#EDC948", "questions": [
        "Ich habe klare Überzeugungen über den Sinn des Lebens",
        "Spiritualität gibt mir Halt und Orientierung",
        "Ich denke über größere Zusammenhänge nach",
        "Mein Glaube beeinflusst mein Handeln"
    ]}
}

LIKERT_OPTIONS = {
    1: "Trifft nicht zu",
    2: "Trifft eher nicht zu", 
    3: "Neutral",
    4: "Trifft eher zu",
    5: "Trifft voll zu"
}

# ======================
# 🔢 Hilfsfunktionen
# ======================
def get_questions_for_version(version):
    mapping = {"short": 2, "medium": 3, "full": 4}
    limit = mapping.get(version, 3)
    questions = {
        s: {"domain": d["domain"], "color": d["color"], "questions": d["questions"][:limit]}
        for s, d in CHARACTER_STRENGTHS.items()
    }
    return questions

def get_randomized_question_list(questions):
    """Erstellt eine randomisierte Liste aller Fragen ohne Stärken-Namen"""
    all_questions = []
    for strength, data in questions.items():
        for i, question_text in enumerate(data["questions"]):
            all_questions.append({
                "strength": strength,
                "domain": data["domain"],
                "color": data["color"],
                "text": question_text,
                "id": f"{strength}_{i}"
            })
    
    # Zufällige Reihenfolge
    random.shuffle(all_questions)
    return all_questions

def calculate_results(responses):
    # Gruppiere Antworten nach Stärken
    strength_responses = {}
    for question_id, score in responses.items():
        strength_name = question_id.split("_")[0]  # Extrahiere Stärken-Namen aus ID
        if strength_name not in strength_responses:
            strength_responses[strength_name] = []
        strength_responses[strength_name].append(score)
    
    # Berechne Scores
    scores = {}
    for strength, answers in strength_responses.items():
        if answers:
            raw = sum(answers)
            max_possible = len(answers) * 5
            pct = (raw / max_possible) * 100 if max_possible > 0 else 0
            
            scores[strength] = {
                "score": pct,
                "domain": CHARACTER_STRENGTHS[strength]["domain"],
                "color": CHARACTER_STRENGTHS[strength]["color"],
                "raw_score": raw,
                "max_possible": max_possible,
                "question_count": len(answers)
            }
    
    # Relative Scores berechnen
    if scores:
        max_absolute = max(v["raw_score"] for v in scores.values())
        for strength in scores:
            if max_absolute > 0:
                scores[strength]["relative_score"] = (scores[strength]["raw_score"] / max_absolute) * 100
            else:
                scores[strength]["relative_score"] = 0
                
    return scores

def create_ranking_table(results):
    ranked = sorted(results.items(), key=lambda x: x[1]["relative_score"], reverse=True)
    data = []
    for rank, (strength, data_dict) in enumerate(ranked, 1):
        data.append({
            "Rang": rank,
            "Stärke": strength,
            "Wert": f"{data_dict['relative_score']:.0f}%",
            "Domäne": data_dict["domain"],
            "Rohpunktzahl": f"{data_dict['raw_score']}/{data_dict['max_possible']}",
            "Fragen": data_dict["question_count"]
        })
    return pd.DataFrame(data)

def plot_results(results):
    df = pd.DataFrame([{
        "Stärke": strength,
        "Wert": data["relative_score"],
        "Domäne": data["domain"]
    } for strength, data in results.items()])

    fig1 = px.bar(
        df.sort_values("Wert", ascending=True),
        x="Wert", y="Stärke",
        color="Domäne",
        color_discrete_map={
            "🧠 Weisheit & Wissen": "#4E79A7",
            "💪 Mut": "#F28E2B",
            "🤝 Humanität": "#E15759",
            "⚖️ Gerechtigkeit": "#76B7B2",
            "🕊️ Mäßigung": "#59A14F",
            "✨ Spiritualität": "#EDC948"
        },
        orientation="h",
        title="Charakterstärken - Ranking"
    )
    fig1.update_layout(
        showlegend=True,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=12)
    )

    domain_scores = df.groupby("Domäne")["Wert"].mean().reset_index()
    fig2 = px.pie(domain_scores, values="Wert", names="Domäne", hole=0.4,
                  color_discrete_map={
                      "🧠 Weisheit & Wissen": "#4E79A7",
                      "💪 Mut": "#F28E2B",
                      "🤝 Humanität": "#E15759",
                      "⚖️ Gerechtigkeit": "#76B7B2",
                      "🕊️ Mäßigung": "#59A14F",
                      "✨ Spiritualität": "#EDC948"
                  },
                  title="Durchschnittliche Ausprägung nach Domänen")
    
    # Spider Chart für Domänen
    fig3 = create_spider_chart(domain_scores)
    
    return fig1, fig2, fig3

def create_spider_chart(domain_scores):
    categories = domain_scores['Domäne'].tolist()
    values = domain_scores['Wert'].tolist()
    
    # Das Radar-Chart schließen, indem wir den ersten Punkt am Ende wiederholen
    categories = categories + [categories[0]]
    values = values + [values[0]]
    
    fig = go.Figure(data=
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            fillcolor='rgba(102, 126, 234, 0.3)',
            line=dict(color='#667eea', width=3),
            marker=dict(size=6, color='#764ba2')
        )
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10),
                gridcolor='lightgray'
            ),
            angularaxis=dict(
                tickfont=dict(size=11),
                rotation=90,
                direction="clockwise"
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        title="Charakterstärken-Profil nach Domänen",
        title_x=0.5,
        height=500,
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

# ==========================
# 🚀 Hauptfunktion
# ==========================
def main():
    # Haupt-Container mit weißem Hintergrund
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    # Header mit Farbverlauf
    st.markdown('<h1 class="main-header">🧠 VIA Charakterstärken Test</h1>', unsafe_allow_html=True)
    st.markdown('<h3 class="sub-header">Entdecke deine persönlichen Stärken</h3>', unsafe_allow_html=True)

    # Einleitungstext in schöner Box
    st.markdown("""
    <div class="info-box">
        <h3 style='color: white; margin-bottom: 1rem;'>📋 Test-Anleitung</h3>
        <p style='color: white; font-size: 1.1rem;'>
        Die folgenden Fragen beziehen sich auf Merkmale und Verhaltensweisen, die viele Menschen als positiv einschätzen. 
        Bitte beantworten Sie die Aussagen ehrlich und geben Sie an, in welchem Maß sie auf Sie persönlich zutreffen.
        </p>
        <p style='color: white; font-size: 1.1rem;'>
        Da der Fragebogen in drei unterschiedlichen Längen verfügbar ist, können Sie selbst entscheiden, welche Variante Sie bearbeiten möchten: 
        <strong>Kurz (48 Fragen)</strong>, <strong>Mittel (72 Fragen)</strong> oder <strong>Vollständig (96 Fragen)</strong>.
        </p>
        <p style='color: white; font-size: 1.1rem;'>
        Die vollständige Version liefert ein differenzierteres und umfassenderes Bild Ihrer Charakterstärken, nimmt jedoch etwas mehr Zeit in Anspruch.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar mit Premium Design
    with st.sidebar:
        st.markdown("""
        <div class="sidebar-box">
            <h3 style='color: white; text-align: center;'>⚙️ Test-Einstellungen</h3>
        </div>
        """, unsafe_allow_html=True)
        
        version = st.radio(
            "**Test-Version wählen:**",
            ["Kurz (48 Fragen)", "Mittel (72 Fragen)", "Vollständig (96 Fragen)"],
            index=1
        )
        
        version_key = {
            "Kurz (48 Fragen)": "short",
            "Mittel (72 Fragen)": "medium", 
            "Vollständig (96 Fragen)": "full"
        }[version]

        questions = get_questions_for_version(version_key)
        total_questions = sum(len(v["questions"]) for v in questions.values())
        
        # Metriken in schönen Boxen
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"""
            <div class="metric-box">
                <div style='font-size: 1.8rem; font-weight: bold; color: #667eea;'>{total_questions}</div>
                <div style='font-size: 0.9rem; color: #666;'>Fragen</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-box">
                <div style='font-size: 1.8rem; font-weight: bold; color: #667eea;'>{len(questions)}</div>
                <div style='font-size: 0.9rem; color: #666;'>Stärken</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Geschätzte Dauer
        estimated_minutes = (total_questions * 0.5) / 60
        st.markdown(f"""
        <div class="metric-box">
            <div style='font-size: 1.8rem; font-weight: bold; color: #667eea;'>{estimated_minutes:.1f}</div>
            <div style='font-size: 0.9rem; color: #666;'>Minuten Dauer</div>
        </div>
        """, unsafe_allow_html=True)

    # Session-State Management
    if "current_version" not in st.session_state:
        st.session_state.current_version = version_key
    
    if st.session_state.current_version != version_key:
        st.session_state.responses = {}
        st.session_state.randomized_questions = get_randomized_question_list(questions)
        st.session_state.current_version = version_key
    
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "randomized_questions" not in st.session_state:
        st.session_state.randomized_questions = get_randomized_question_list(questions)

    # Fragebogen Section
    st.markdown("---")
    st.markdown('<h2 class="sub-header">📝 Fragebogen</h2>', unsafe_allow_html=True)
    
    # Progress Bar mit Premium Design
    answered = sum(1 for response in st.session_state.responses.values() if response)
    
    if total_questions > 0:
        progress = answered / total_questions
        progress = max(0.0, min(1.0, progress))
    else:
        progress = 0.0

    st.markdown(f"""
    <div class="progress-container">
        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem;">
            <span style='font-size: 1.1rem;'><b>Fortschritt</b></span>
            <span style='font-size: 1.1rem;'><b>{answered}/{total_questions} beantwortet ({progress*100:.0f}%)</b></span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.progress(progress)

    # Fragen anzeigen mit Premium Design
    for i, q in enumerate(st.session_state.randomized_questions):
        if i < total_questions:
            st.markdown(f"""
            <div class="question-card">
                <h4 style='color: #2c3e50; margin-bottom: 1rem;'>Frage {i+1} von {total_questions}</h4>
                <p style='font-size: 1.2rem; color: #34495e; line-height: 1.6;'><b>{q["text"]}</b></p>
            </div>
            """, unsafe_allow_html=True)
            
            # Animierte Radio Buttons
            response = st.radio(
                "Wie sehr trifft diese Aussage auf Sie zu?",
                options=list(LIKERT_OPTIONS.keys()),
                format_func=lambda x: LIKERT_OPTIONS[x],
                key=q["id"],
                horizontal=True,
                index=(st.session_state.responses.get(q["id"], 0) - 1) if st.session_state.responses.get(q["id"]) else 0
            )
            
            if response:
                st.session_state.responses[q["id"]] = response
            
            st.markdown("---")

    # Ergebnisse Button mit Premium Design
    st.markdown("---")
    if st.button("🚀 **ERGEBNISSE ANALYSIEREN & ANZEIGEN**", type="primary"):
        if answered < total_questions:
            st.error(f"Bitte beantworte alle Fragen bevor du fortfährst. Noch {total_questions - answered} Fragen offen.")
        else:
            with st.spinner("🔍 Analysiere Ihre Charakterstärken..."):
                results = calculate_results(st.session_state.responses)
                ranking_df = create_ranking_table(results)
                fig1, fig2, fig3 = plot_results(results)

                # Erfolgsmeldung
                st.success("🎉 **Auswertung abgeschlossen!** Ihre persönlichen Charakterstärken wurden analysiert.")
                
                # Tabs mit Premium Design
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📊 **Rangliste**", 
                    "📈 **Visualisierungen**", 
                    "🕷️ **Stärken-Profil**", 
                    "💾 **Export**"
                ])

                with tab1:
                    st.dataframe(ranking_df, use_container_width=True, height=400)

                with tab2:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.plotly_chart(fig1, use_container_width=True)
                    with col2:
                        st.plotly_chart(fig2, use_container_width=True)

                with tab3:
                    st.plotly_chart(fig3, use_container_width=True)
                    st.info("💡 Das Spider-Diagramm zeigt Ihre durchschnittliche Ausprägung in den sechs Charakterstärken-Domänen.")

                with tab4:
                    csv_data = ranking_df.to_csv(index=False).encode("utf-8")
                    st.download_button(
                        "📥 **Ergebnisse als CSV herunterladen**",
                        data=csv_data,
                        file_name="via_charakterstaerken_ergebnisse.csv",
                        mime="text/csv"
                    )

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

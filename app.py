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
    layout="wide"
)

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
    # ... (alle anderen Stärken gleich wie vorher)
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
    
    # Zufällige Reihenfolge der Fragen pro Stärke
    randomized_questions = {}
    for strength, data in CHARACTER_STRENGTHS.items():
        questions = data["questions"][:limit]
        randomized_questions[strength] = {
            "domain": data["domain"],
            "color": data["color"], 
            "questions": questions
        }
    
    return randomized_questions

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
    fig1.update_layout(showlegend=True)

    domain_scores = df.groupby("Domäne")["Wert"].mean().reset_index()
    fig2 = px.pie(domain_scores, values="Wert", names="Domäne", hole=0.4,
                  title="Durchschnittliche Ausprägung nach Domänen")
    
    fig3 = create_spider_chart(domain_scores)
    
    return fig1, fig2, fig3

def create_spider_chart(domain_scores):
    categories = domain_scores['Domäne'].tolist()
    values = domain_scores['Wert'].tolist()
    
    categories = categories + [categories[0]]
    values = values + [values[0]]
    
    fig = go.Figure(data=
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            line=dict(color='royalblue', width=2)
        )
    )
    
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
        showlegend=False,
        title="Charakterstärken-Profil nach Domänen"
    )
    
    return fig

# ==========================
# 🚀 Hauptfunktion
# ==========================
def main():
    st.title("🧠 VIA Charakterstärken Test")
    st.markdown("### Entdecke deine persönlichen Stärken")

    # Sidebar
    st.sidebar.header("🔧 Einstellungen")
    version = st.sidebar.radio(
        "Test-Version wählen:",
        ["Kurz (48 Fragen)", "Mittel (72 Fragen)", "Vollständig (96 Fragen)"],
        index=1
    )

    version_key = {
        "Kurz (48 Fragen)": "short",
        "Mittel (72 Fragen)": "medium",
        "Vollständig (96 Fragen)": "full"
    }[version]

    # Initialisiere Session-State
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "questions_initialized" not in st.session_state:
        st.session_state.questions_initialized = False
    if "randomized_questions" not in st.session_state:
        st.session_state.randomized_questions = []

    # Fragen initialisieren
    if not st.session_state.questions_initialized:
        questions = get_questions_for_version(version_key)
        st.session_state.randomized_questions = get_randomized_question_list(questions)
        st.session_state.questions_initialized = True

    total_questions = len(st.session_state.randomized_questions)
    answered = len(st.session_state.responses)

    st.sidebar.write(f"**{total_questions} Fragen** insgesamt")
    st.sidebar.write(f"**{len(CHARACTER_STRENGTHS)} Charakterstärken**")
    st.sidebar.write(f"**{answered}/{total_questions} beantwortet**")

    # Fragebogen
    st.header("📝 Fragebogen")
    st.info("💡 Die Fragen werden in zufälliger Reihenfolge angezeigt, um beste Ergebnisse zu gewährleisten.")
    st.caption("Bitte beantworte alle Fragen ehrlich. 1 = Trifft nicht zu, 5 = Trifft voll zu.")

    # Fragen in randomisierter Reihenfolge anzeigen
    for i, q in enumerate(st.session_state.randomized_questions):
        st.subheader(f"Frage {i+1} von {total_questions}")
        
        response = st.radio(
            q["text"],
            options=list(LIKERT_OPTIONS.keys()),
            format_func=lambda x: LIKERT_OPTIONS[x],
            key=q["id"],
            horizontal=True,
            index=(st.session_state.responses.get(q["id"], 0) - 1) if st.session_state.responses.get(q["id"]) else 0
        )
        
        # Speichere Antwort
        if response:
            st.session_state.responses[q["id"]] = response

    # Fortschritt
    progress = answered / total_questions if total_questions > 0 else 0
    st.progress(progress)
    st.caption(f"Fortschritt: {answered}/{total_questions} beantwortet")

    # Ergebnisse
    if st.button("🚀 Ergebnisse berechnen", type="primary"):
        if answered < total_questions:
            st.error(f"Bitte beantworte alle Fragen bevor du fortfährst. Noch {total_questions - answered} Fragen offen.")
            return

        with st.spinner("Analysiere deine Charakterstärken..."):
            results = calculate_results(st.session_state.responses)
            
            st.balloons()
            st.success("🎉 Auswertung abgeschlossen! Hier sind deine persönlichen Charakterstärken:")
            
            ranking_df = create_ranking_table(results)
            fig1, fig2, fig3 = plot_results(results)

            tab1, tab2, tab3, tab4 = st.tabs(["📊 Rangliste", "📈 Visualisierung", "🕷️ Profil", "💾 Export"])

            with tab1:
                st.dataframe(ranking_df, use_container_width=True)
                
                # Top-Stärken hervorheben
                st.subheader("🎯 Deine Top-Stärken")
                top_3 = ranking_df.head(3)
                for idx, row in top_3.iterrows():
                    st.info(f"**{row['Rang']}. {row['Stärke']}** ({row['Domäne']}) - {row['Wert']}")

            with tab2:
                col1, col2 = st.columns(2)
                with col1:
                    st.plotly_chart(fig1, use_container_width=True)
                with col2:
                    st.plotly_chart(fig2, use_container_width=True)

            with tab3:
                st.plotly_chart(fig3, use_container_width=True)
                st.info("💡 Das Spider-Diagramm zeigt deine durchschnittliche Ausprägung in den sechs Charakterstärken-Domänen.")

            with tab4:
                csv_data = ranking_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Ergebnisse als CSV herunterladen",
                    data=csv_data,
                    file_name="via_charakterstaerken_ergebnisse.csv",
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()

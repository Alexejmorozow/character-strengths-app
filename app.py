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
    fig1.update_layout(showlegend=True)

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
            fillcolor='rgba(100, 149, 237, 0.3)',
            line=dict(color='royalblue', width=2),
            marker=dict(size=4)
        )
    )
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=10)
            ),
            angularaxis=dict(
                tickfont=dict(size=11),
                rotation=90,
                direction="clockwise"
            )
        ),
        showlegend=False,
        title="Charakterstärken-Profil nach Domänen",
        title_x=0.5,
        height=500
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

    questions = get_questions_for_version(version_key)
    total_questions = sum(len(v["questions"]) for v in questions.values())

    st.sidebar.write(f"**{total_questions} Fragen** insgesamt")
    st.sidebar.write(f"**{len(questions)} Charakterstärken**")

    # Initialisiere Session-State mit Version-Tracking
    if "current_version" not in st.session_state:
        st.session_state.current_version = version_key
    
    # Wenn Version geändert wurde, reset die Fragen und Antworten
    if st.session_state.current_version != version_key:
        st.session_state.responses = {}
        st.session_state.randomized_questions = get_randomized_question_list(questions)
        st.session_state.current_version = version_key
    
    # Initialisiere falls nicht vorhanden
    if "responses" not in st.session_state:
        st.session_state.responses = {}
    if "randomized_questions" not in st.session_state:
        st.session_state.randomized_questions = get_randomized_question_list(questions)

    st.header("📝 Fragebogen")
    st.info("💡 Die Fragen werden in zufälliger Reihenfolge angezeigt, um beste Ergebnisse zu gewährleisten.")
    st.caption("Bitte beantworte alle Fragen ehrlich. 1 = Trifft nicht zu, 5 = Trifft voll zu.")

    # Fragen in randomisierter Reihenfolge anzeigen
    answered = 0
    for i, q in enumerate(st.session_state.randomized_questions):
        # Nur anzeigen wenn wir innerhalb der aktuellen Fragenanzahl sind
        if i < total_questions:
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
                answered += 1

    # Fortschritt - BEREINIGT
    if total_questions > 0:
        progress = answered / total_questions
        # Sicherstellen, dass progress zwischen 0 und 1 liegt
        progress = max(0.0, min(1.0, progress))
    else:
        progress = 0.0

    st.progress(progress)
    st.caption(f"Fortschritt: {answered}/{total_questions} beantwortet")

    # Ergebnisberechnung
    if st.button("🚀 Ergebnisse berechnen", type="primary"):
        if answered < total_questions:
            st.error(f"Bitte beantworte alle Fragen bevor du fortfährst. Noch {total_questions - answered} Fragen offen.")
            return

        with st.spinner("Berechne Ergebnisse..."):
            results = calculate_results(st.session_state.responses)
            ranking_df = create_ranking_table(results)
            fig1, fig2, fig3 = plot_results(results)

            tab1, tab2, tab3, tab4 = st.tabs(["📊 Rangliste", "📈 Visualisierung", "🕷️ Spider-Diagramm", "💾 Export"])

            with tab1:
                st.dataframe(ranking_df, use_container_width=True)

            with tab2:
                c1, c2 = st.columns(2)
                with c1:
                    st.plotly_chart(fig1, use_container_width=True)
                with c2:
                    st.plotly_chart(fig2, use_container_width=True)

            with tab3:
                st.plotly_chart(fig3, use_container_width=True)
                st.info("💡 Das Spider-Diagramm zeigt Ihre durchschnittliche Ausprägung in den sechs Charakterstärken-Domänen.")

            with tab4:
                csv_data = ranking_df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "📥 Ergebnisse als CSV herunterladen",
                    data=csv_data,
                    file_name="via_charakterstaerken_ergebnisse.csv",
                    mime="text/csv"
                )

            st.success("🎉 Auswertung abgeschlossen! Deine Charakterstärken wurden erfolgreich analysiert.")

if __name__ == "__main__":
    main()

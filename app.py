import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from collections import defaultdict
import math

# Konfiguration
st.set_page_config(
    page_title="VIA Charakterstärken Test",
    page_icon="🧠",
    layout="wide"
)

# Daten der Charakterstärken mit Farben und Domänen
CHARACTER_STRENGTHS = {
    "Liebe zum Lernen": {
        "domain": "🧠 Weisheit & Wissen",
        "color": "#4E79A7",
        "questions": [
            "Ich lese regelmäßig Bücher oder Artikel, um Neues zu lernen",
            "Neue Themen wecken sofort mein Interesse",
            "Ich besuche häufig Kurse oder Workshops aus Interesse am Thema",
            "Das Gefühl, etwas dazugelernt zu haben, bereitet mir Freude"
        ]
    },
    "Urteilsvermögen": {
        "domain": "🧠 Weisheit & Wissen",
        "color": "#4E79A7",
        "questions": [
            "Ich hinterfrage Informationen, bevor ich sie akzeptiere",
            "Bei Entscheidungen wäge ich verschiedene Perspektiven ab",
            "Ich ändere meine Meinung, wenn neue Fakten vorliegen",
            "Komplexe Probleme analysiere ich gründlich"
        ]
    },
    "Neugier": {
        "domain": "🧠 Weisheit & Wissen",
        "color": "#4E79A7",
        "questions": [
            "Ich stelle oft Fragen, um Dinge besser zu verstehen",
            "Unbekannte Orte und Aktivitäten reizen mich",
            "Ich erkunde gerne neue Ideen und Konzepte",
            "Alltägliche Dinge betrachte ich oft mit Staunen"
        ]
    },
    "Kreativität": {
        "domain": "🧠 Weisheit & Wissen",
        "color": "#4E79A7",
        "questions": [
            "Ich habe oft originelle und einfallsreiche Ideen",
            "Ich suche nach neuen Wegen, um Aufgaben zu erledigen",
            "Kreative Lösungen machen mir besondere Freude",
            "Ich denke gerne über unkonventionelle Ansätze nach"
        ]
    },
    "Weisheit": {
        "domain": "🧠 Weisheit & Wissen",
        "color": "#4E79A7",
        "questions": [
            "Andere Menschen bitten mich oft um Rat",
            "Ich betrachte Situationen aus einer langfristigen Perspektive",
            "Meine Lebenserfahrung hilft mir bei schwierigen Entscheidungen",
            "Ich kann gut zwischen Wichtigem und Unwichtigem unterscheiden"
        ]
    },
    "Tapferkeit": {
        "domain": "💪 Mut",
        "color": "#F28E2B",
        "questions": [
            "Ich stehe für meine Überzeugungen ein, auch gegen Widerstand",
            "Angst hält mich nicht davon ab, das Richtige zu tun",
            "Ich konfrontiere schwierige Situationen direkt",
            "Bei Bedrohungen bewahre ich die Ruhe"
        ]
    },
    "Ausdauer": {
        "domain": "💪 Mut",
        "color": "#F28E2B",
        "questions": [
            "Ich gebe nicht auf, auch wenn Aufgaben schwierig werden",
            "Langfristige Projekte halte ich konsequent durch",
            "Rückschläge motivieren mich, es weiter zu versuchen",
            "Ich erledige Aufgaben stets bis zum Ende"
        ]
    },
    "Authentizität": {
        "domain": "💪 Mut",
        "color": "#F28E2B",
        "questions": [
            "Ich bin immer ich selbst, egal in welcher Situation",
            "Ich stehe zu meinen Werten und Prinzipien",
            "Meine Handlungen entsprechen meinen Überzeugungen",
            "Ich täusche nichts vor, um anderen zu gefallen"
        ]
    },
    "Enthusiasmus": {
        "domain": "💪 Mut",
        "color": "#F28E2B",
        "questions": [
            "Ich gehe Aufgaben mit großer Begeisterung an",
            "Meine Energie steckt oft andere an",
            "Ich betreibe Dinge mit vollem Einsatz",
            "Lebensfreude ist ein wichtiger Teil meines Wesens"
        ]
    },
    "Bindungsfähigkeit": {
        "domain": "🤝 Humanität",
        "color": "#E15759",
        "questions": [
            "Tiefe zwischenmenschliche Beziehungen sind mir wichtig",
            "Ich pflege enge Verbindungen zu meinen Liebsten",
            "Gegenseitiges Vertrauen ist die Basis meiner Beziehungen",
            "Ich investiere Zeit und Energie in meine wichtigsten Beziehungen"
        ]
    },
    "Freundlichkeit": {
        "domain": "🤝 Humanität",
        "color": "#E15759",
        "questions": [
            "Ich helfe anderen gerne ohne Gegenleistung",
            "Großzügigkeit macht mir Freude",
            "Ich bemerke, wenn andere Unterstützung brauchen",
            "Kleine Gefälligkeiten sind für mich selbstverständlich"
        ]
    },
    "Soziale Intelligenz": {
        "domain": "🤝 Humanität",
        "color": "#E15759",
        "questions": [
            "Ich erkenne schnell die Stimmungen anderer Menschen",
            "In sozialen Situationen weiß ich intuitiv, was angemessen ist",
            "Ich kann mich gut in andere hineinversetzen",
            "Zwischenmenschliche Dynamiken verstehe ich gut"
        ]
    },
    "Teamwork": {
        "domain": "⚖️ Gerechtigkeit",
        "color": "#76B7B2",
        "questions": [
            "In der Gruppe arbeite ich besonders effektiv",
            "Team-Erfolge sind mir wichtiger als Einzelleistungen",
            "Ich trage loyal zum Gruppenerfolg bei",
            "Gemeinsame Ziele motivieren mich besonders"
        ]
    },
    "Fairness": {
        "domain": "⚖️ Gerechtigkeit",
        "color": "#76B7B2",
        "questions": [
            "Ich behandle alle Menschen gleich, unabhängig von Herkunft oder Status",
            "Bei Entscheidungen lasse ich mich nicht von Sympathien leiten",
            "Gerechtigkeit ist mir ein wichtiges Anliegen",
            "Ich setze mich für faire Behandlung ein"
        ]
    },
    "Führungsvermögen": {
        "domain": "⚖️ Gerechtigkeit",
        "color": "#76B7B2",
        "questions": [
            "Ich kann Gruppen gut motivieren und leiten",
            "In Leitungsrollen fühle ich mich wohl",
            "Ich organisiere gerne Aktivitäten für Gruppen",
            "Andere folgen mir freiwillig"
        ]
    },
    "Vergebungsbereitschaft": {
        "domain": "🕊️ Mäßigung",
        "color": "#59A14F",
        "questions": [
            "Ich kann anderen leicht verzeihen",
            "Nach Konflikten gewähre ich eine zweite Chance",
            "Groll trage ich nicht lange mit mir herum",
            "Vergebung ist mir wichtiger als Rache"
        ]
    },
    "Bescheidenheit": {
        "domain": "🕊️ Mäßigung",
        "color": "#59A14F",
        "questions": [
            "Ich prahle nicht mit meinen Erfolgen",
            "Im Mittelpunkt stehen macht mir nichts aus",
            "Meine Fähigkeiten sprechen für sich selbst",
            "Ich sehe mich nicht als etwas Besonderes"
        ]
    },
    "Vorsicht": {
        "domain": "🕊️ Mäßigung",
        "color": "#59A14F",
        "questions": [
            "Ich überlege Konsequenzen, bevor ich handle",
            "Risiken schätze ich sorgfältig ab",
            "Impulsive Entscheidungen vermeide ich",
            "Sorgfältige Planung ist mir wichtig"
        ]
    },
    "Selbstregulation": {
        "domain": "🕊️ Mäßigung",
        "color": "#59A14F",
        "questions": [
            "Ich kann meine Gefühle gut kontrollieren",
            "Versuchungen widerstehe ich leicht",
            "Disziplin fällt mir nicht schwer",
            "Ich bleibe auch unter Stress gelassen"
        ]
    },
    "Sinn für das Schöne": {
        "domain": "✨ Spiritualität",
        "color": "#EDC948",
        "questions": [
            "Ich bewundere häufig Schönheit in Natur oder Kunst",
            "Ästhetische Erlebnisse berühren mich tief",
            "Ich nehme Schönheit im Alltag bewusst wahr",
            "Kunst, Musik oder Natur begeistern mich"
        ]
    },
    "Dankbarkeit": {
        "domain": "✨ Spiritualität",
        "color": "#EDC948",
        "questions": [
            "Ich bin dankbar für die guten Dinge in meinem Leben",
            "Oft halte ich inne, um meine Dankbarkeit auszudrücken",
            "Ich schätze bewusst, was ich habe",
            "Dankbarkeit ist ein täglicher Teil meines Lebens"
        ]
    },
    "Hoffnung": {
        "domain": "✨ Spiritualität",
        "color": "#EDC948",
        "questions": [
            "Ich blicke optimistisch in die Zukunft",
            "Auch in schwierigen Zeiten sehe ich Licht am Horizont",
            "Ich vertraue darauf, dass sich Dinge zum Guten wenden",
            "Positive Erwartungen prägen meine Haltung"
        ]
    },
    "Humor": {
        "domain": "✨ Spiritualität",
        "color": "#EDC948",
        "questions": [
            "Ich lache gerne und bringe andere zum Lachen",
            "Humor hilft mir in schwierigen Situationen",
            "Ich sehe oft die komische Seite des Lebens",
            "Spielerische Leichtigkeit ist mir wichtig"
        ]
    },
    "Spiritualität": {
        "domain": "✨ Spiritualität",
        "color": "#EDC948",
        "questions": [
            "Ich habe klare Überzeugungen über den Sinn des Lebens",
            "Spiritualität gibt mir Halt und Orientierung",
            "Ich denke über größere Zusammenhänge nach",
            "Mein Glaube beeinflusst mein Handeln"
        ]
    }
}

# Likert-Skala Optionen
LIKERT_OPTIONS = {
    1: "Trifft nicht zu",
    2: "Trifft eher nicht zu", 
    3: "Neutral",
    4: "Trifft eher zu",
    5: "Trifft voll zu"
}

def get_questions_for_version(version):
    """Gibt Fragen basierend auf der gewählten Version zurück"""
    questions = {}
    
    for strength, data in CHARACTER_STRENGTHS.items():
        if version == "short":
            questions[strength] = {
                "domain": data["domain"],
                "color": data["color"],
                "questions": data["questions"][:2]  # Nur erste 2 Fragen
            }
        elif version == "medium":
            questions[strength] = {
                "domain": data["domain"],
                "color": data["color"], 
                "questions": data["questions"][:3]  # Erste 3 Fragen
            }
        else:  # full
            questions[strength] = {
                "domain": data["domain"],
                "color": data["color"],
                "questions": data["questions"]  # Alle 4 Fragen
            }
    
    return questions

def calculate_results(responses):
    """Berechnet die Ergebnisse basierend auf den Antworten"""
    strength_scores = {}
    
    for strength, answers in responses.items():
        if answers:  # Nur wenn Antworten vorhanden
            raw_score = sum(answers.values())
            max_possible = len(answers) * 5
            percentage = (raw_score / max_possible) * 100
            
            strength_scores[strength] = {
                "score": percentage,
                "domain": CHARACTER_STRENGTHS[strength]["domain"],
                "color": CHARACTER_STRENGTHS[strength]["color"],
                "raw_score": raw_score,
                "max_possible": max_possible
            }
    
    # Ranking erstellen (höchste Punktzahl = 100%)
    if strength_scores:
        max_score = max(s["score"] for s in strength_scores.values())
        
        for strength in strength_scores:
            if max_score > 0:
                # Relative Prozentzahl berechnen (wie im Original)
                strength_scores[strength]["relative_score"] = (strength_scores[strength]["score"] / max_score) * 100
            else:
                strength_scores[strength]["relative_score"] = 0
    
    return strength_scores

def create_ranking_table(results):
    """Erstellt eine Rangliste der Stärken"""
    ranked_strengths = sorted(
        results.items(), 
        key=lambda x: x[1]["relative_score"], 
        reverse=True
    )
    
    ranking_data = []
    for rank, (strength, data) in enumerate(ranked_strengths, 1):
        ranking_data.append({
            "Rang": rank,
            "Stärke": strength,
            "Wert": f"{data['relative_score']:.0f}%",
            "Domäne": data["domain"],
            "Rohpunktzahl": f"{data['raw_score']}/{data['max_possible']}"
        })
    
    return pd.DataFrame(ranking_data)

def plot_results(results):
    """Erstellt Visualisierungen der Ergebnisse"""
    # Daten für Plot vorbereiten
    plot_data = []
    for strength, data in results.items():
        plot_data.append({
            "Stärke": strength,
            "Wert": data["relative_score"],
            "Domäne": data["domain"],
            "Farbe": data["color"]
        })
    
    df = pd.DataFrame(plot_data)
    
    # Balkendiagramm nach Stärken
    fig1 = px.bar(
        df.sort_values("Wert", ascending=True),
        x="Wert",
        y="Stärke",
        color="Domäne",
        color_discrete_map={
            "🧠 Weisheit & Wissen": "#4E79A7",
            "💪 Mut": "#F28E2B", 
            "🤝 Humanität": "#E15759",
            "⚖️ Gerechtigkeit": "#76B7B2",
            "🕊️ Mäßigung": "#59A14F",
            "✨ Spiritualität": "#EDC948"
        },
        title="Charakterstärken - Ranking",
        orientation="h"
    )
    fig1.update_layout(showlegend=True)
    
    # Domänen-Übersicht
    domain_scores = df.groupby("Domäne")["Wert"].mean().reset_index()
    fig2 = px.pie(
        domain_scores,
        values="Wert",
        names="Domäne",
        title="Durchschnittliche Ausprägung nach Domänen",
        color="Domäne",
        color_discrete_map={
            "🧠 Weisheit & Wissen": "#4E79A7",
            "💪 Mut": "#F28E2B",
            "🤝 Humanität": "#E15759", 
            "⚖️ Gerechtigkeit": "#76B7B2",
            "🕊️ Mäßigung": "#59A14F",
            "✨ Spiritualität": "#EDC948"
        }
    )
    
    return fig1, fig2

def main():
    st.title("🧠 VIA Charakterstärken Test")
    st.markdown("### Entdecke deine persönlichen Stärken")
    
    # Sidebar für Version-Auswahl
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
    
    st.sidebar.info(f"**{version}** - Basierend auf dem wissenschaftlichen VIA-Modell")
    
    # Fragen laden
    questions = get_questions_for_version(version_key)
    total_questions = sum(len(data["questions"]) for data in questions.values())
    
    st.sidebar.write(f"**{total_questions} Fragen** insgesamt")
    st.sidebar.write(f"**{len(questions)} Charakterstärken**")
    
    # Fragebogen
    st.header("📝 Fragebogen")
    st.write("Bitte beantworte die folgenden Fragen auf einer Skala von 1-5:")
    
    responses = {}
    progress_bar = st.progress(0)
    question_count = 0
    
    for strength, data in questions.items():
        st.subheader(f"**{strength}**")
        st.caption(f"Domäne: {data['domain']}")
        
        strength_responses = {}
        for i, question in enumerate(data["questions"]):
            question_count += 1
            progress = question_count / total_questions
            progress_bar.progress(progress)
            
            col1, col2 = st.columns([3, 2])
            with col1:
                st.write(f"**{question}**")
            with col2:
                response = st.radio(
                    f"Antwort für: {question}",
                    options=list(LIKERT_OPTIONS.keys()),
                    format_func=lambda x: LIKERT_OPTIONS[x],
                    key=f"{strength}_{i}",
                    horizontal=True
                )
                strength_responses[question] = response
        
        responses[strength] = strength_responses
    
    # Auswertung
    if st.button("🚀 Ergebnisse berechnen", type="primary"):
        if responses:
            with st.spinner("Berechne Ergebnisse..."):
                # Ergebnisse berechnen
                results = calculate_results(responses)
                
                # Ergebnisse anzeigen
                st.header("📊 Deine Ergebnisse")
                
                # Ranking Tabelle
                st.subheader("Rangliste deiner Charakterstärken")
                ranking_df = create_ranking_table(results)
                st.dataframe(ranking_df, use_container_width=True)
                
                # Visualisierungen
                col1, col2 = st.columns(2)
                
                with col1:
                    fig1, fig2 = plot_results(results)
                    st.plotly_chart(fig1, use_container_width=True)
                
                with col2:
                    st.plotly_chart(fig2, use_container_width=True)
                
                # Domänen-Übersicht
                st.subheader("🎯 Domänen-Übersicht")
                
                domains = {
                    "🧠 Weisheit & Wissen": ["Liebe zum Lernen", "Urteilsvermögen", "Neugier", "Kreativität", "Weisheit"],
                    "💪 Mut": ["Tapferkeit", "Ausdauer", "Authentizität", "Enthusiasmus"],
                    "🤝 Humanität": ["Bindungsfähigkeit", "Freundlichkeit", "Soziale Intelligenz"],
                    "⚖️ Gerechtigkeit": ["Teamwork", "Fairness", "Führungsvermögen"],
                    "🕊️ Mäßigung": ["Vergebungsbereitschaft", "Bescheidenheit", "Vorsicht", "Selbstregulation"],
                    "✨ Spiritualität": ["Sinn für das Schöne", "Dankbarkeit", "Hoffnung", "Humor", "Spiritualität"]
                }
                
                for domain, strengths in domains.items():
                    domain_score = sum(results.get(s, {}).get("relative_score", 0) for s in strengths) / len(strengths)
                    
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.metric(label=domain, value=f"{domain_score:.0f}%")
                    with col2:
                        st.progress(domain_score / 100)
                
                # Export Option
                st.subheader("💾 Ergebnisse exportieren")
                csv_data = ranking_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Ergebnisse als CSV herunterladen",
                    data=csv_data,
                    file_name="via_charakterstaerken_ergebnisse.csv",
                    mime="text/csv"
                )
                
                st.success("🎉 Auswertung abgeschlossen! Deine Charakterstärken wurden analysiert.")
        
        else:
            st.error("Bitte beantworte zunächst alle Fragen.")

if __name__ == "__main__":
    main()

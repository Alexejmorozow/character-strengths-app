import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
from fpdf import FPDF
import tempfile
import base64
from datetime import datetime
import io

# =====================
# 🔧 Grundkonfiguration
# =====================
st.set_page_config(
    page_title="VIA Charakterstärken Test",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS für besseres Design
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem !important;
        color: #2e86ab;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f8ff;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .progress-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .strength-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# 📚 Charakterstärken-Daten mit korrekten Domain-Namen
# =========================
CHARACTER_STRENGTHS = {
    "Liebe zum Lernen": {"domain": "Weisheit und Wissen", "color": "#4E79A7", "questions": [
        "Ich lese regelmäßig Bücher oder Artikel, um Neues zu lernen",
        "Neue Themen wecken sofort mein Interesse",
        "Ich besuche häufig Kurse oder Workshops aus Interesse am Thema",
        "Das Gefühl, etwas dazugelernt zu haben, bereitet mir Freude"
    ]},
    "Urteilsvermögen": {"domain": "Weisheit und Wissen", "color": "#4E79A7", "questions": [
        "Ich hinterfrage Informationen, bevor ich sie akzeptiere",
        "Bei Entscheidungen wäge ich verschiedene Perspektiven ab",
        "Ich ändere meine Meinung, wenn neue Fakten vorliegen",
        "Komplexe Probleme analysiere ich gründlich"
    ]},
    "Neugier": {"domain": "Weisheit und Wissen", "color": "#4E79A7", "questions": [
        "Ich stelle oft Fragen, um Dinge besser zu verstehen",
        "Unbekannte Orte und Aktivitäten reizen mich",
        "Ich erkunde gerne neue Ideen und Konzepte",
        "Alltägliche Dinge betrachte ich oft mit Staunen"
    ]},
    "Kreativität": {"domain": "Weisheit und Wissen", "color": "#4E79A7", "questions": [
        "Ich habe oft originelle und einfallsreiche Ideen",
        "Ich suche nach neuen Wegen, um Aufgaben zu erledigen",
        "Kreative Lösungen machen mir besondere Freude",
        "Ich denke gerne über unkonventionelle Ansätze nach"
    ]},
    "Weisheit": {"domain": "Weisheit und Wissen", "color": "#4E79A7", "questions": [
        "Andere Menschen bitten mich oft um Rat",
        "Ich betrachte Situationen aus einer langfristigen Perspektive",
        "Meine Lebenserfahrung hilft mir bei schwierigen Entscheidungen",
        "Ich kann gut zwischen Wichtigem und Unwichtigem unterscheiden"
    ]},
    "Tapferkeit": {"domain": "Mut", "color": "#F28E2B", "questions": [
        "Ich stehe für meine Überzeugungen ein, auch gegen Widerstand",
        "Angst hält mich nicht davon ab, das Richtige zu tun",
        "Ich konfrontiere schwierige Situationen direkt",
        "Bei Bedrohungen bewahre ich die Ruhe"
    ]},
    "Ausdauer": {"domain": "Mut", "color": "#F28E2B", "questions": [
        "Ich gebe nicht auf, auch wenn Aufgaben schwierig werden",
        "Langfristige Projekte halte ich konsequent durch",
        "Rückschläge motivieren mich, es weiter zu versuchen",
        "Ich erledige Aufgaben stets bis zum Ende"
    ]},
    "Authentizität": {"domain": "Mut", "color": "#F28E2B", "questions": [
        "Ich bin immer ich selbst, egal in welcher Situation",
        "Ich stehe zu meinen Werten und Prinzipien",
        "Meine Handlungen entsprechen meinen Überzeugungen",
        "Ich täusche nichts vor, um anderen zu gefallen"
    ]},
    "Enthusiasmus": {"domain": "Mut", "color": "#F28E2B", "questions": [
        "Ich gehe Aufgaben mit großer Begeisterung an",
        "Meine Energie steckt oft andere an",
        "Ich betreibe Dinge mit vollem Einsatz",
        "Lebensfreude ist ein wichtiger Teil meines Wesens"
    ]},
    "Bindungsfähigkeit": {"domain": "Menschlichkeit", "color": "#E15759", "questions": [
        "Tiefe zwischenmenschliche Beziehungen sind mir wichtig",
        "Ich pflege enge Verbindungen zu meinen Liebsten",
        "Gegenseitiges Vertreuen ist die Basis meiner Beziehungen",
        "Ich investiere Zeit und Energie in meine wichtigsten Beziehungen"
    ]},
    "Freundlichkeit": {"domain": "Menschlichkeit", "color": "#E15759", "questions": [
        "Ich helfe anderen gerne ohne Gegenleistung",
        "Großzügigkeit macht mir Freude",
        "Ich bemerke, wenn andere Unterstützung brauchen",
        "Kleine Gefälligkeiten sind für mich selbstverständlich"
    ]},
    "Soziale Intelligenz": {"domain": "Menschlichkeit", "color": "#E15759", "questions": [
        "Ich erkenne schnell die Stimmungen anderer Menschen",
        "In sozialen Situationen weiß ich intuitiv, was angemessen ist",
        "Ich kann mich gut in andere hineinversetzen",
        "Zwischenmenschliche Dynamiken verstehe ich gut"
    ]},
    "Teamwork": {"domain": "Gerechtigkeit", "color": "#76B7B2", "questions": [
        "In der Gruppe arbeite ich besonders effektiv",
        "Team-Erfolge sind mir wichtiger als Einzelleistungen",
        "Ich trage loyal zum Gruppenerfolg bei",
        "Gemeinsame Ziele motivieren mich besonders"
    ]},
    "Fairness": {"domain": "Gerechtigkeit", "color": "#76B7B2", "questions": [
        "Ich behandle alle Menschen gleich, unabhängig von Herkunft oder Status",
        "Bei Entscheidungen lasse ich mich nicht von Sympathien leiten",
        "Gerechtigkeit ist mir ein wichtiges Anliegen",
        "Ich setze mich für faire Behandlung ein"
    ]},
    "Führungsvermögen": {"domain": "Gerechtigkeit", "color": "#76B7B2", "questions": [
        "Ich kann Gruppen gut motivieren und leiten",
        "In Leitungsrollen fühle ich mich wohl",
        "Ich organisiere gerne Aktivitäten für Gruppen",
        "Andere folgen mir freiwillig"
    ]},
    "Vergebungsbereitschaft": {"domain": "Mässigung", "color": "#59A14F", "questions": [
        "Ich kann anderen leicht verzeihen",
        "Nach Konflikten gewähre ich eine zweite Chance",
        "Groll trage ich nicht lange mit mir herum",
        "Vergebung ist mir wichtiger als Rache"
    ]},
    "Bescheidenheit": {"domain": "Mässigung", "color": "#59A14F", "questions": [
        "Ich prahle nicht mit meinen Erfolgen",
        "Im Mittelpunkt stehen macht mir nichts aus",
        "Meine Fähigkeiten sprechen für sich selbst",
        "Ich sehe mich nicht als etwas Besonderes"
    ]},
    "Vorsicht": {"domain": "Mässigung", "color": "#59A14F", "questions": [
        "Ich überlege Konsequenzen, bevor ich handle",
        "Risiken schätze ich sorgfältig ab",
        "Impulsive Entscheidungen vermeide ich",
        "Sorgfältige Planung ist mir wichtig"
    ]},
    "Selbstregulation": {"domain": "Mässigung", "color": "#59A14F", "questions": [
        "Ich kann meine Gefühle gut kontrollieren",
        "Versuchungen widerstehe ich leicht",
        "Disziplin fällt mir nicht schwer",
        "Ich bleibe auch unter Stress gelassen"
    ]},
    "Sinn für das Schöne": {"domain": "Transzendenz", "color": "#EDC948", "questions": [
        "Ich bewundere häufig Schönheit in Natur oder Kunst",
        "Ästhetische Erlebnisse berühren mich tief",
        "Ich nehme Schönheit im Alltag bewusst wahr",
        "Kunst, Musik oder Natur begeistern mich"
    ]},
    "Dankbarkeit": {"domain": "Transzendenz", "color": "#EDC948", "questions": [
        "Ich bin dankbar für die guten Dinge in meinem Leben",
        "Oft halte ich inne, um meine Dankbarkeit auszudrücken",
        "Ich schätze bewusst, was ich habe",
        "Dankbarkeit ist ein täglicher Teil meines Lebens"
    ]},
    "Hoffnung": {"domain": "Transzendenz", "color": "#EDC948", "questions": [
        "Ich blicke optimistisch in die Zukunft",
        "Auch in schwierigen Zeiten sehe ich Licht am Horizont",
        "Ich vertraue darauf, dass sich Dinge zum Guten wenden",
        "Positive Erwartungen prägen meine Haltung"
    ]},
    "Humor": {"domain": "Transzendenz", "color": "#EDC948", "questions": [
        "Ich lache gerne und bringe andere zum Lachen",
        "Humor hilft mir in schwierigen Situationen",
        "Ich sehe oft die komische Seite des Lebens",
        "Spielerische Leichtigkeit ist mir wichtig"
    ]},
    "Spiritualität": {"domain": "Transzendenz", "color": "#EDC948", "questions": [
        "Ich habe klare Überzeugungen über den Sinn des Lebens",
        "Spiritualität gibt mir Halt und Orientierung",
        "Ich denke über größere Zusammenhänge nach",
        "Mein Glaube beeinflusst mein Handeln"
    ]}
}

# =========================
# 📖 BESCHREIBUNGSTEXTE aus dem VIA-Bericht (bereinigt für PDF)
# =========================
STRENGTH_DESCRIPTIONS = {
    "Kreativität": "Kreative Menschen produzieren staendig eine Vielzahl von verschiedenen originellen Ideen oder sie zeigen originelle Verhaltensweisen. Diese Ideen und Verhaltensweisen zeichnen sich nicht nur dadurch aus, dass sie innovativ und neu sind, sie muessen auch der Realitaet angepasst sein, damit sie dem Individuum im Leben nuetzlich sind und ihm weiterhelfen.",
    
    "Neugier": "Neugierige Menschen haben ein ausgepraegtes Interesse an neuen Erfahrungen. Sie sind sehr offen und flexibel bezueglich neuen, oft auch unerwarteten Situationen. Sie haben viele Interessen und finden an jeder Situation etwas Interessantes. Sie suchen aktiv nach Abwechslungen und Herausforderungen in ihrem taeglichen Leben.",
    
    "Urteilsvermögen": "Menschen mit einem stark ausgepraegten Urteilsvermoegen haben die Faehigkeit, Probleme und Gegebenheiten des Alltags aus unterschiedlichen Perspektiven zu betrachten und auf diese Weise Argumente fuer wichtige Entscheidungen zu entwickeln. Sie sind in der Lage, Informationen objektiv und kritisch zu beleuchten wobei sie sich an der Realitaet orientieren.",
    
    "Liebe zum Lernen": "Wissbegierige Menschen zeichnen sich durch eine grosse Begeisterung fuer das Lernen neuer Fertigkeiten und Wissensinhalte aus. Sie lieben es, neue Dinge zu lernen und sind bemueht, sich staendig weiterzubilden und zu entwickeln. Dabei wird das staendige Lernen als eine Herausforderung betrachtet.",
    
    "Weisheit": "Weise Menschen sind weitlaeufig und tiefsinnig. Sie haben einen guten Ueberblick und eine reife Sichtweise des Lebens. Ausserdem besitzen sie die Faehigkeit, eine sinnvolle Bilanz ueber das Leben ziehen zu koennen. Diese Koordination des geheimen Wissens und der gemachten Erfahrungen eines Menschen traegt zu seinem Wohlbefinden bei.",
    
    "Authentizität": "Authentische Menschen sind sich selbst und ihren Mitmenschen gegenueber aufrichtig und ehrlich. Sie halten ihre Versprechen und bleiben ihren Prinzipien treu. Sie legen Wert darauf, die Realitaet unverfaelscht wahrzunehmen. Authentizitaet befaehigt Menschen fuer sich selbst die Verantwortung zu uebernehmen.",
    
    "Tapferkeit": "Tapfere Menschen streben nach ihren Zielen und lassen sich dabei nicht von Schwierigkeiten und Hindernissen entmutigen. Tapferkeit kann sich in unterschiedlichen Lebensbereichen zeigen. Es handelt sich um die Faehigkeit, etwas Positives und Nuetzliches trotz drohenden Gefahren weiterzubringen.",
    
    "Ausdauer": "Ausdauer kennzeichnet Individuen, die alles zu Ende bringen wollen, was sie sich vorgenommen haben. Sie sind zielstrebig, geben nicht schnell auf, beenden was sie angefangen haben und lassen sich selten ablenken. Ausdauernde Menschen sind beharrlich - sie verfolgen aber nicht zwanghaft unerreichbare Ziele.",
    
    "Enthusiasmus": "Menschen mit einem ausgepraegten Tatendrang sind voller Energie und Lebensfreude und koennen sich fuer viele unterschiedliche Aktivitäten begeistern. Sie freuen sich auf jeden neuen Tag. Solche Menschen werden oft als energisch, flott, munter und schwungvoll beschrieben.",
    
    "Freundlichkeit": "Freundliche Menschen zeichnen sich dadurch aus, dass sie sehr nett, grosszuegig und hilfsbereit zu anderen Menschen sind. Sie machen anderen Personen gerne einen Gefallen, auch wenn sie diese nicht gut kennen. Sie lieben es, andere gluecklich zu machen.",
    
    "Bindungsfähigkeit": "Menschen mit einer sicheren Bindungsfaehigkeit zeichnen sich dadurch aus, dass sie anderen Menschen ihre Liebe zeigen koennen und auch in der Lage sind, Liebe von anderen anzunehmen. Bei dieser Staerke handelt es sich um die Faehigkeit enge Beziehungen und Freundschaften mit Mitmenschen aufzubauen.",
    
    "Soziale Intelligenz": "Menschen unterscheiden sich in der Faehigkeit, wichtige soziale Informationen, wie z.B. Gefuehle, wahrzunehmen und zu verarbeiten. Sozial kompetente Menschen kennen ihre eigenen Motive und Gefuehle. Sie kennen auch ihre eigenen Interessen und Faehigkeiten und sind in der Lage, sie zu foerdern.",
    
    "Teamwork": "Menschen mit dieser Staerke zeichnen sich durch ihre Teamfaehigkeit und Loyalitaet gegenueber ihrer Gruppe aus. Sie koennen dann am besten arbeiten, wenn sie Teil einer Gruppe sind. Die Gruppenzugehoerigkeit wird sehr hoch bewertet. Teamfaehige Menschen tragen oft eine soziale Verantwortung.",
    
    "Fairness": "Faire Menschen besitzen einen ausgepraegten Sinn fuer Gerechtigkeit und Gleichheit. Jede Person wird von ihnen gleich und fair behandelt, ungeachtet dessen, wer und was sie ist. Sie lassen sich in Entscheidungen nicht durch persoenliche Gefuehle beeinflussen und versuchen allen eine Chance zu geben.",
    
    "Führungsvermögen": "Menschen mit einem ausgepraegten Fuehrungsvermoegen besitzen die Faehigkeit, einer Gruppe trotz individueller Unterschiede eine gute Zusammenarbeit zu ermoeglichen. Ebenso zeichnen sie sich durch gute Planungs- und Organisationsfaehigkeiten von Gruppenaktivitaeten aus und dadurch, dass sie auch schwierige Entscheidungen treffen koennen.",
    
    "Vergebungsbereitschaft": "Menschen mit dieser Staerke sind eher in der Lage Vergangenes (z.B. zwischenmenschliche Konflikte) ruhen zu lassen und einen Neuanfang zu wagen. Sie koennen bis zu einem gewissen Punkt Verstaendnis aufbringen fuer die schlechte Behandlung durch andere Menschen und geben ihnen eine Chance zur Wiedergutmachung.",
    
    "Bescheidenheit": "Bescheidene Menschen zeichnen sich dadurch aus, dass sie nicht mit ihren Erfolgen prahlen. In der Menge fallen sie nicht gerne auf und wollen nicht die Aufmerksamkeit auf sich ziehen, sondern ziehen es vor, andere reden zu lassen. Bescheidene Menschen koennen eigene Fehler und Maengel zugeben.",
    
    "Vorsicht": "Vorsichtige Menschen treffen Entscheidungen sorgfaeltig, denken ueber moegliche Konsequenzen vor dem Sprechen und Handeln nach und koennen Recht von Unrecht unterscheiden. Sie vermeiden gefaehrliche koerperliche Aktivitaeten, was aber nicht heisst, dass sie neue Erfahrungen meiden.",
    
    "Selbstregulation": "Menschen mit ausgepraegter Selbstregulation bekunden keine Muehe, ihre Gefuehle und ihr Verhalten in entsprechenden Situationen zu kontrollieren, z.B. eine Diaet durchhalten, sich gesund ernaehren, regelmaessig trainieren, rechtzeitig Aufgaben erledigen. Sie zeichnen sich dadurch aus, dass sie laengerfristigen Erfolg dem kurzfristigen vorziehen.",
    
    "Sinn für das Schöne": "Menschen, die in verschiedenen Lebensbereichen (wie z.B. Musik, Kunst, Natur, Sport, Wissenschaft) Schoenes bewusst wahrnehmen, wertschaetzen und sich darueber freuen koennen, haben einen ausgepraegten Sinn fuer das Schoene. Sie nehmen im Alltag schoene Dinge wahr, die von anderen uebersehen oder nicht beachtet werden.",
    
    "Dankbarkeit": "Dankbare Menschen sind sich bewusst ueber die vielen guten Dinge in ihrem Leben, wissen diese zu schaetzen und nehmen sie nicht als selbstverstaendlich hin. Sie nehmen sich die Zeit, ihre Dankbarkeit Menschen gegenueber auszudruecken, z.B. wenn sie ein Geschenk bekommen.",
    
    "Hoffnung": "Hoffnungsvolle Menschen haben grundsaetzlich eine positive Einstellung gegenueber der Zukunft. Sie sind optimistisch und zuversichtlich und koennen auch dann etwas positiv noch sehen, wenn es fuer andere negativ erscheint. Sie hoffen das Beste fuer die Zukunft und tun ihr Moeglichstes, um ihre Ziele zu erreichen.",
    
    "Humor": "Humorvolle Menschen haben gerne und bringen andere Menschen gerne zum Laecheln oder zum Lachen. Sie versuchen ihre Freunde und Freundinnen aufzuheitern, wenn diese in einer bedrueckten Stimmung sind. Menschen mit einem ausgepraegten Sinn fuer Humor versuchen in allen moeglichen Situationen Spass zu haben.",
    
    "Spiritualität": "Spirituelle Menschen haben kohaerente Ueberzeugungen ueber den hoeheren Sinn und Zweck des Universums. Sie glauben an eine uebermaechtige Macht bzw. an einen Gott. Ihre religioesen Ueberzeugungen beeinflussen ihr Denken, Handeln und Fuehlen und koennen auch in schwierigen Zeiten eine Quelle des Trostes und der Kraft sein."
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
            "Weisheit und Wissen": "#4E79A7",
            "Mut": "#F28E2B",
            "Menschlichkeit": "#E15759",
            "Gerechtigkeit": "#76B7B2",
            "Mässigung": "#59A14F",
            "Transzendenz": "#EDC948"
        },
        orientation="h",
        title="Charakterstärken - Ranking"
    )
    fig1.update_layout(showlegend=True)

    domain_scores = df.groupby("Domäne")["Wert"].mean().reset_index()
    fig2 = px.pie(domain_scores, values="Wert", names="Domäne", hole=0.4,
                  color_discrete_map={
                      "Weisheit und Wissen": "#4E79A7",
                      "Mut": "#F28E2B",
                      "Menschlichkeit": "#E15759",
                      "Gerechtigkeit": "#76B7B2",
                      "Mässigung": "#59A14F",
                      "Transzendenz": "#EDC948"
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

# ======================
# 📄 PDF GENERIERUNG (komplett überarbeitet)
# ======================
class SimplePDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'VIA Charakterstaerken Bericht', 0, 1, 'C')
        self.ln(5)
    
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Seite {self.page_no()}', 0, 0, 'C')

def create_pdf_report(results, ranking_df):
    """Erstellt einen einfachen PDF-Bericht ohne komplexe Formatierung"""
    
    pdf = SimplePDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    # Titel
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, 'VIA Charakterstaerken Bericht', 0, 1, 'C')
    pdf.ln(10)
    
    # Einleitung
    pdf.set_font('Arial', '', 12)
    intro_text = (
        'Dieser Bericht basiert auf dem VIA-IS (Values in Action Inventory of Strengths), '
        'einem wissenschaftlichen Fragebogen zur Erfassung von 24 Charakterstaerken. '
        'Ihre persoenlichen Signaturstaerken sind diejenigen Charaktereigenschaften, '
        'die fuer Sie besonders zentral sind und deren Ausuebung Sie als erfuellend empfinden.'
    )
    pdf.multi_cell(0, 8, intro_text)
    pdf.ln(10)
    
    # Top 7 Stärken
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Ihre Top 7 Signaturstaerken', 0, 1)
    pdf.ln(5)
    
    top_7_strengths = ranking_df.head(7)
    
    for index, row in top_7_strengths.iterrows():
        strength_name = row['Stärke']
        rank = row['Rang']
        domain = row['Domäne']
        score = row['Wert']
        
        # Stärken-Header
        pdf.set_font('Arial', 'B', 12)
        pdf.cell(0, 8, f'{rank}. {strength_name} ({score})', 0, 1)
        pdf.set_font('Arial', 'I', 10)
        pdf.cell(0, 6, f'Domain: {domain}', 0, 1)
        
        # Beschreibung
        pdf.set_font('Arial', '', 10)
        description = STRENGTH_DESCRIPTIONS.get(strength_name, "Beschreibung nicht verfuegbar.")
        pdf.multi_cell(0, 6, description)
        pdf.ln(5)
    
    # Zusammenfassung
    pdf.add_page()
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, 'Zusammenfassung', 0, 1)
    pdf.ln(5)
    
    pdf.set_font('Arial', '', 12)
    summary_text = (
        'Ihre Signaturstaerken sind ein wertvolles Werkzeug fuer Ihre persoenliche Entwicklung. '
        'Nutzen Sie diese Staerken bewusst in verschiedenen Lebensbereichen:\n'
        '\n'
        '• Berufliche Entscheidungen, die zu Ihren Staerken passen\n'
        '• Herausforderungen mit Ihren natuerlichen Ressourcen bewältigen\n'
        '• Erfuellende Beziehungen gestalten\n'
        '• Mehr Sinn und Zufriedenheit im Alltag finden'
    )
    pdf.multi_cell(0, 8, summary_text)
    
    return pdf

def get_pdf_download_link(pdf, filename):
    """Erstellt einen Download-Link für das PDF"""
    try:
        # Verwende Bytes-IO anstatt direkte String-Konvertierung
        pdf_output = pdf.output()
        b64 = base64.b64encode(pdf_output).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📥 PDF Bericht herunterladen</a>'
        return href
    except Exception as e:
        # Fallback: Erstelle einen einfachen Error-Link
        error_msg = f"Fehler beim Erstellen des PDFs: {str(e)}"
        st.error(error_msg)
        return f'<a href="#" style="color: red;">❌ {error_msg}</a>'

# ==========================
# 🚀 Hauptfunktion
# ==========================
def main():
    st.title("🧠 VIA Charakterstärken Test")
    st.markdown("### Entdecke deine persönlichen Stärken")

    # Einleitungstext
    st.markdown("""
    Die folgenden Fragen beziehen sich auf Merkmale und Verhaltensweisen, die viele Menschen als positiv einschätzen. 
    Bitte beantworten Sie die Aussagen ehrlich und geben Sie an, in welchem Maß sie auf Sie persönlich zutreffen.

    Da der Fragebogen in drei unterschiedlichen Längen verfügbar ist, können Sie selbst entscheiden, welche Variante Sie bearbeiten möchten: 
    **Kurz (48 Fragen)**, **Mittel (72 Fragen)** oder **Vollständig (96 Fragen)**.

    Die vollständige Version liefert ein differenzierteres und umfassenderes Bild Ihrer Charakterstärken, nimmt jedoch etwas mehr Zeit in Anspruch.
    """)

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
    answered_questions = 0
    for i, q in enumerate(st.session_state.randomized_questions):
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
            
            if response:
                st.session_state.responses[q["id"]] = response
                answered_questions += 1

    # Fortschritt
    if total_questions > 0:
        progress = min(1.0, answered_questions / total_questions)
    else:
        progress = 0.0

    st.progress(progress)
    st.caption(f"Fortschritt: {answered_questions}/{total_questions} beantwortet")

    # Ergebnisberechnung
    if st.button("🚀 Ergebnisse berechnen", type="primary"):
        if answered_questions < total_questions:
            st.error(f"Bitte beantworte alle Fragen bevor du fortfährst. Noch {total_questions - answered_questions} Fragen offen.")
        else:
            with st.spinner("Berechne Ergebnisse..."):
                st.session_state.results = calculate_results(st.session_state.responses)
                st.session_state.ranking_df = create_ranking_table(st.session_state.results)
                st.session_state.fig1, st.session_state.fig2, st.session_state.fig3 = plot_results(st.session_state.results)
                st.success("🎉 Auswertung abgeschlossen! Deine Charakterstärken wurden erfolgreich analysiert.")

    # Ergebnisse anzeigen wenn berechnet
    if hasattr(st.session_state, 'results'):
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Rangliste", "📈 Visualisierung", "🕷️ Spider-Diagramm", "📄 PDF Bericht", "💾 Export"])

        with tab1:
            st.dataframe(st.session_state.ranking_df, use_container_width=True)

        with tab2:
            c1, c2 = st.columns(2)
            with c1:
                st.plotly_chart(st.session_state.fig1, use_container_width=True)
            with c2:
                st.plotly_chart(st.session_state.fig2, use_container_width=True)

        with tab3:
            st.plotly_chart(st.session_state.fig3, use_container_width=True)
            st.info("💡 Das Spider-Diagramm zeigt Ihre durchschnittliche Ausprägung in den sechs Charakterstärken-Domänen.")

        with tab4:
            st.header("📄 PDF Bericht erstellen")
            st.info("Erstellen Sie einen detaillierten Bericht mit Ihren Top 7 Signaturstärken basierend auf dem offiziellen VIA-Handbuch.")
            
            if st.button("📋 PDF Bericht generieren", type="primary", key="pdf_button"):
                with st.spinner("Erstelle PDF-Bericht..."):
                    try:
                        pdf = create_pdf_report(
                            st.session_state.results, 
                            st.session_state.ranking_df
                        )
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                        filename = f"VIA_Bericht_{timestamp}.pdf"
                        
                        st.markdown(
                            get_pdf_download_link(pdf, filename), 
                            unsafe_allow_html=True
                        )
                        st.success("✅ PDF Bericht erfolgreich generiert!")
                        
                    except Exception as e:
                        st.error(f"Fehler beim Erstellen des PDFs: {str(e)}")

        with tab5:
            csv_data = st.session_state.ranking_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Ergebnisse als CSV herunterladen",
                data=csv_data,
                file_name="via_charakterstaerken_ergebnisse.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    main()

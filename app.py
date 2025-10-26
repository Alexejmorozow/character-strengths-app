import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import random
import base64
from datetime import datetime
import io

# =====================
# 🔧 PDF GENERIERUNG mit ReportLab
# =====================
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

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
# 📖 BESCHREIBUNGSTEXTE aus dem VIA-Bericht (mit originalen Umlauten)
# =========================
STRENGTH_DESCRIPTIONS = {
    "Kreativität": "Kreative Menschen produzieren ständig eine Vielzahl von verschiedenen originellen Ideen oder sie zeigen originelle Verhaltensweisen. Diese Ideen und Verhaltensweisen zeichnen sich nicht nur dadurch aus, dass sie innovativ und neu sind, sie müssen auch der Realität angepasst sein, damit sie dem Individuum im Leben nützlich sind und ihm weiterhelfen.",
    
    "Neugier": "Neugierige Menschen haben ein ausgeprägtes Interesse an neuen Erfahrungen. Sie sind sehr offen und flexibel bezüglich neuen, oft auch unerwarteten Situationen. Sie haben viele Interessen und finden an jeder Situation etwas Interessantes. Sie suchen aktiv nach Abwechslungen und Herausforderungen in ihrem täglichen Leben.",
    
    "Urteilsvermögen": "Menschen mit einem stark ausgeprägten Urteilsvermögen haben die Fähigkeit, Probleme und Gegebenheiten des Alltags aus unterschiedlichen Perspektiven zu betrachten und auf diese Weise Argumente für wichtige Entscheidungen zu entwickeln. Sie sind in der Lage, Informationen objektiv und kritisch zu beleuchten wobei sie sich an der Realität orientieren.",
    
    "Liebe zum Lernen": "Wissbegierige Menschen zeichnen sich durch eine große Begeisterung für das Lernen neuer Fertigkeiten und Wissensinhalte aus. Sie lieben es, neue Dinge zu lernen und sind bemüht, sich ständig weiterzubilden und zu entwickeln. Dabei wird das ständige Lernen als eine Herausforderung betrachtet.",
    
    "Weisheit": "Weise Menschen sind weitsichtig und tiefsinnig. Sie haben einen guten Überblick und eine reife Sichtweise des Lebens. Ausserdem besitzen sie die Fähigkeit, eine sinnvolle Bilanz über das Leben ziehen zu können. Diese Koordination des gelernten Wissens und der gemachten Erfahrungen eines Menschen trägt zu seinem Wohlbefinden bei.",
    
    "Authentizität": "Authentische Menschen sind sich selbst und ihren Mitmenschen gegenüber aufrichtig und ehrlich. Sie halten ihre Versprechen und bleiben ihren Prinzipien treu. Sie legen Wert darauf, die Realität unverfälscht wahrzunehmen. Authentizität befähigt Menschen für sich selbst die Verantwortung zu übernehmen.",
    
    "Tapferkeit": "Tapfere Menschen streben nach ihren Zielen und lassen sich dabei nicht von Schwierigkeiten und Hindernissen entmutigen. Tapferkeit kann sich in unterschiedlichen Lebensbereichen zeigen. Es handelt sich um die Fähigkeit, etwas Positives und Nützliches trotz drohenden Gefahren weiterzubringen.",
    
    "Ausdauer": "Ausdauer kennzeichnet Individuen, die alles zu Ende bringen wollen, was sie sich vorgenommen haben. Sie sind zielstrebig, geben nicht schnell auf, beenden was sie angefangen haben und lassen sich selten ablenken. Ausdauernde Menschen sind beharrlich – sie verfolgen aber nicht zwanghaft unerreichbare Ziele.",
    
    "Enthusiasmus": "Menschen mit einem ausgeprägten Tatendrang sind voller Energie und Lebensfreude und können sich für viele unterschiedliche Aktivitäten begeistern. Sie freuen sich auf jeden neuen Tag. Solche Menschen werden oft als energisch, flott, munter und schwungvoll beschrieben.",
    
    "Freundlichkeit": "Freundliche Menschen zeichnen sich dadurch aus, dass sie sehr nett, großzügig und hilfsbereit zu anderen Menschen sind. Sie machen anderen Personen gerne einen Gefallen, auch wenn sie diese nicht gut kennen. Sie lieben es, andere glücklich zu machen.",
    
    "Bindungsfähigkeit": "Menschen mit einer sicheren Bindungsfähigkeit zeichnen sich dadurch aus, dass sie anderen Menschen ihre Liebe zeigen können und auch in der Lage sind, Liebe von anderen anzunehmen. Bei dieser Stärke handelt es sich um die Fähigkeit enge Beziehungen und Freundschaften mit Mitmenschen aufzubauen.",
    
    "Soziale Intelligenz": "Menschen unterscheiden sich in der Fähigkeit, wichtige soziale Informationen, wie z.B. Gefühle, wahrzunehmen und zu verarbeiten. Sozial kompetente Menschen kennen ihre eigenen Motive und Gefühle. Sie kennen auch ihre eigenen Interessen und Fähigkeiten und sind in der Lage, sie zu fördern.",
    
    "Teamwork": "Menschen mit dieser Stärke zeichnen sich durch ihre Teamfähigkeit und Loyalität gegenüber ihrer Gruppe aus. Sie können dann am besten arbeiten, wenn sie Teil einer Gruppe sind. Die Gruppenzugehörigkeit wird sehr hoch bewertet. Teamfähige Menschen tragen oft eine soziale Verantwortung.",
    
    "Fairness": "Faire Menschen besitzen einen ausgeprägten Sinn für Gerechtigkeit und Gleichheit. Jede Person wird von ihnen gleich und fair behandelt, ungeachtet dessen, wer und was sie ist. Sie lassen sich in Entscheidungen nicht durch persönliche Gefühle beeinflussen und versuchen allen eine Chance zu geben.",
    
    "Führungsvermögen": "Menschen mit einem ausgeprägten Führungsvermögen besitzen die Fähigkeit, einer Gruppe trotz individueller Unterschiede eine gute Zusammenarbeit zu ermöglichen. Ebenso zeichnen sie sich durch gute Planungs- und Organisationsfähigkeiten von Gruppenaktivitäten aus und dadurch, dass sie auch schwierige Entscheidungen treffen können.",
    
    "Vergebungsbereitschaft": "Menschen mit dieser Stärke sind eher in der Lage Vergangenes (z.B. zwischenmenschliche Konflikte) ruhen zu lassen und einen Neuanfang zu wagen. Sie können bis zu einem gewissen Punkt Verständnis aufbringen für die schlechte Behandlung durch andere Menschen und geben ihnen eine Chance zur Wiedergutmachung.",
    
    "Bescheidenheit": "Bescheidene Menschen zeichnen sich dadurch aus, dass sie nicht mit ihren Erfolgen prahlen. In der Menge fallen sie nicht gerne auf und wollen nicht die Aufmerksamkeit auf sich ziehen, sondern ziehen es vor, andere reden zu lassen. Bescheidene Menschen können eigene Fehler und Mängel zugeben.",
    
    "Vorsicht": "Vorsichtige Menschen treffen Entscheidungen sorgfältig, denken über mögliche Konsequenzen vor dem Sprechen und Handeln nach und können Recht von Unrecht unterscheiden. Sie vermeiden gefährliche körperliche Aktivitäten, was aber nicht heisst, dass sie neue Erfahrungen meiden.",
    
    "Selbstregulation": "Menschen mit ausgeprägter Selbstregulation bekunden keine Mühe, ihre Gefühle und ihr Verhalten in entsprechenden Situationen zu kontrollieren, z.B. eine Diät durchhalten, sich gesund ernähren, regelmässig trainieren, rechtzeitig Aufgaben erledigen. Sie zeichnen sich dadurch aus, dass sie längerfristigen Erfolg dem kurzfristigen vorziehen.",
    
    "Sinn für das Schöne": "Menschen, die in verschiedenen Lebensbereichen (wie z.B. Musik, Kunst, Natur, Sport, Wissenschaft) Schönes bewusst wahrnehmen, wertschätzen und sich darüber freuen können, haben einen ausgeprägten Sinn für das Schöne. Sie nehmen im Alltag schöne Dinge wahr, die von anderen übersehen oder nicht beachtet werden.",
    
    "Dankbarkeit": "Dankbare Menschen sind sich bewusst über die vielen guten Dinge in ihrem Leben, wissen diese zu schätzen und nehmen sie nicht als selbstverständlich hin. Sie nehmen sich die Zeit, ihre Dankbarkeit Menschen gegenüber auszudrücken, z.B. wenn sie ein Geschenk bekommen.",
    
    "Hoffnung": "Hoffnungsvolle Menschen haben grundsätzlich eine positive Einstellung gegenüber der Zukunft. Sie sind optimistisch und zuversichtlich und können auch dann etwas positiv noch sehen, wenn es für andere negativ erscheint. Sie hoffen das Beste für die Zukunft und tun ihr Möglichstes, um ihre Ziele zu erreichen.",
    
    "Humor": "Humorvolle Menschen lachen gerne und bringen andere Menschen gerne zum Lächeln oder zum Lachen. Sie versuchen ihre Freunde und Freundinnen aufzuheitern, wenn diese in einer bedrückten Stimmung sind. Menschen mit einem ausgeprägten Sinn für Humor versuchen in allen möglichen Situationen Spass zu haben.",
    
    "Spiritualität": "Spirituelle Menschen haben kohärente Überzeugungen über den höheren Sinn und Zweck des Universums. Sie glauben an eine übermächtige Macht bzw. an einen Gott. Ihre religiösen Überzeugungen beeinflussen ihr Denken, Handeln und Fühlen und können auch in schwierigen Zeiten eine Quelle des Trostes und der Kraft sein."
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
# 📄 PDF GENERIERUNG - Professionell nach VIA-Vorlage
# ======================
class ViaPDFTemplate(SimpleDocTemplate):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    def afterFlowable(self, flowable):
        """Wasserzeichen auf jeder Seite"""
        if hasattr(flowable, 'canvas'):
            canvas = flowable.canvas
            canvas.saveState()
            
            # Dezentes Wasserzeichen
            canvas.setFont('Helvetica-Oblique', 40)
            canvas.setFillColorRGB(0.9, 0.9, 0.95)  # Sehr helles Blau
            canvas.rotate(45)
            canvas.drawCentredString(300, 100, "VIA-IS")
            
            # Blaue Kopfzeile
            canvas.setFillColorRGB(0.12, 0.47, 0.71)  # VIA Blau
            canvas.rect(0, self.pagesize[1] - 30, self.pagesize[0], 30, fill=1)
            
            # Footer mit Copyright
            canvas.setFillColorRGB(0.4, 0.4, 0.4)
            canvas.setFont('Helvetica', 8)
            canvas.drawString(40, 20, f"© {datetime.now().year} VIA-IS Charakterstärken | Erstellt am: {datetime.now().strftime('%d.%m.%Y')}")
            canvas.drawRightString(self.pagesize[0] - 40, 20, f"Seite {self.page}")
            
            canvas.restoreState()

def create_professional_pdf_report(results, ranking_df):
    """Erstellt einen professionellen PDF-Bericht im VIA-Stil"""
    
    buffer = io.BytesIO()
    doc = ViaPDFTemplate(buffer, pagesize=A4, 
                        rightMargin=40, leftMargin=40, 
                        topMargin=60, bottomMargin=50)
    
    styles = getSampleStyleSheet()
    
    # Professionelle Styles im VIA-Stil
    styles.add(ParagraphStyle(
        name='ViaTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=24,
        alignment=1,
        textColor='#1f77b4',
        fontName='Helvetica-Bold'
    ))
    
    styles.add(ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=12,
        spaceBefore=20,
        textColor='#1f77b4',
        fontName='Helvetica-Bold',
        leftIndent=10,
        borderLeft=3,
        borderColor='#1f77b4',
        borderPadding=8
    ))
    
    styles.add(ParagraphStyle(
        name='StrengthHeader',
        parent=styles['Heading3'],
        fontSize=12,
        spaceAfter=6,
        spaceBefore=15,
        textColor='#2e86ab',
        fontName='Helvetica-Bold',
        backColor='#f0f8ff',
        borderPadding=6
    ))
    
    styles.add(ParagraphStyle(
        name='DomainStyle',
        parent=styles['Italic'],
        fontSize=10,
        spaceAfter=8,
        textColor='#666666'
    ))
    
    styles.add(ParagraphStyle(
        name='BodyEnhanced',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=8,
        leading=14
    ))
    
    styles.add(ParagraphStyle(
        name='HighlightBox',
        parent=styles['BodyText'],
        fontSize=10,
        backColor='#f8f9fa',
        borderColor='#1f77b4',
        borderWidth=1,
        borderPadding=12,
        spaceAfter=12,
        spaceBefore=12
    ))
    
    styles.add(ParagraphStyle(
        name='RankingItem',
        parent=styles['BodyText'],
        fontSize=10,
        leftIndent=0,
        spaceAfter=4,
        backColor='#ffffff'
    ))

    content = []
    
    # ===== TITELSEITE =====
    content.append(Paragraph('VIA-IS CHARAKTERSTÄRKEN BERICHT', styles['ViaTitle']))
    content.append(Spacer(1, 0.3*inch))
    
    # Untertitel
    content.append(Paragraph('Auswertung Ihrer persönlichen Stärken', styles['BodyEnhanced']))
    content.append(Spacer(1, 0.4*inch))
    
    # Erstellt am
    content.append(Paragraph(f'Erstellt am: {datetime.now().strftime("%d. %B %Y")}', styles['BodyEnhanced']))
    content.append(Spacer(1, 0.6*inch))
    
    # Einleitungstext im VIA-Stil
    intro_text = (
        'Dieser Bericht basiert auf dem VIA-IS (Values in Action Inventory of Strengths), '
        'einem wissenschaftlichen Fragebogen zur Erfassung von 24 Charakterstärken. '
        'Der VIA-IS wurde unter der Leitung der Psychologen Christopher Peterson und '
        'Martin Seligman entwickelt und wird seit 2004 international eingesetzt.'
    )
    content.append(Paragraph(intro_text, styles['BodyEnhanced']))
    content.append(Spacer(1, 0.3*inch))
    
    # Wichtiger Hinweis
    highlight_text = (
        'Ihre Signaturstärken (typischerweise die ersten 3-7 Stärken) sind jene '
        'Charaktereigenschaften, die für Sie besonders zentral sind und deren Ausübung '
        'Sie als besonders erfüllend empfinden.'
    )
    content.append(Paragraph(highlight_text, styles['HighlightBox']))
    
    content.append(PageBreak())
    
    # ===== RANGLISTE =====
    content.append(Paragraph('Rangliste Ihrer Charakterstärken', styles['SectionHeader']))
    content.append(Spacer(1, 0.2*inch))
    
    # Erklärender Text
    explanation = (
        'Die folgende Liste zeigt Ihre 24 Charakterstärken in der Reihenfolge ihrer Ausprägung. '
        'Die Rangreihenfolge beruht auf einem Vergleich mit Ihrer Normgruppe und dem '
        'Verhältnis Ihrer Stärken zueinander.'
    )
    content.append(Paragraph(explanation, styles['BodyEnhanced']))
    content.append(Spacer(1, 0.3*inch))
    
    # Top 10 Stärken als formatierte Liste
    top_strengths = ranking_df.head(10)
    for index, row in top_strengths.iterrows():
        rank = row['Rang']
        strength = row['Stärke']
        score = row['Wert']
        domain = row['Domäne']
        
        # Farbe basierend auf Rang für bessere Visualisierung
        if rank <= 3:
            rank_style = "<b>"
        elif rank <= 7:
            rank_style = ""
        else:
            rank_style = "<i>"
            
        strength_text = f'{rank_style}{rank}. {strength} - {score} (Domäne: {domain})'
        if rank <= 3:
            strength_text += "</b>"
        elif rank > 7:
            strength_text += "</i>"
            
        content.append(Paragraph(strength_text, styles['RankingItem']))
    
    content.append(Spacer(1, 0.3*inch))
    content.append(Paragraph('... und die weiteren Stärken', styles['BodyEnhanced']))
    
    # Restliche Stärken
    remaining_strengths = ranking_df.iloc[10:]
    for index, row in remaining_strengths.iterrows():
        strength_text = f"{row['Rang']}. {row['Stärke']} - {row['Wert']}"
        content.append(Paragraph(strength_text, styles['RankingItem']))
    
    content.append(PageBreak())
    
    # ===== DETAILIERTE TOP 7 STÄRKEN =====
    content.append(Paragraph('Ihre Top 7 Signaturstärken im Detail', styles['SectionHeader']))
    content.append(Spacer(1, 0.2*inch))
    
    intro_detail = (
        'Im Folgenden finden Sie detaillierte Beschreibungen Ihrer wichtigsten '
        'Signaturstärken basierend auf der wissenschaftlichen Forschung der '
        'Positiven Psychologie (Peterson & Seligman, 2004).'
    )
    content.append(Paragraph(intro_detail, styles['BodyEnhanced']))
    content.append(Spacer(1, 0.3*inch))
    
    top_7_strengths = ranking_df.head(7)
    for index, row in top_7_strengths.iterrows():
        strength_name = row['Stärke']
        rank = row['Rang']
        domain = row['Domäne']
        score = row['Wert']
        
        # Stärken-Header mit Rang und Domäne
        strength_header = f'{rank}. {strength_name} - {score}'
        content.append(Paragraph(strength_header, styles['StrengthHeader']))
        
        # Domäne
        domain_text = f'Domäne: {domain}'
        content.append(Paragraph(domain_text, styles['DomainStyle']))
        
        # Beschreibung
        description = STRENGTH_DESCRIPTIONS.get(strength_name, "Beschreibung nicht verfügbar.")
        content.append(Paragraph(description, styles['BodyEnhanced']))
        
        content.append(Spacer(1, 0.2*inch))
    
    content.append(PageBreak())
    
    # ===== INTERPRETATIONSHINWEISE =====
    content.append(Paragraph('Hinweise zur Interpretation', styles['SectionHeader']))
    content.append(Spacer(1, 0.2*inch))
    
    interpretation_texts = [
        "Ihre Rangreihenfolge spiegelt sowohl Ihre persönlichen Präferenzen als auch den Vergleich mit Ihrer Normgruppe wider.",
        "Signaturstärken (typischerweise Rang 1-7) sind jene Stärken, die Sie besonders charakterisieren und deren Ausübung Sie als erfüllend empfinden.",
        "Die Ausprägungen Ihrer Charakterstärken bleiben im Erwachsenenalter in der Regel relativ stabil.",
        "Niedrigere Ränge sind nicht als Schwächen zu interpretieren, sondern als weniger ausgeprägte Stärken.",
        "Die regelmäßige Anwendung Ihrer Signaturstärken kann zu mehr Zufriedenheit und Wohlbefinden führen."
    ]
    
    for text in interpretation_texts:
        content.append(Paragraph(f"• {text}", styles['BodyEnhanced']))
        content.append(Spacer(1, 0.1*inch))
    
    content.append(Spacer(1, 0.3*inch))
    
    # ===== LITERATURHINWEISE =====
    content.append(Paragraph('Wissenschaftliche Grundlage', styles['SectionHeader']))
    content.append(Spacer(1, 0.2*inch))
    
    literature_text = (
        'Dieser Bericht basiert auf der wissenschaftlichen Forschung der Positiven Psychologie. '
        'Weiterführende Informationen finden Sie unter: www.viacharacter.org'
    )
    content.append(Paragraph(literature_text, styles['BodyEnhanced']))
    
    references = [
        "Peterson, C. & Seligman, M.E.P. (2004). Character strengths and virtues: A handbook and classification. Oxford University Press.",
        "Ruch, W., Proyer, R. T., Harzer, C., Park, N., Peterson, C. & Seligman, M. E. (2010). Values in Action Inventory of Strengths (VIA-IS): Adaptation and validation of the German version. Journal of Individual Differences, 31(3), 138-149.",
        "Seligman, M. E. P. (2002). Authentic Happiness. Using the New Positive Psychology to Realize Your Potential for Lasting Fulfillment. Free Press."
    ]
    
    content.append(Spacer(1, 0.2*inch))
    for ref in references:
        content.append(Paragraph(f"• {ref}", styles['BodyEnhanced']))
        content.append(Spacer(1, 0.05*inch))
    
    # PDF erstellen
    doc.build(content)
    buffer.seek(0)
    return buffer

def get_pdf_download_link(pdf_buffer, filename):
    """Erstellt einen Download-Link für das PDF"""
    pdf_data = pdf_buffer.getvalue()
    b64 = base64.b64encode(pdf_data).decode()
    href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">📥 PDF Bericht herunterladen</a>'
    return href

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

    Der originale VIA-IS-Fragebogen umfasst **240 Fragen**. 
    In dieser Version wurde er verkürzt, um die Bearbeitungszeit zu reduzieren, ohne den inhaltlichen Schwerpunkt zu verändern. 

    Sie können selbst entscheiden, welche Variante Sie bearbeiten möchten: 
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
            st.info("Erstellen Sie einen professionellen Bericht im VIA-Stil mit wissenschaftlicher Fundierung.")
            
            if st.button("📋 Professionellen PDF Bericht generieren", type="primary", key="pdf_button"):
                with st.spinner("Erstelle professionellen PDF-Bericht..."):
                    try:
                        pdf_buffer = create_professional_pdf_report(
                            st.session_state.results, 
                            st.session_state.ranking_df
                        )
                        
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M")
                        filename = f"VIA_Bericht_{timestamp}.pdf"
                        
                        st.markdown(
                            get_pdf_download_link(pdf_buffer, filename), 
                            unsafe_allow_html=True
                        )
                        st.success("✅ Professioneller PDF Bericht erfolgreich generiert!")
                        
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

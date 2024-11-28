from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from django.http import HttpResponse
import io

def generate_questionnaire_pdf(questionnaire, domains, sous_domains, responses):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Title
    title = f"Rapport du questionnaire - {questionnaire.student.name}"
    story.append(Paragraph(title, styles['Heading1']))
    story.append(Spacer(1, 20))
    
    add_summary_section(story, styles, domains, sous_domains, responses, questionnaire)
    add_detailed_section(story, styles, domains, sous_domains, responses, questionnaire)
    
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def add_summary_section(story, styles, domains, sous_domains, responses, questionnaire):
    story.append(Paragraph("Résumé par domaine", styles['Heading2']))
    
    for domain in domains:
        data = [['Sous Domaine', '0', '1', '2', 'Total']]
        domain_total = 0
        
        for sous_domain in sous_domains.filter(domain=domain):
            domain_responses = responses.filter(question__sous_domain=sous_domain)
            scores = calculate_scores(domain_responses)
            data.append([
                sous_domain.name,
                str(scores['zeros']),
                str(scores['ones']),
                str(scores['twos']),
                str(scores['total'])
            ])
            domain_total += scores['total']
            
        data.append(['Total ' + domain.name, '', '', '', str(domain_total)])
        story.append(create_table(data))
        story.append(Spacer(1, 20))

def add_detailed_section(story, styles, domains, sous_domains, responses, questionnaire):
    story.append(Paragraph("Détail des réponses", styles['Heading2']))
    story.append(Spacer(1, 12))
    
    for domain in domains:
        story.append(Paragraph(domain.name, styles['Heading3']))
        
        for sous_domain in sous_domains.filter(domain=domain):
            story.append(Paragraph(sous_domain.name, styles['Heading4']))
            domain_responses = responses.filter(question__sous_domain=sous_domain)
            
            for answer in [0, 1, 2]:
                questions = domain_responses.filter(answer=answer)
                if questions.exists():
                    story.append(Paragraph(f"Réponses {answer}:", styles['Normal']))
                    for response in questions:
                        story.append(Paragraph(
                            f"• {response.question.text}", 
                            ParagraphStyle('bullet', leftIndent=20)
                        ))
            story.append(Spacer(1, 12))

def calculate_scores(responses):
    zeros = responses.filter(answer=0).count()
    ones = responses.filter(answer=1).count()
    twos = responses.filter(answer=2).count()
    total = (zeros * 0) + (ones * 1) + (twos * 2)
    return {'zeros': zeros, 'ones': ones, 'twos': twos, 'total': total}

def create_table(data):
    t = Table(data)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    return t
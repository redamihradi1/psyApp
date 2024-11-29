from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from .score_calculator import ScoreCalculator
import io

def generate_questionnaire_pdf(questionnaire, domains, sous_domains, responses):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    styles.add(ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        spaceAfter=30,
        textColor=HexColor('#2563EB')
    ))
    
    # Header
    title = f"Rapport d'Évaluation - {questionnaire.student.name}"
    story.append(Paragraph(title, styles['CustomTitle']))
    
    # Student Info
    info_data = [
        ['Élève:', questionnaire.student.name],
        ['Date de naissance:', questionnaire.student.date_of_birth.strftime('%d/%m/%Y') if questionnaire.student.date_of_birth else 'Non spécifié'],
        ['Date d\'évaluation:', questionnaire.created_at.strftime('%d/%m/%Y')],
        ['Parent:', questionnaire.parent.name]
    ]
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 12),
        ('TEXTCOLOR', (0,0), (0,-1), HexColor('#4B5563')),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 30))

    # Score Results Section
    story.append(Paragraph("Résultats des Scores", styles['Heading2']))
    story.append(Spacer(1, 20))
    
    # First Table - Detailed Results
    calculator = ScoreCalculator(questionnaire.student, questionnaire)
    resultat_final, deuxieme_tableau = calculator.calculate()
    
    headers = ['Domaine', 'Sous-Domaine', 'Score Brut', 'Âge Développé', '%ile', 'Niveau']
    result_data = [headers]
    for resultat in resultat_final:
        result_data.append([
            resultat['domaine'],
            resultat['label'],
            str(resultat['total']),
            resultat.get('age_developpe', '-'),
            resultat.get('percentile', '-'),
            resultat.get('niveau', '-')
        ])
    
    results_table = Table(result_data, repeatRows=1)
    results_table.setStyle(create_table_style())
    story.append(results_table)
    story.append(Spacer(1, 30))

    # Second Table - Domain Synthesis
    story.append(Paragraph("Synthèse par Domaine", styles['Heading2']))
    story.append(Spacer(1, 20))
    
    synth_headers = [
                    'Domaine', 'CVP', 'LE', 'LR', 'MF', 'MG', 'IOM', 
                    'EA', 'RS', 'CMC', 'CVC', 'Somme\nNS', '%ile', 
                    'Niveau\ndév.', 'Âge\nDév.'
                    ]
    
    synth_style = TableStyle([
                            ('FONTSIZE', (0, 0), (-1, 0), 8),  # Smaller header font
                            ('FONTSIZE', (0, 1), (-1, -1), 8),  # Smaller content font
                            ('WORDWRAP', (0, 0), (-1, -1), True),  # Enable word wrapping
                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                            ])
    synth_data = [synth_headers]
    for tableau in deuxieme_tableau:
        synth_data.append([
            tableau['domaine'],
            tableau.get('CVP', '-'),
            tableau.get('LE', '-'),
            tableau.get('LR', '-'),
            tableau.get('MF', '-'),
            tableau.get('MG', '-'),
            tableau.get('IOM', '-'),
            tableau.get('EA', '-'),
            tableau.get('RS', '-'),
            tableau.get('CMC', '-'),
            tableau.get('CVC', '-'),
            tableau.get('somme_ns', '0'),
            tableau.get('percentile', '-'),
            tableau.get('niveau', '-'),
            tableau.get('age_developpe', '-')
        ])
    
    col_widths = [
                    1.5*inch,  # Domaine
                    0.4*inch,  # CVP
                    0.4*inch,  # LE
                    0.4*inch,  # LR
                    0.4*inch,  # MF
                    0.4*inch,  # MG
                    0.4*inch,  # IOM
                    0.4*inch,  # EA
                    0.4*inch,  # RS
                    0.4*inch,  # CMC
                    0.4*inch,  # CVC
                    0.5*inch,  # Somme NS
                    0.4*inch,  # %ile
                    0.8*inch,  # Niveau
                    0.5*inch   # Âge Dév.
                ]
    synth_table = Table(synth_data, repeatRows=1, colWidths=col_widths, style=synth_style)
    # synth_table = Table(synth_data, repeatRows=1, colWidths=col_widths)
    # synth_table = Table(synth_data, repeatRows=1)
    synth_table.setStyle(create_table_style())
    story.append(synth_table)
    story.append(Spacer(1, 30))

    # Detailed Responses Section
    add_detailed_responses(story, styles, domains, sous_domains, responses)
    
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf

def create_table_style():
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#2563EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [HexColor('#F3F4F6'), colors.white]),
    ])

def add_detailed_responses(story, styles, domains, sous_domains, responses):
    story.append(Paragraph("Détail des Réponses par Domaine", styles['Heading2']))
    
    for domain in domains:
        story.append(Paragraph(domain.name, styles['Heading3']))
        
        for sous_domain in sous_domains.filter(domain=domain):
            story.append(Paragraph(sous_domain.name, styles['Heading4']))
            domain_responses = responses.filter(question__sous_domain=sous_domain)
            
            for answer in [0, 1, 2]:
                questions = domain_responses.filter(answer=answer)
                if questions.exists():
                    bullet_style = ParagraphStyle(
                        'BulletPoint',
                        parent=styles['Normal'],
                        leftIndent=20,
                        fontSize=9,
                        leading=12
                    )
                    story.append(Paragraph(f"Score {answer}:", styles['Normal']))
                    for response in questions:
                        story.append(Paragraph(f"• {response.question.text}", bullet_style))
            story.append(Spacer(1, 12))


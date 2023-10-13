from sqlalchemy import create_engine
import pandas as pd
import cx_Oracle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, AnchorFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
from datetime import datetime
import matplotlib.pyplot as plt

# Initialisation du client Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\app\client\ELLAIA\product\19.0.0\client_1\bin")

# Connexion à la base de données
engine = create_engine('oracle+cx_oracle://DAAMHAOUZ:DAAMHO2023uzA%@172.16.5.28:1521/TAYSSIRPROD')

# Requête SQL
query = """
SELECT d.LIBF_PROVINCE as "Province", d.LIBF_COMMUNE as "Commune", decode(mad.current_statut,'GENERE','NON ENCORE RETIRE','PAYE','RETIRE','VEROUILLE','EN COURS','','EN COURS') as "Etat", count(*) as "Nombre"
FROM pp_pay_mad mad, DETAIL_FICHIER_ALLER mi, douar_mi d
WHERE mad.cnie = mi.cin
AND mi.CODE_DOUAR_MI = d.ID_QUARTIER_DOUAR
AND mi.CODE_COMMUNE_MI = d.ID_COMMUNE
group by mad.current_statut, d.LIBF_PROVINCE, d.LIBF_COMMUNE
order by 1,2,3
"""

# Exécution de la requête et stockage des résultats dans un DataFrame
df = pd.read_sql(query, engine)

# Suppression des lignes où la colonne 'Province' ou 'Etat' contient None
df = df.dropna(subset=['Province', 'Etat'])

# Nom du fichier PDF avec un timestamp
pdf_file = f"Rapport_Etats_Paiements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
pdf = SimpleDocTemplate(pdf_file, pagesize=A4)

# Couleurs de la charte graphique
color1 = HexColor("#303e47")
color2 = HexColor("#618c19")

# Obtenez un ensemble de styles de paragraphe
styles = getSampleStyleSheet()

# Liste pour stocker les éléments du PDF
elements = []

# Titre du rapport
title_style = styles['Heading1']
title_style.alignment = 1  # 1 pour centré
title_style.fontName = 'Helvetica-Bold'
title_style.fontSize = 18
title_style.leading = 22  # Espace entre les lignes
title_style.textColor = color2  # Couleur du texte du titre
elements.append(Paragraph("Tableau de bord des états de paiement des aides par Province et par Commune", title_style))

# Ajout d'un espace vide
elements.append(Paragraph("<br/><br/>", None))

# Ajout d'un espace vide
elements.append(Paragraph("<br/><br/>", None))

# Obtention des provinces uniques
# ... (le début du script reste inchangé)

# Obtention des provinces uniques
provinces = df['Province'].unique()

# Génération des graphiques par province
for province in provinces:
    anchor_name = province.replace(" ", "_")
    elements.append(AnchorFlowable(anchor_name))
    elements.append(Paragraph(province, None))
    
    # Génération du graphique à barres pour la province actuelle
    sub_df = df[df['Province'] == province]
    etats = sub_df['Etat'].unique()
    nombres = [sub_df[sub_df['Etat'] == etat]['Nombre'].sum() for etat in etats]
    
    # Vérifiez si 'etats' ou 'nombres' contiennent une valeur None
    if None not in etats and None not in nombres:
        plt.figure(figsize=(10, 6))
        plt.bar(etats, nombres, color=['#303e47', '#618c19'])
        plt.xlabel('Etats de paiement')
        plt.ylabel('Nombre')
        plt.title(f'Etats de paiement pour la province {province}')
        
        # Sauvegarde du graphique dans un fichier temporaire
        plt.savefig(f"{province}_graph.png")
        
        # Ajout du graphique au PDF
        elements.append(Image(f"{province}_graph.png", 400, 250))
    else:
        print(f"Des valeurs None ont été trouvées pour la province {province}. Le graphique n'a pas été créé.")

# ... (le reste du script reste inchangé)

# Ajout d'un espace vide
elements.append(Paragraph("<br/><br/>", None))
# Ajout d'un espace vide
elements.append(Paragraph("<br/><br/>", None))



# Ajout de la phrase "La liste des provinces"
elements.append(Paragraph("La liste des provinces :", None))
# Liste des provinces pour créer des liens hypertextes
provinces = df['Province'].unique()
for province in provinces:
    anchor_name = province.replace(" ", "_")
    elements.append(Paragraph(f"<a href='#{anchor_name}'>{province}</a><br/>", None))




# Ajout d'un espace vide
elements.append(Paragraph("<br/><br/>", None))

# Génération des tableaux par province
for province in provinces:
    anchor_name = province.replace(" ", "_")
    elements.append(AnchorFlowable(anchor_name))
    elements.append(Paragraph(province, None))
    sub_df = df[df['Province'] == province]
    table_data = [['Commune', 'Etat', 'Nombre']]
    for index, row in sub_df.iterrows():
        table_data.append([row['Commune'], row['Etat'], row['Nombre']])
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), color1),  # Couleur de fond de l'en-tête
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Couleur du texte de l'en-tête
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alignement du texte
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Police de l'en-tête
        ('FONTSIZE', (0, 0), (-1, 0), 14),  # Taille de la police de l'en-tête
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Espacement en bas de l'en-tête
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),  # Couleur de fond du reste du tableau
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Grille
    ]))


    elements.append(table)
    elements.append(Paragraph("<br/><br/>", None))

# Génération du PDF
pdf.build(elements)

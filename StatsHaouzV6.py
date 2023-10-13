from sqlalchemy import create_engine
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, AnchorFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.colors import HexColor
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np
    
import cx_Oracle
cx_Oracle.init_oracle_client(lib_dir=r"C:\app\client\ELLAIA\product\19.0.0\client_1\bin")

def main():
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
    
    
    color1 = "#303e47"
    color2 = "#618c19"
    
    # Préparation des données pour le graphique
    grouped_df = df.groupby(['Province', 'Etat'])['Nombre'].sum().reset_index()
    
    # Liste unique des provinces et des états
    unique_provinces = grouped_df['Province'].unique()
    unique_etats = grouped_df['Etat'].unique()
    
    # Initialisation des variables pour le graphique
    barWidth = 0.4
    r1 = list(range(len(unique_provinces)))
    
    plt.figure(figsize=(15, 8))
    
    # Génération des barres pour chaque état
    for idx, etat in enumerate(unique_etats):
        values = []
        for province in unique_provinces:
            value = grouped_df.loc[(grouped_df['Province'] == province) & (grouped_df['Etat'] == etat), 'Nombre']
            values.append(value.iloc[0] if not value.empty else 0)
        plt.bar(r1 if idx == 0 else [x + barWidth*idx for x in r1], values, color=color1 if idx % 2 == 0 else color2, width=barWidth, edgecolor='grey', label=etat)
    
    
    
    # Configuration des axes et du graphique
    plt.xlabel('Provinces', fontweight='bold', fontsize=18)  # Augmentation de la taille de la police pour l'axe des x
    plt.ylabel('Nombre', fontsize=18)  # Augmentation de la taille de la police pour l'axe des y
    plt.xticks([r + barWidth for r in range(len(unique_provinces))], unique_provinces, fontsize=16)  # Taille de la police pour les étiquettes de l'axe des x
    plt.yticks(fontsize=16)  # Taille de la police pour les étiquettes de l'axe des y
    plt.title('États de paiement par province', fontsize=16)  # Augmentation de la taille de la police pour le titre
    plt.legend(fontsize=16)  # Augmentation de la taille de la police pour la légende
    
    
    # Sauvegarde du graphique avec un nom de fichier unique
    graph_filename = f"Graphique_Etats_Paiements_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    plt.savefig(graph_filename)
    
    # Ajout du graphique au PDF
    elements.append(Image(graph_filename, 400, 250))
    
    
    
    
    
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
    #pdf.save()
    return pdf_file


if __name__ == '__main__':
    main()
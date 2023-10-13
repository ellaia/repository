from flask import Flask, send_file

import StatsHaouzV6  # Remplacez ceci par le nom de votre script Python
import logging

#logging.basicConfig(filename='application.log', level=logging.INFO)
app = Flask(__name__)
   
@app.route('/generate_pdf')
def generate_pdf():
    pdf_path = StatsHaouzV6.main()  # La fonction main() doit retourner le chemin du PDF généré
    return send_file(pdf_path, as_attachment=True, download_name='custom_name.pdf')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
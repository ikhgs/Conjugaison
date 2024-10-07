from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# Route pour conjuguer un verbe
@app.route('/conjugate', methods=['GET'])
def conjugate():
    # Récupérer le verbe à conjuguer depuis les paramètres de l'URL
    verb = request.args.get('verb', '').lower()
    
    if not verb:
        return jsonify({'error': 'Le verbe est requis'}), 400
    
    # URL de conjugaison sur Reverso (cible la page HTML de conjugaison)
    reverso_url = f"https://conjugator.reverso.net/conjugation-french-verb-{verb}.html"
    
    # Envoyer la requête pour récupérer la page HTML
    response = requests.get(reverso_url)
    
    if response.status_code != 200:
        return jsonify({'error': 'Erreur lors de la récupération de la conjugaison'}), 500
    
    # Utiliser BeautifulSoup pour parser le HTML
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extraire la section de conjugaison
    conjugations = {}
    tense_sections = soup.find_all('section', {'mobile-title': True})
    
    for section in tense_sections:
        tense_name = section['mobile-title']
        forms = [form.text.strip() for form in section.find_all('li')]
        conjugations[tense_name] = forms
    
    # Retourner la réponse JSON avec les conjugaisons extraites
    return jsonify({
        'verb': verb,
        'conjugations': conjugations
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)

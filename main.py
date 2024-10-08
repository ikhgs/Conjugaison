from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
import urllib.parse

app = Flask(__name__)

# Route pour effectuer une recherche Google et scraper la conjugaison
@app.route('/recherche', methods=['GET'])
def recherche():
    query = request.args.get('query')
    
    if not query:
        return jsonify({"error": "La requête est manquante"}), 400

    try:
        # Encoder la requête pour la recherche Google
        search_url = "https://www.google.com/search?q=" + urllib.parse.quote(query + " conjugaison")
        
        # Envoyer une requête GET à Google pour obtenir la page de recherche
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(search_url, headers=headers)
        
        if response.status_code == 200:
            # Parser le contenu HTML avec BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extraire les résultats (extrait de la page visible directement)
            resultats = []
            for item in soup.find_all('span', class_='BNeawe'):
                resultats.append(item.get_text(strip=True))
            
            # Retourner les résultats sous forme de JSON
            return jsonify({
                "query": query,
                "resultats": resultats
            }), 200
        else:
            return jsonify({"error": "Impossible d'accéder à la page de recherche"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Point d'entrée principal
if __name__ == '__main__':
    app.run(debug=True)

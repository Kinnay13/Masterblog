from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

def load_posts():
    """Lädt die Blogbeiträge aus der JSON-Datei"""
    posts_file = os.path.join(os.path.dirname(__file__), 'posts.json')
    if os.path.exists(posts_file):
        with open(posts_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_posts(posts):
    """Speichert die Blogbeiträge in der JSON-Datei"""
    posts_file = os.path.join(os.path.dirname(__file__), 'posts.json')
    with open(posts_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, indent=2, ensure_ascii=False)

def get_next_id(posts):
    """Generiert die nächste eindeutige ID für einen neuen Beitrag"""
    if not posts:
        return 1
    return max(post['id'] for post in posts) + 1

@app.route('/')
def index():
    """Zeigt alle Blogbeiträge auf der Startseite an"""
    posts = load_posts()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    """Zeigt das Formular zum Hinzufügen eines neuen Beitrags oder speichert einen neuen Beitrag"""
    if request.method == 'POST':
        # Daten aus dem Formular holen
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        
        # Validierung: Alle Felder müssen ausgefüllt sein
        if not author or not title or not content:
            return render_template('add.html', error='Alle Felder sind erforderlich!')
        
        # Existierende Beiträge laden
        posts = load_posts()
        
        # Neuen Beitrag erstellen
        new_post = {
            'id': get_next_id(posts),
            'author': author,
            'title': title,
            'content': content
        }
        
        # Neuen Beitrag zur Liste hinzufügen
        posts.append(new_post)
        
        # Beiträge speichern
        save_posts(posts)
        
        # Benutzer zur Startseite umleiten
        return redirect(url_for('index'))
    
    return render_template('add.html')

if __name__ == '__main__':
    app.run(debug=True)
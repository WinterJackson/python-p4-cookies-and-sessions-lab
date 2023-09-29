#!/usr/bin/env python3

from flask import Flask, make_response, jsonify, session
from flask_migrate import Migrate

from models import db, Article, User

app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/clear')
def clear_session():
    session['page_views'] = 0
    return {'message': '200: Successfully cleared session data.'}, 200

@app.route('/articles')
def index_articles():
    # Query all articles from the database
    articles = Article.query.all()
    
    # Manually serialize the articles to a list of dictionaries
    serialized_articles = []
    for article in articles:
        serialized_article = {
            'id': article.id,
            'author': article.author,
            'title': article.title,
            'content': article.content,
            'preview': article.preview,
            'minutes_to_read': article.minutes_to_read,
            'date': article.date.strftime('%Y-%m-%d %H:%M:%S'),
        }
        serialized_articles.append(serialized_article)
    
    # Return the list of articles as a JSON response
    return jsonify(serialized_articles), 200

@app.route('/articles/<int:id>')
def show_article(id):
    # Check if session['page_views'] exists, and if not, set it to 0
    session['page_views'] = session.get('page_views', 0)
    
    # Increment the page_views for each request
    session['page_views'] += 1
    
    # Check if the user has viewed more than 3 pages
    if session['page_views'] > 3:
        return jsonify({'message': 'Maximum pageview limit reached'}), 401
    
    # Retrieve the article by ID
    article = Article.query.get(id)
    
    # Check if the article exists
    if article is None:
        return jsonify({'message': 'Article not found'}), 404
    
    # Manually serialize the article data
    serialized_article = {
        'id': article.id,
        'author': article.author,
        'title': article.title,
        'content': article.content,
        'preview': article.preview,
        'minutes_to_read': article.minutes_to_read,
        'date': article.date.strftime('%Y-%m-%d %H:%M:%S'),
    }
    
    # Return the article data as JSON response
    return jsonify(serialized_article), 200

if __name__ == '__main__':
    app.run(port=5555)

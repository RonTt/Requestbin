from flask import Flask, redirect
import config


app = Flask(__name__)

from werkzeug.contrib.fixers import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app)

app.debug = config.DEBUG
app.secret_key = config.FLASK_SESSION_SECRET_KEY

app.add_url_rule('/', 'views.home')
app.add_url_rule('/<name>', 'views.bin', methods=['GET', 'POST', 'DELETE', 'PUT', 'OPTIONS', 'HEAD', 'PATCH', 'TRACE'])

app.add_url_rule('/docs/<name>', 'views.docs')
app.add_url_rule('/api/v1/bins', 'api.bins', methods=['POST'])
app.add_url_rule('/api/v1/bins/<name>', 'api.bin', methods=['GET'])
app.add_url_rule('/api/v1/bins/<bin>/requests', 'api.requests', methods=['GET'])
app.add_url_rule('/api/v1/bins/<bin>/requests/<name>', 'api.request', methods=['GET'])

app.add_url_rule('/api/v1/stats', 'api.stats')

app.add_url_rule('/favicon.ico', view_func=lambda: redirect('/static/favicon.ico'))
app.add_url_rule('/robots.txt', view_func=lambda: redirect('/static/robots.txt'))


from requestbin import api, views
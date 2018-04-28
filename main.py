from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
from flask_cors import CORS, cross_origin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import sqlite3
import sys

subdomain = 'api'
<<<<<<< HEAD
=======
domain = 'fusiondiscordbots.com'
>>>>>>> d8c60a76538d4a3d7e72d20d85a06697ac728703

app = FlaskAPI(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'
<<<<<<< HEAD
=======
app.config['SERVER_NAME'] = domain
>>>>>>> d8c60a76538d4a3d7e72d20d85a06697ac728703

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['10 per minute']
)

<<<<<<< HEAD
@app.route('/', methods=['GET'])
@cross_origin()
def get_bots():
    with sqlite3.connect('/var/www/fusion-api/API.db') as connection:
=======
@app.route('/', methods=['GET'], subdomain=subdomain)
@cross_origin()
def get_bots():
    with sqlite3.connect('API.db') as connection:
>>>>>>> d8c60a76538d4a3d7e72d20d85a06697ac728703

        cursor = connection.cursor()

        cursor.execute('SELECT id FROM bots')
        return [x[0] for x in cursor.fetchall()]


@app.route('/int:idx')
<<<<<<< HEAD
@app.route('/<int:idx>/', methods=['GET', 'POST'])
@cross_origin()
def update(idx):
    with sqlite3.connect('/var/www/fusion-api/API.db') as connection:
=======
@app.route('/<int:idx>/', methods=['GET', 'POST'], subdomain=subdomain)
@cross_origin()
def update(idx):
    with sqlite3.connect('API.db') as connection:
>>>>>>> d8c60a76538d4a3d7e72d20d85a06697ac728703

        cursor = connection.cursor()
        cursor.row_factory = sqlite3.Row

        cursor.execute('SELECT * FROM bots WHERE id = ?', (idx,))
        bot = [x for x in cursor.fetchall()]

        if len(bot) != 1:
            print('Failed lookup')
            return '', status.HTTP_404_NOT_FOUND

        members = dict(bot[0])['members']
        guilds = dict(bot[0])['guilds']

        if request.method == 'POST':

            token = dict(bot[0])['token']

            if not token == str(request.data.get('token')):
                return '', status.HTTP_401_UNAUTHORIZED

            try:
                members = int(request.data.get('members'))
            except:
                pass

            try:
                guilds = int(request.data.get('guilds'))
            except:
                pass

            cursor.execute('UPDATE bots SET members = ?, guilds = ? WHERE id = ?', (members, guilds, idx))
            connection.commit()

    return {'members' : members, 'guilds' : guilds}

if __name__ == '__main__':
    if 'debug' in sys.argv:
        app.run(debug=True)
    else:
        app.run(host='0.0.0.0', port=443, threaded=True, ssl_context=('/etc/letsencrypt/live/{}.{}/fullchain.pem'.format(subdomain, domain), '/etc/letsencrypt/live/{}.{}/privkey.pem'.format(subdomain, domain)))

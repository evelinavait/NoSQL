import werkzeug
import redis
from flask import (Flask, request, jsonify, abort)


# # Užduoties variantas
# # Redis #5. Skaitiklių rodmenų saugojimo servisas.

s1 = 2110930
s2 = 2110904
uzd_nr = (s1 + s2) % 5 + 1
print(uzd_nr)

from flask import Flask, request, jsonify
import redis

def create_app():
    app = Flask(__name__)

    redisClient = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Užregistruoti klientą sistemoje.
    @app.route('/client', methods=['PUT'])
    def register_client():
        data = request.get_json()

        client_id = redisClient.incr('client_id')

        client_data = {
            'address': data['address'],
            'fullName': data['fullName']
        }

        redisClient.hset(f'client:{client_id}', mapping=client_data)

        return jsonify({'message': 'Klientas sėkmingai užregistruotas', 'clientId': client_id}), 200

# Gauti kliento duomenis.
    @app.route('/client/<int:client_id>', methods=['GET'])
    def get_client(client_id):
        client_data = redisClient.hgetall(f'client:{client_id}')
        # return jsonify({'message': 'Kliento duomenys'}), 200

        return jsonify({
            'clientId': client_id,
            'address': client_data.get('address'),
            'fullName': client_data.get('fullName')
        }), 200


# Išregistruoti klientą iš sistemos.
    @app.route('/client/<int:client_id>', methods=['DELETE'])
    def delete_client(client_id):
        if not redisClient.exists(f'client:{client_id}'):
            return jsonify({'message': 'Klientas sistemoje nerastas'}), 404
        redisClient.delete(f'client:{client_id}')
    
        return jsonify({'message': 'Klientas sėkmingai išregistruotas'}), 200
        
    return app

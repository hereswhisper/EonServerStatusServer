
from flask import Flask, jsonify, request
from flask_cors import CORS
# Import the required libraries for MySQL connection
import mysql.connector

app = Flask(__name__)
CORS(app)  # Handle CORS headers

# Database configuration
DB_CONFIG = {
    'host': '193.203.166.19',
    'user': 'u681420757_Custox',
    'password': 'Farisadam12!',
    'database': 'u681420757_Custox'
}

# Function to get a connection to the database
def get_db_connection():
    # connection = mysql.connector.connect(**DB_CONFIG)
    # Placeholder connection object
    connection = None
    return connection

# Function to read server data from the database
def read_data():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM servers")
    servers = {}
    for row in cursor.fetchall():
        server_name = row['server_name']
        servers[server_name] = {
            'match_started': row['match_started'],
            'player_count': row['player_count'],
            'status': row['status']
        }
    cursor.close()
    connection.close()
    return servers

# Function to write server data to the database
def write_data(servers):
    connection = get_db_connection()
    cursor = connection.cursor()
    for server_name, data in servers.items():
        cursor.execute(
            "UPDATE servers SET match_started=%s, player_count=%s, status=%s WHERE server_name=%s",
            (data['match_started'], data['player_count'], data['status'], server_name)
        )
    connection.commit()
    cursor.close()
    connection.close()


# Removed initialization check for file
    with open(DATA_FILE, 'w') as f:
        initial_data = {
            "NAE": {"match_started": False, "player_count": 0, "status": "Online"},
            "EU": {"match_started": False, "player_count": 0, "status": "Online"}
        }
        json.dump(initial_data, f)

def read_data():
    with open(DATA_FILE, 'r') as f:
        return json.load(f)

def write_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f)

@app.route('/server/<server_name>/status', methods=['GET'])
def get_server_status(server_name):
    servers = read_data()
    return jsonify(servers.get(server_name, {}))

@app.route('/server/<server_name>/start_match', methods=['POST'])
def start_match(server_name):
    servers = read_data()
    servers[server_name]['match_started'] = False
    servers[server_name]['status'] = "The match has started!"
    write_data(servers)
    return jsonify({"message": "Match ended."})

@app.route('/server/<server_name>/end_match', methods=['POST'])
def end_match(server_name):
    servers = read_data()
    servers[server_name]['match_started'] = False
    servers[server_name]['player_count'] = 0
    servers[server_name]['status'] = "Waiting for the match to start.."
    write_data(servers)
    return jsonify({"message": "Match ended."})

@app.route('/server/<server_name>/change_player_count', methods=['POST'])
def change_player_count(server_name):
    change = request.json.get('change')
    servers = read_data()
    servers[server_name]['player_count'] += change
    write_data(servers)
    return jsonify({"message": f"Player count changed by {change}."})

@app.route('/server/<server_name>/waiting_for_players', methods=['POST'])
def waiting_for_players(server_name):
    servers = read_data()
    servers[server_name]['status'] = "Waiting for Players"
    write_data(servers)
    return jsonify({"message": "Status set to 'Waiting for Players'."})

@app.route('/server/<server_name>/offline', methods=['POST'])
def set_offline(server_name):
    servers = read_data()
    servers[server_name]['status'] = "Offline"
    write_data(servers)
    return jsonify({"message": "Status set to 'Offline'."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)  # Bind to all IP addresses


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)  # Bind to all IP addresses

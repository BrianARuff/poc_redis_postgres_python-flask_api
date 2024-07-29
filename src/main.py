from flask import Flask, request, jsonify
import redis
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from functools import wraps

app = Flask(__name__)

# Redis connection setup
redis_client = redis.StrictRedis(host='localhost', port=6379, decode_responses=True)

# PostgreSQL connection pool setup
postgres_pool = SimpleConnectionPool(
    1, 20,  # min and max connections in the pool
    host='localhost',
    dbname='brian',
    user='brian',
    password='2477',
    cursor_factory=RealDictCursor
)

# Decorator for PostgreSQL connection management
def with_postgres_connection(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        conn = postgres_pool.getconn()
        try:
            return f(conn, *args, **kwargs)
        finally:
            postgres_pool.putconn(conn)
    return decorated_function

# Add a new name
@app.route('/names', methods=['POST'])
@with_postgres_connection
def add_name(conn):
    name = request.json.get('name')
    if not name:
        return jsonify({'error': 'Name is required'}), 400

    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO test (name) VALUES (%s)", (name,))
            conn.commit()
        # Cache in Redis
        redis_client.set(name, name)
        return jsonify({'message': 'Name added successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get all names (limited to 100)
@app.route('/names', methods=['GET'])
@with_postgres_connection
def get_all_names(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM test LIMIT 100")
            names = cursor.fetchall()
        return jsonify(names), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get a specific name
@app.route('/names/<name>', methods=['GET'])
@with_postgres_connection
def get_name(conn, name):
    # Check if the name is in Redis
    cached_name = redis_client.get(name)
    if cached_name:
        return jsonify({'name': cached_name}), 200

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name FROM test WHERE name = %s", (name,))
            result = cursor.fetchone()
            if result:
                # Cache the result in Redis
                redis_client.set(name, result['name'])
                return jsonify(result), 200
            else:
                return jsonify({'error': 'Name not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/names/search', methods=['GET'])
@with_postgres_connection
def search_names(conn):
    query = request.args.get('query')
    search_type = request.args.get('type', 'contains').lower()  # Default to 'contains' if not specified

    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    if search_type == 'startswith':
        search_pattern = f'%{query}'
    elif search_type == 'endswith':
        search_pattern = f'{query}%'
    elif search_type == 'contains':
        search_pattern = f'%{query}%'
    else:
        return jsonify({'error': 'Invalid search type'}), 400

    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT name FROM test WHERE name LIKE %s LIMIT 100', (search_pattern,))
            results = cursor.fetchall()
        return jsonify(results), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


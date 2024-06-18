import os
from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
# from dotenv import load_dotenv

print(os.getenv('FLASK_ENV'))
# load_dotenv()

app = Flask(__name__)

if os.getenv('FLASK_ENV') == 'development':
    import debugpy
    debugpy.listen(('0.0.0.0', 5678))
    # print("Waiting for debugger attach...")
    # debugpy.wait_for_client()

def get_db_connection():
    conn = psycopg2.connect(
        host="db",
        database="postgres",
        user="postgres",
        password="postgres"
    )
    return conn

@app.route('/items', methods=['GET', 'POST'])
def manage_items():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=RealDictCursor)

    if request.method == 'POST':
        new_item = request.json['name']
        cursor.execute('INSERT INTO items (name) VALUES (%s)', (new_item,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'status': 'Item added'}), 201

    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(items)

print('PAPAYA')
if __name__ == "__main__":
    app.run(host='0.0.0.0')

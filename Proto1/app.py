from flask import Flask, jsonify, render_template

import psycopg2
import os

app = Flask(__name__)

# PostgreSQL connection config (replace with your actual values)
DB_HOST = "localhost"
DB_NAME = "your_db_name"
DB_USER = "your_username"
DB_PASSWORD = "your_password"

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, price, image_url FROM products")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    products = [
        {
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "price": float(row[3]),
            "image_url": row[4]
        } for row in rows
    ]
    return jsonify(products)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

# Serve frontend if needed
@app.route('/')
def serve_index():
    return render_template('index.html')  # assumes index.html is in the same dir

@app.route('/debug/db')
def debug_db():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM products")
        count = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify({"product_count": count})
    except Exception as e:
        return jsonify({"error": str(e)})
    

if __name__ == '__main__':
    app.run(debug=True)




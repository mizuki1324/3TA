from flask import Flask, jsonify, render_template

import psycopg2
import os

app = Flask(__name__)

# PostgreSQL connection config
DB_HOST = "localhost"
DB_NAME = "product_db"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create products table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            price DECIMAL(10,2) NOT NULL,
            image_url VARCHAR(255)
        )
    """)
    
    # Check if table is empty
    cur.execute("SELECT COUNT(*) FROM products")
    count = cur.fetchone()[0]
    
    # Insert sample data only if table is empty
    if count == 0:
        cur.execute("""
            INSERT INTO products (name, description, price, image_url) VALUES
            ('Premium Wireless Headphones', 'High-quality noise-canceling headphones with 30-hour battery life', 249.99, 'https://example.com/headphones.jpg'),
            ('Smart Fitness Watch', 'Advanced fitness tracking with heart rate monitoring', 199.99, 'https://example.com/watch.jpg'),
            ('Wireless Charging Pad', 'Fast wireless charging pad compatible with all Qi-enabled devices', 49.99, 'https://example.com/charger.jpg'),
            ('Smart Home Speaker', 'Voice-activated smart speaker with excellent sound quality', 129.99, 'https://example.com/speaker.jpg')
        """)
    
    conn.commit()
    cur.close()
    conn.close()

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
    # Initialize database when app starts
    try:
        init_db()
        print("Database initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
    
    app.run(debug=True)




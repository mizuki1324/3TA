from flask import Flask, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(
        host=os.environ.get('DB_HOST', 'localhost'),
        database=os.environ.get('DB_NAME', 'product_db'),
        user=os.environ.get('DB_USER', 'postgres'),
        password=os.environ.get('DB_PASSWORD', 'postgres'),
        port=os.environ.get('DB_PORT', '5432')
    )
    conn.autocommit = True
    return conn

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint to verify the API is running"""
    try:
        # Test database connection
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT 1')
        cur.close()
        conn.close()
        
        return jsonify({
            'status': 'healthy',
            'message': 'API is running and database connection is successful'
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'message': f'Error: {str(e)}'
        }), 500

@app.route('/api/products', methods=['GET'])
def get_products():
    """Endpoint to retrieve all products from the database"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM products')
        products = cur.fetchall()
        cur.close()
        conn.close()
        
        return jsonify({
            'status': 'success',
            'count': len(products),
            'products': products
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to retrieve products: {str(e)}'
        }), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Endpoint to retrieve a specific product by ID"""
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute('SELECT * FROM products WHERE id = %s', (product_id,))
        product = cur.fetchone()
        cur.close()
        conn.close()
        
        if product:
            return jsonify({
                'status': 'success',
                'product': product
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': f'Product with ID {product_id} not found'
            }), 404
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to retrieve product: {str(e)}'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'lib'
}

def connect_to_database():
    try:
        conn = mysql.connector.connect(**mysql_config)
        print("connected to mysql")
        return conn
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

@app.route('/')
def index():
    conn = connect_to_database()
    print("mainpage")
    cursor = conn.cursor(dictionary=True)
    query = "SELECT * FROM library"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    return render_template('index.html', results=results)

@app.route('/add_book', methods=['POST'])
def add_book():
    try:
        data = request.get_json()
        print(data)
        if data:
            conn = connect_to_database()
            if conn:
                cursor = conn.cursor()
                print("cursor connected")

                query = "INSERT INTO library (TITLE,AUTHOR,GENRE,DATEOFPUBLISH,PGNUMBER) VALUES (%s, %s, %s, %s, %s)"
                insert_values = (
                    data['TITLE'], data['AUTHOR'], data['GENRE'], data['DATEOFPUBLISH'], data['PGNUMBER']
                                )
                cursor.execute(query, insert_values)
                print("executed")               
                conn.commit()
                cursor.close()
                conn.close()
                return jsonify({'message': 'Employee details added successfully'})
            else:
                return jsonify({'error': 'Failed to connect to the database'})
        else:
            return jsonify({'error': 'No data provided'})
    except Exception as e:
        return jsonify({'error': str(e)})
    
if __name__ == '__main__':
    app.run(debug=True, port = 4000)
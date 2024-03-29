from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

# def handle_error(message, status_code=400): 
#     return jsonify({"error": message}), status_code

def fetch_data():
    
    try:
        connection_string = "mongodb://172.17.0.2:27017/niha_mongodb"
        client = MongoClient(connection_string)
        db = client.get_database("niha_mongodb")
    except MongoClient.Error as err:
        return jsonify({'error': f'Database connection error: {err}'}), 500

    try:
        collection = db.get_collection("items")
        data = collection.find()
        book_data = []
        for document in data: 
            print (document)
            document['_id'] = str(document['_id'])
            book_data.append(document)
    except MongoClient.Error as err:
        return jsonify({'error': f'Query execution error: {err}'}), 500

    finally:
        if client.server_info():
            client.close() 
    print(book_data)
    return book_data

@app.route('/data')
def display_data():
    tempdata=fetch_data()     
    json_data = jsonify({'my_books': tempdata})
    print(json_data)
    return json_data

# Route for index page
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/books", methods=["GET"])
def search_books():
    alldata = fetch_data()
    print("THIS IS ALL DATA", alldata)
    book = request.args.get("book")
    print(book)
    result = search_book_by_author(book, alldata)
    return render_template("searching_book.html", searched_author=result)
    
# API endpoint to get a book by ID (GET)   
def search_book_by_author(x, y):
    print(y)
    for z in y:
        if x in z.values():
            print("Found the book")
            return z
    return None


@app.route("/add-book", methods=['POST'])
def add_book():
    try:
        connection_string = "mongodb://172.17.0.2:27017/niha_mongodb"
        client = MongoClient(connection_string)
        db = client.get_database("niha_mongodb")
    except MongoClient.Error as err:
        return jsonify({'error': f'Database connection error: {err}'}), 500

    try:
        collection = db.get_collection("items")
        data = collection.find()
        print("This is collection", data)
        getbook = request.get_json()
        print("Document to update", getbook)
        if not getbook:
            return jsonify ({'error': 'No data provided'}), 400
        book_id = getbook.get("Book_id")
        print(book_id)
        title = getbook.get('title')
        print(title)
        author = getbook.get('Author') # Validate data
        print(author)
        collection.insert_one({"Book_id": book_id, "Title": title, "Author": author})
        data = collection.find()
        print("This is updated collection", data)
        if not data:
            return jsonify({'error': 'Missing required fields'}), 400
        # Process data (store in database, etc. ) #
        else:
            return jsonify({'message': 'Book added success fully '}), 201

    finally:
        if client.server_info():
            client.close()  

    
    # Get data from request for MYSQL server
    # getbook = request.get_json()
    # print(getbook)
    # if not getbook:
    #     return jsonify ({'error': 'No data provided'}), 400
    # book_id = getbook.get('Book_id')
    # print(book_id)
    # title = getbook.get('title')
    # print(title)
    # author = getbook.get('Author') # Validate data
    # print(author)
    # sql = "INSERT INTO books (book_id, Title, Author) VALUES (%s, %s, %s)"
    # val = (book_id, title, author)   
    # cursor.execute(sql, val)

    # Commit the changes
    # connection.commit()

    # # Close the connection
    # connection.close()
    # if not title or not author:
    #     return jsonify({'error': 'Missing required fields'}), 400
    # # Process data (store in database, etc. ) #
    # return jsonify({'message': 'Book added success fully '}), 201
    
#DELETE query for MongoDB   
@app.route("/delete", methods=['DELETE'])
def delete_book():
    try:
        connection_string = "mongodb://172.17.0.2:27017/niha_mongodb"
        client = MongoClient(connection_string)
        db = client.get_database("niha_mongodb")
    except MongoClient.Error as err:
        return jsonify({'error': f'Database connection error: {err}'}), 500

    try:
        collection = db.get_collection("items")
        data = collection.find()
        getbook = request.get_json()
        print("This is my collection", getbook)
        if not getbook:
            return jsonify ({'error': 'No data provided'}), 400
        book_id = getbook.get('Book_id')
        print(book_id)
        collection.delete_one({"Book_id" : book_id})
        data = collection.find()
        print(data)
        if not data:
            return jsonify({'error': 'Missing required fields'}), 400
        # Process data (store in database, etc. ) #
        else:
            return jsonify({'message': 'Book deleted successfully'}), 201

    finally:
        if client.server_info():
            client.close()  

    
# @app.route("/delete", methods=['DELETE'])
# def remove_book():
#     # Get data from request
#     data = request.get_json()
#     print(data)
#     if not data:
#         return jsonify ({'error': 'No data provided'}), 400
#     book_id = data.get('book_id')
#     print(book_id)
    
#     try:
#         connection = mysql.connector.connect(**DATABASE_CONFIG)
#         cursor = connection.cursor(dictionary=True)
#     except mysql.connector.Error as err:
#         return jsonify({'error': f'Database connection error: {err}'}), 500
    

#     sql = "DELETE from books WHERE book_id = %s"
#     my_deleted_id = (book_id)
#     cursor.execute(sql, my_deleted_id)

#     # Commit the changes
#     connection.commit()

#     # Close the connection
#     connection.close()
    
#     if not book_id:
#         return jsonify({'error': 'Missing required fields'}), 400
#     # Process data (store in database, etc. ) #
#     return jsonify({'message': 'Book deleted successfully'}), 201
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)



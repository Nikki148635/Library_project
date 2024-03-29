from pymongo import MongoClient

connection_string = "mongodb://localhost:27017/niha_mongodb"
client = MongoClient(connection_string)
db = client.get_database("niha_mongodb")

collection = db.get_collection("items")

documents = []
documents.append({"Book_id": 2,
        "title": "Geetanjali",
        "Author": "Rabindra Nath Tagore"
    })
documents.append({
        "Book_id": 3,
        "title": "Utopia",
        "Author": "Sir Thomas Moor"
    })
documents.append({
        "Book_id": 4,
        "title": "Origin of Species",
        "Author": "Charles Darwin"
    })
documents.append({
        "Book_id": 5,
        "title": "Das Kapital",
        "Author": "Karl Marx"
    })
response = collection.insert_many(documents)
last_inserted_ids = response.inserted_ids
print(f"last_inserted_id {last_inserted_ids}")
import pymongo
from pymongo import MongoClient

# Connection URI for MongoDB Atlas
# Replace <username> and <password> with your MongoDB Atlas credentials
# Replace <cluster-url> with your MongoDB cluster URL
uri = "mongodb+srv://samriddh_kumar:sam123@tracknclassify.kjmrfft.mongodb.net/?retryWrites=true&w=majority&appName=TrackNClassify"

# Create a connection using MongoClient
client = MongoClient(uri)

# Specify the database to use (if it doesn't exist, it will be created)
db = client['Employee']

# Specify the collection to use (if it doesn't exist, it will be created)
collection = db['Employee']

# Insert a document into the collection
document = {"ID": "4", "Name": "S.K.Sahu","Age":"45"}
insert_result = collection.insert_one(document)
print(f"Inserted document ID: {insert_result.inserted_id}")

# Find a document in the collection
found_document = collection.find_one({"name": "John Doe"})
print(f"Found document: {found_document}")


# Close the connection
client.close()

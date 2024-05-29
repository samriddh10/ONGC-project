
// Select the database to use.
use('Employee');

// Insert a few documents into the sales collection.
db.getCollection('Sales').insertMany([
  { 'ID': '1', 'Name':'Samriddh' , 'Age': 19},
  { 'ID': '2', 'Name':'Abhinav' , 'Age': 20},
  { 'ID': '3', 'Name':'Shakti' , 'Age': 20}
]);



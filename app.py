from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# MongoDB Configuration
client = MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB connection string
db = client['note_app']  # Database name
notes_collection = db['notes']  # Collection name

@app.route('/')
def index():
    notes = load_notes()
    return render_template('index.html', notes=notes)

@app.route('/add_note', methods=['POST'])
def add_note():
    note_text = request.form['note_text']
    note_color = request.form['note_color']
    # Insert note into MongoDB
    notes_collection.insert_one({'text': note_text, 'color': note_color})
    return index()

@app.route('/delete_note/<note_id>', methods=['POST'])
def delete_note(note_id):
    # Delete note by its MongoDB ObjectId
    from bson.objectid import ObjectId
    notes_collection.delete_one({'_id': ObjectId(note_id)})
    return index()

def load_notes():
    # Retrieve all notes from MongoDB
    notes = list(notes_collection.find())
    for note in notes:
        note['_id'] = str(note['_id'])  # Convert ObjectId to string for rendering
    return notes

if __name__ == '__main__':
    app.run(debug=True)


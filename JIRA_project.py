import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'my_database',
    'host': 'localhost',
    'port': 27017
}
db = MongoEngine()
db.init_app(app)

class User(db.Document):
    Title = db.StringField()
    Description = db.StringField()
    Jira_Project_ID = db.StringField()
    def to_json(self):
        return {"Title": self.Title,
                "Description": self.Description,
                "Jira Project ID": self.Jira_Project_ID}

@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    user = User.objects(name=record['Jira Project ID']).first()
    if not user:
        return jsonify({'error': 'Task with same title already exists'})
    else:
        user.update(Jira_Project_ID=record['Jira Project ID'])
    return jsonify(user.to_json())

if __name__ == "__main__":
    app.run(debug=True)

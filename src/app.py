from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    messages = db.relationship('Message', backref='chat')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(), nullable=False)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)

@app.route('/chat', methods=['POST'])
def create_chat():
    chat = Chat()
    db.session.add(chat)
    db.session.commit()
    return jsonify({"id": chat.id}), 201

@app.route('/chat', methods=['GET'])
def get_chats():
    chats = Chat.query.all()
    return jsonify([{"id": chat.id} for chat in chats])

@app.route('/chat/messages', methods=['POST'])
def post_message():
    chat_id = request.json['chat_id']
    content = request.json['content']
    message = Message(content=content, chat_id=chat_id)
    db.session.add(message)
    db.session.commit()
    return jsonify({"id": message.id}), 201

@app.route('/chat/messages', methods=['GET'])
def get_messages():
    chat_id = request.args.get('chat_id')
    messages = Message.query.filter_by(chat_id=chat_id).all()
    return jsonify([{"id": message.id, "content": message.content} for message in messages])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

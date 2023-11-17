from flask import Flask, render_template, request, jsonify, session, escape
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chatbot.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

peruvian_food_qa = {
    "¿Cuál es el plato más famoso de la comida peruana?": "El ceviche es uno de los platos más famosos de la comida peruana.",
    "¿Qué ingredientes lleva el lomo saltado?": "El lomo saltado lleva carne de res, tomate, cebolla, y otros ingredientes.",
    "¿Cuál es el postre típico de Perú?": "El postre típico de Perú es el suspiro a la limeña.",
    "¿Qué es el rocoto?": "El rocoto es un tipo de pimiento picante utilizado en la gastronomía peruana.",
    "¿Cómo se prepara el ají de gallina?": "El ají de gallina se prepara con gallina desmenuzada y una salsa espesa de ají amarillo.",
    "¿Cuál es la bebida típica de Perú?": "La bebida típica de Perú es el pisco sour.",
    "¿Qué es la causa limeña?": "La causa limeña es un plato peruano hecho a base de papa amarilla y ají.",
    "¿Cuál es la diferencia entre el ceviche peruano y el ceviche mexicano?": "La diferencia principal radica en los ingredientes y el estilo de preparación.",
    "¿Qué es el cuy?": "El cuy es un plato tradicional peruano que consiste en carne de conejillo de Indias.",
    "¿Cuál es la influencia de la cocina peruana en la gastronomía mundial?": "La cocina peruana ha ganado reconocimiento global por su diversidad y sabores únicos."
}

class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_message = db.Column(db.String(255))
    bot_response = db.Column(db.String(255))

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.form['user_message']

        user_data = session.get('user_data', {})

        if user_message in peruvian_food_qa:
            bot_response = peruvian_food_qa[user_message]
        else:
            bot_response = 'Lo siento, no tengo información sobre eso en este momento.'

        bot_response = escape(bot_response)

        user_data[user_message] = bot_response
        session['user_data'] = user_data

        chat_entry = Chat(user_message=user_message, bot_response=bot_response)
        db.session.add(chat_entry)
        db.session.commit()

        # Obtén todas las entradas del chat y conviértelas a una lista de diccionarios
        chat_entries = [{'user_message': entry.user_message, 'bot_response': entry.bot_response} for entry in Chat.query.all()]

        return render_template('index.html', chat_entries=json.dumps(chat_entries))

    except KeyError:
        return jsonify({'bot_response': 'Error: Debes proporcionar un mensaje del usuario.'})

    except Exception as e:
        return jsonify({'bot_response': f'Error: {escape(str(e))}'})

if __name__ == '__main__':
    app.run(debug=True)

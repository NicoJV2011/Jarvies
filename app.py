from flask import Flask, request # type: ignore
from flask_migrate import Migrate # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort # type: ignore
import os
from dotenv import load_dotenv # type: ignore
from twilio.rest import Client # type: ignore
from twilio.rest import Client # type: ignore
import logging


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
# Initialize Flask-Migrate
migrate = Migrate(app, db)
api = Api(app)
load_dotenv()


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(80), unique = True, nullable = False) 

    def __repr__(self):
        return f'ID {self.id } Name {self.name}'
    
user_args = reqparse.RequestParser()
user_args.add_argument('name', type=str, required=True, help='Name cannot be blank')

class SmsOutbounding(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    text = db.Column(db.String(100))

    def __repr__(self):
        return f'text message: {self.text}'
sms_args = reqparse.RequestParser()
sms_args.add_argument('text', type=str)

#Serializers
userFields = {
    'id':fields.Integer,
    'name':fields.String
}
SmsFields = {
    'id':fields.Integer,
    'text':fields.String
}

#controller
class Users(Resource):
    @marshal_with(userFields)
    def get(self):
        users = UserModel.query.all()
        return users
    
    @marshal_with(userFields)
    def post(self):

        """
        in this section i'll implement sms functionality

        """
        account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        client = Client(account_sid, auth_token)
        message = client.messages.create(
        from_='whatsapp:+14155238886',
        to='whatsapp:+61430636134',
        body='Hola Nicolas',
        )


        print(message)


        args = user_args.parse_args()
        user = UserModel(name=args['name'])
        db.session.add(user)
        db.session.commit()
        user = UserModel.query.all()
        return user, 201
    
class Text(Resource):
    @marshal_with(SmsFields)
    def get(self):
        text = SmsOutbounding.query.all()
        return text
    
    @marshal_with(SmsFields)
    def post(self):
        args = sms_args.parse_args()
        message_sid = request.form['Body']
        logging.info(f' data ---> {message_sid}')
        # message_status = request.form.get('MessageStatus')
        # message = SmsOutbounding(text=args['text'])
        # db.session.add(message_sid)
    
        # db.session.commit()
        # message = SmsOutbounding.query.all()
        return message_sid, message_sid




#routes
api.add_resource(Users, '/api/users/')
api.add_resource(Text,'/api/text/')


@app.route('/')
def home():
    return '<h1>Flask Rest Api</h1>'

if __name__ == '__main__':
    app.run(debug=True)

    
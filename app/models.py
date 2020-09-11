from app import db
from datetime import datetime


class Companies(db.Model):
    guid = db.Column(db.String(50), primary_key=True)
    address = db.Column(db.String(50))
    fullName = db.Column(db.String(256), nullable=False)
    inn = db.Column(db.String(50), unique=True, nullable=False)
    kpp = db.Column(db.String(50), unique=True, nullable=False)
    ogrn = db.Column(db.String(50), unique=True, nullable=False)

    addresses = db.relationship('Messages', backref='companies', lazy=False)

    def asdict(self):
        return {
            'guid': self.guid,
            'address': self.address,
            'fullName': self.fullName,
            'inn': self.inn,
            'kpp': self.kpp,
            'ogrn': self.ogrn
        }

    def __repr__(self):
        return f'<Company {self.guid}>'


class Messages(db.Model):
    guid = db.Column(db.String(50), primary_key=True)
    text = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(256), unique=True, nullable=False)
    date = db.Column(db.DateTime)
    owner_guid = db.Column(db.Integer, db.ForeignKey('companies.guid'), nullable=False)

    def asdict(self):
        return {
            'guid': self.guid,
            'owner_guid': self.owner_guid,
            'text': self.text,
            'url': self.url,
            'date': self.date
        }
        
    def __repr__(self):
        return f'<Message {self.guid}>'

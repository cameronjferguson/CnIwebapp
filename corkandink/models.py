from datetime import datetime
from corkandink import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(150), nullable=False)
    region = db.Column(db.String(150))
    grape = db.Column(db.String(100))
    country = db.Column(db.String(30))
    year = db.Column(db.Integer)
    wine_type = db.Column(db.String(20))
    location = db.Column(db.String(100))
    price = db.Column(db.String(16))
    purch_loc = db.Column(db.String(150))
    purch_url = db.Column(db.String(2048))
    rating = db.Column(db.Integer)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
from db import SessionLocal
from models import Painting, User, Like

def seed_data():
    db = SessionLocal()
    if db.query(Painting).count() == 0:
        paintings = [
            {"title": "Starry Night", "artist": "Vincent van Gogh", "price": 100.0},
            {"title": "Mona Lisa", "artist": "Leonardo da Vinci", "price": 200.0},
            {"title": "The Persistence of Memory", "artist": "Salvador Dali", "price": 150.0},
            {"title": "The Scream", "artist": "Edvard Munch", "price": 120.0},
            {"title": "Girl with a Pearl Earring", "artist": "Johannes Vermeer", "price": 130.0},
            {"title": "Guernica", "artist": "Pablo Picasso", "price": 160.0},
            {"title": "The Kiss", "artist": "Gustav Klimt", "price": 140.0},
            {"title": "American Gothic", "artist": "Grant Wood", "price": 110.0},
            {"title": "The Night Watch", "artist": "Rembrandt", "price": 170.0},
            {"title": "The Birth of Venus", "artist": "Sandro Botticelli", "price": 180.0},
        ]
        for p in paintings:
            db.add(Painting(**p))

    if not db.query(User).filter_by(username="Henri").first():
        user = User(username="Henri", token="123123123")
        db.add(user)
        db.add(Like(username="Henri", title="Starry Night"))
        db.add(Like(username="Henri", title="Mona Lisa"))
    db.commit()
    db.close()


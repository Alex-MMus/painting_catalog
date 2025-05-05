from sqlalchemy.orm import Session
from models import Painting, User, Like
from schemas import PaintingCreate
from fastapi import HTTPException
import uuid

def get_user_by_token(db: Session, token: str):
    return db.query(User).filter(User.token == token).first()

def authenticate_user(db: Session, username: str):
    user = db.query(User).filter(User.username == username).first()
    if user:
        return {"token": user.token}
    token = str(uuid.uuid4())
    user = User(username=username, token=token)
    db.add(user)
    db.commit()
    return {"token": token}

def create_painting(db: Session, painting: PaintingCreate):
    db_painting = Painting(**painting.model_dump())
    db.add(db_painting)
    db.commit()
    db.refresh(db_painting)
    return db_painting

def get_all_paintings(db: Session):
    return db.query(Painting).all()

def toggle_like(db: Session, username: str, title: str):
    painting = db.query(Painting).filter(Painting.title == title).first()
    if not painting:
        raise HTTPException(status_code=404, detail="Painting not found")
    like = db.query(Like).filter(Like.username == username, Like.title == title).first()
    if like:
        db.delete(like)
        db.commit()
        return {"message": "Like removed"}
    new_like = Like(username=username, title=title)
    db.add(new_like)
    db.commit()
    return {"message": "Like added"}

def calculate_rating(db: Session, title: str):
    painting = db.query(Painting).filter(Painting.title == title).first()
    if not painting:
        raise HTTPException(status_code=404, detail="Painting not found")

    # Все картины и цены
    paintings = db.query(Painting).all()
    prices = [p.price for p in paintings]
    avg_price = sum(prices) / len(prices) if prices else 1

    # Подсчёт лайков по картинам
    like_counts = {}
    for like in db.query(Like).all():
        like_counts[like.title] = like_counts.get(like.title, 0) + 1
    all_likes = list(like_counts.values())
    avg_likes = sum(all_likes) / len(all_likes) if all_likes else 1

    # Вычисляем рейтинг каждой картины
    rating_map = {}
    for p in paintings:
        price_factor = p.price / avg_price
        like_count = like_counts.get(p.title, 0)
        like_factor = like_count / avg_likes if avg_likes else 0
        rating_map[p.title] = price_factor * like_factor

    # Рейтинг текущей картины
    current_rating = rating_map.get(title, 0)
    max_rating = max(rating_map.values()) if rating_map else 1
    score = 10 * current_rating / max_rating if max_rating else 0

    return {
        "title": title,
        "rating": current_rating,
        "score": score,
        "likes": like_counts.get(title, 0),
        "price": painting.price,
        "avg_price": avg_price,
        "avg_likes": avg_likes,
        "max_rating": max_rating
    }


def get_paintings_by_score(db: Session):
    paintings = db.query(Painting).all()
    prices = [p.price for p in paintings]
    avg_price = sum(prices) / len(prices) if prices else 1

    # Подсчёт лайков
    like_counts = {}
    for like in db.query(Like).all():
        like_counts[like.title] = like_counts.get(like.title, 0) + 1
    all_likes = list(like_counts.values())
    avg_likes = sum(all_likes) / len(all_likes) if all_likes else 1

    # Расчёт рейтингов
    rating_map = {}
    for p in paintings:
        price_factor = p.price / avg_price
        like_factor = (like_counts.get(p.title, 0) / avg_likes) if avg_likes else 0
        rating_map[p.title] = price_factor * like_factor

    max_rating = max(rating_map.values()) if rating_map else 1

    # Формируем список с оценками (score)
    result = [
        {"title": title, "score": 10 * rating / max_rating if max_rating else 0}
        for title, rating in rating_map.items()
    ]

    # Сортировка по убыванию
    result.sort(key=lambda x: x["score"], reverse=True)
    return result



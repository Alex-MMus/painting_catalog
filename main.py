from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
from db import get_db, Base, engine
import models, crud, init_db
from schemas import PaintingCreate, PaintingOut, LikeResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

app = FastAPI()
Base.metadata.create_all(bind=engine)
init_db.seed_data()

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    user = crud.get_user_by_token(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    return user.username

@app.post("/login")
def login(username: str, db: Session = Depends(get_db)):
    return crud.authenticate_user(db, username)

@app.get("/paintings", response_model=list[schemas.PaintingOut])
def list_paintings(db: Session = Depends(get_db)):
    paintings = db.query(models.Painting).all()
    return paintings

@app.post("/paintings", response_model=PaintingOut)
def add_painting(painting: PaintingCreate, username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_painting(db, painting)

@app.post("/like/{title}", response_model=LikeResponse)
def like(title: str, username: str = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.toggle_like(db, username, title)

@app.get("/rating/{title}")
def get_rating(title: str, db: Session = Depends(get_db)):
    return crud.calculate_rating(db, title)

@app.get("/paintings/scores", response_model=list[schemas.PaintingScore])
def get_scores(db: Session = Depends(get_db)):
    return crud.get_paintings_by_score(db)


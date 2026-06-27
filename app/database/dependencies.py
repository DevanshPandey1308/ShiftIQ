from app.database.database import SessionLocal


def get_db(): 
    db = SessionLocal()

    try:
        yield db #Intead of using return we use yield because return immediately exit function but yield takes this datbase session Use it and when finished come back. (return ends the session yields pause it)

    finally:
        db.close()
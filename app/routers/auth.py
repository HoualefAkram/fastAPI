from fastapi import Depends, status, HTTPException, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )
    if user == None:
        raise HTTPException(
            status_code=status.HTTP_403_NOT_FOUND, detail="Invalid Credentials"
        )

    verify = utils.verify(
        plain_password=user_credentials.password, hashed_password=user.password
    )

    if not verify:
        raise HTTPException(
            status_code=status.HTTP_403_NOT_FOUND, detail="Invalid Credentials"
        )

    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer"}

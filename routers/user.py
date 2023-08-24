from fastapi import Body, status, Path, Depends
from fastapi.responses import JSONResponse
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from fastapi import HTTPException

from schemas.user import User, UserLogin, UserSingUp
from schemas.user import UserComplete
from services.user import UserService
from middlewares.jwt_bearer import JWTBearer
from utils.jwt_manager import get_password_hash
from utils.jwt_manager import create_token
from config.database import Session

from schemas.rig import Rig
from services.company import CompanyService
from services.rig import RigService

user_router = APIRouter()

@user_router.post(
          path="/login", 
          status_code=status.HTTP_200_OK,
          tags=["users"],
          summary="Login user in the app",
          response_model=dict)
def login(user: UserLogin = Body(...)):
     db = Session()
     result = UserService(db).authenticate_user(user)
     print(result)
     if result:
        token: str = create_token(user.dict())
        return JSONResponse(status_code=status.HTTP_200_OK, content=token)

@user_router.post(
        path="/signup",
        response_model=UserLogin,
        tags=["users"],
        status_code=status.HTTP_201_CREATED,
        summary="Create new User")
def signup(user: User = Body(...)):
      db = Session()
      existing_user = UserService(db).get_user_by_username(user.username)
      if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
      hashed_password = get_password_hash(user.password)
      user.password = hashed_password
      result = UserService(db).create_user(user)
      signup_user = UserSingUp(username=result.username, email=result.email, company_id=result.company_id)
      return JSONResponse(status_code=status.HTTP_201_CREATED, content=jsonable_encoder(signup_user))

@user_router.delete(
        path='/users/{id_user}',
        tags=['users'], 
        response_model=dict, 
        status_code=status.HTTP_200_OK,
        summary="Delete User",
        dependencies=[Depends(JWTBearer())])
def delete_user(id_user: int = Path(...)):
    db = Session()
    print(id)
    user = UserService(db).get_user_by_Id(id_user)
    print(user)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    UserService(db).delete_user(id_user)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "User removed"})

@user_router.put(
        path='/users/{id_user}', 
        tags=['users'], 
        response_model=dict, 
        status_code=status.HTTP_200_OK,
        summary="Update data User",
        dependencies=[Depends(JWTBearer())])
def update_user(id_user: int = Path(...), user: User = Body(...)):
    db = Session()
    result = UserService(db).get_user_by_Id(id_user)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    UserService(db).update_user(id_user, user)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Modified User"})


@user_router.post(
          path="/userComplete", 
          status_code=status.HTTP_201_CREATED,
          tags=["users"],
          summary="Add User With Company and Rig",
          response_model=dict)
def loginUserComplete(user_complete: UserComplete = Body(...)):
    db = Session()
    ## Create Company
    CompanyService(db).create_company(user_complete.company)
    id_company = CompanyService(db).get_company_by_name(user_complete.company.name).id
    ## Create User
    hashed_password = get_password_hash(user_complete.user.password)
    new_user = User(
        username=user_complete.user.username,
        password=hashed_password,
        email=user_complete.user.email,
        company_id=id_company)
    UserService(db).create_user(new_user)
    id_user = UserService(db).get_user_by_username(new_user.username).id
    ## Create Rig
    new_rig = Rig(name=user_complete.rig.name, company_id=id_company, user_id=id_user)
    RigService(db).create_rig(new_rig)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "User Complete created"})
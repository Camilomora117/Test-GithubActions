from fastapi import APIRouter
from fastapi import Depends, Path, Body, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List
from models.rig import Rig as RigModel
from schemas.rig import Rig
from services.rig import RigService

from middlewares.jwt_bearer import JWTBearer
from config.database import Session

rig_router = APIRouter()

@rig_router.get(
        path='/rigs', tags=['rigs'], 
        response_model=List[Rig], 
        status_code=status.HTTP_200_OK, 
        summary="Get All Rigs",
        dependencies=[Depends(JWTBearer())])
def get_rigs():
    db = Session()
    result = RigService(db).get_rigs()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@rig_router.get(
        path='/rigs/{id}', 
        tags=['rigs'], 
        response_model=Rig,
        status_code=status.HTTP_200_OK,
        summary="Get rig by id",
        dependencies=[Depends(JWTBearer())])
def get_rig_by_id(id: int = Path(...)):
    db = Session()
    result = RigService(db).get_rig(id)
    if not result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rig not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@rig_router.put(
        path='/rigs/{id}', 
        tags=['rigs'], 
        response_model=dict, 
        status_code=status.HTTP_200_OK,
        summary="Update a rig",
        dependencies=[Depends(JWTBearer())])
def update_company(id: int = Path(...), rig: Rig = Body(...)):
    db = Session()
    result = RigService(db).get_rig(id)
    if not result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rig not found")
    RigService(db).update_rig(id, rig)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Modified rig"})

@rig_router.delete(
        path='/rigs/{id}', 
        tags=['rigs'], 
        response_model=dict, 
        status_code=status.HTTP_200_OK,
        summary="Delete a rig",
        dependencies=[Depends(JWTBearer())])
def delete_company(id: int = Path(...)):
    db = Session()
    result = RigService(db).get_rig(id)
    if not result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rig not found")
    RigService(db).delete_rig(id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Deleted rig"})

@rig_router.post(
        path='/rigs', 
        tags=['rigs'], 
        response_model=dict, 
        status_code=status.HTTP_201_CREATED,
        summary="Create a new Rig",
        dependencies=[Depends(JWTBearer())])
def create_rig(rig: Rig):
    db = Session()
    RigService(db).create_rig(rig)    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Rig Created"})

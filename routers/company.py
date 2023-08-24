from fastapi import APIRouter
from fastapi import Depends, Path, Body, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from typing import List
from models.company import Company as CompanyModel
from schemas.company import Company
from services.company import CompanyService
from middlewares.jwt_bearer import JWTBearer
from config.database import Session

company_router = APIRouter()

@company_router.get(
        path='/companies', tags=['companies'], 
        response_model=List[Company], 
        status_code=status.HTTP_200_OK, 
        summary="Get All Companies")
def get_companies():
    db = Session()
    result = CompanyService(db).get_companies()
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@company_router.get(
        path='/companies/{id}', 
        tags=['companies'], 
        response_model=Company,
        status_code=status.HTTP_200_OK,
        summary="Get companies by id",
        dependencies=[Depends(JWTBearer())])
def get_company_by_id(id: int = Path(...)):
    db = Session()
    result = CompanyService(db).get_company(id)
    if not result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    return JSONResponse(status_code=status.HTTP_200_OK, content=jsonable_encoder(result))

@company_router.post(
        path='/companies', 
        tags=['companies'], 
        response_model=dict, 
        status_code=status.HTTP_201_CREATED,
        summary="Create a new Company",
        dependencies=[Depends(JWTBearer())])
def create_company(company: Company):
    db = Session()
    CompanyService(db).create_company(company)    
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"message": "Company Created"})

@company_router.put(
        path='/companies/{id}', 
        tags=['companies'], 
        response_model=dict, 
        status_code=status.HTTP_200_OK,
        summary="Update a company",
        dependencies=[Depends(JWTBearer())])
def update_company(id: int = Path(...), com: Company = Body(...)):
    db = Session()
    result = CompanyService(db).get_company(id)
    if not result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    CompanyService(db).update_company(id, com)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Modified company"})

@company_router.delete(
        path='/companies/{id}', 
        tags=['companies'], 
        response_model=dict, 
        status_code=status.HTTP_200_OK,
        summary="Delete a company",
        dependencies=[Depends(JWTBearer())])
def delete_company(id: int = Path(...)):
    db = Session()
    result = CompanyService(db).get_company(id)
    if not result:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Company not found")
    CompanyService(db).delete_company(id)
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Deleted company"})
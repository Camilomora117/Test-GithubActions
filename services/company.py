from schemas.company import Company
from models.company import Company as CompanyModel
from utils.jwt_manager import verify_password

class CompanyService():
    
    def __init__(self, db) -> None:
        self.db = db

    def get_companies(self):
        result = self.db.query(CompanyModel).all()
        return result

    def get_company(self, id):
        result = self.db.query(CompanyModel).filter(CompanyModel.id == id).first()
        return result
    
    def get_company_by_name(self, name):
        result = self.db.query(CompanyModel).filter(CompanyModel.name == name).first()
        return result

    def create_company(self, company: Company):
        new_company = CompanyModel(**company.dict())
        self.db.add(new_company)
        self.db.commit()
        return new_company

    def update_company(self, id: int, company: Company):
        company_db = self.db.query(CompanyModel).filter(CompanyModel.id == id).first()
        company_db.name = company.name
        company_db.description = company.description
        company_db.email = company.email
        company_db.phone = company.phone
        self.db.commit()
        return

    
    def delete_company(self, id: int):
       self.db.query(CompanyModel).filter(CompanyModel.id == id).delete()
       self.db.commit()
       return
    
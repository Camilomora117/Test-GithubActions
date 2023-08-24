from schemas.rig import Rig
from models.rig import Rig as RigModel
from utils.jwt_manager import verify_password

class RigService():
    
    def __init__(self, db) -> None:
        self.db = db

    def get_rigs(self):
        result = self.db.query(RigModel).all()
        return result

    def get_rig(self, id):
        result = self.db.query(RigModel).filter(RigModel.id == id).first()
        return result

    def create_rig(self, rig: Rig):
        new_rig = RigModel(**rig.dict())
        self.db.add(new_rig)
        self.db.commit()
        rig_db = self.db.query(RigModel).filter(RigModel.name == new_rig.name).first()
        rig_db.name = "IndependenceRig" + str(rig_db.id)
        self.db.commit()
        return new_rig

    def update_rig(self, id: int, rig: Rig):
        rig_db = self.db.query(RigModel).filter(RigModel.id == id).first()
        rig_db.name = rig.name
        rig_db.company_id = rig.company_id
        rig_db.user_id = rig.user_id
        self.db.commit()
        return
    
    def delete_rig(self, id: int):
       self.db.query(RigModel).filter(RigModel.id == id).delete()
       self.db.commit()
       return
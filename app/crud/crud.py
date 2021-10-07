from typing import Any, Optional

from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.locations import Locations
from app.models.messages import Messages
from app.models.patients import Patients
from app.models.plans import Plans
from app.models.providers import Providers
from app.models.responses import Responses
from app.models.visits import Visits
from app.utils.enums import Reasons, MessageTypes


class CRUDLocations(CRUDBase[Locations]):
    def get(self, db: Session, id: Any) -> Optional[Locations]:
        return db.query(self.model).filter(self.model.LocationID == id).first()

    def exists(self, db: Session, id: Any) -> bool:
        new_id = (
            id.partition(" ")[0].replace("(", "").replace(")", "") if "(" in id else id
        )
        return self.get(db=db, id=new_id) is not None


locations = CRUDLocations(Locations)


class CRUDMessages(CRUDBase[Messages]):
    def get(self, db: Session, id: Any) -> Optional[Messages]:
        return db.query(self.model).filter(self.model.MessageID == id).first()

    def exists(
        self, db: Session, id: Any, type: MessageTypes = 0, reason: Reasons = None
    ) -> bool:
        if reason:
            return (
                db.query(self.model)
                .filter(self.model.VisitID == id)
                .filter(self.model.TypeID == type.value)
                .filter(self.model.ReasonID == reason.value)
                .first()
                is not None
            )
        return (
            db.query(self.model)
            .filter(self.model.VisitID == id)
            .filter(self.model.TypeID == type.value)
            .first()
            is not None
        )


messages = CRUDMessages(Messages)


class CRUDPatients(CRUDBase[Patients]):
    def get(self, db: Session, id: Any) -> Optional[Patients]:
        return db.query(self.model).filter(self.model.PatientID == id).first()

    def has_landline(self, db: Session, id: Any) -> bool:
        patient = self.get(db=db, id=id)
        return patient.PhoneType == 2


patients = CRUDPatients(Patients)


class CRUDPlans(CRUDBase[Plans]):
    def get(self, db: Session, id: Any) -> Optional[Plans]:
        return db.query(self.model).filter(self.model.PlanID == id).first()


plans = CRUDPlans(Plans)


class CRUDProviders(CRUDBase[Providers]):
    def get(self, db: Session, id: Any) -> Optional[Providers]:
        return db.query(self.model).filter(self.model.ProviderID == id).first()

    def get_by_names(self, db: Session, name: str) -> Optional[Providers]:
        last_name, first_middle = name.split(",")
        if first_middle.contains(" "):
            first_name, middle_name = first_middle.split(" ")
        else:
            first_name = first_middle
            middle_name = ""
        provider = (
            db.query(self.model)
            .filter(self.model.ProviderFirst == first_name)
            .filter(self.model.ProviderLast == last_name)
            .first()
        )
        return provider


providers = CRUDProviders(Providers)


class CRUDResponses(CRUDBase[Responses]):
    def get(self, db: Session, id: Any) -> Optional[Responses]:
        return db.query(self.model).filter(self.model.ID == id).first()


responses = CRUDResponses(Responses)


class CRUDVisits(CRUDBase[Visits]):
    def get(self, db: Session, id: Any) -> Optional[Visits]:
        return db.query(self.model).filter(self.model.VisitID == id).first()


visits = CRUDVisits(Visits)

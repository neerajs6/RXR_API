from extensions import db
from sqlalchemy import asc, desc

class Dob(db.Model):
    __tablename__ = 'dob_data'
    id = db.Column(db.Integer, primary_key=True)
    BOROUGH = db.Column(db.Integer)
    Job_Type = db.Column(db.String(50))
    Block = db.Column(db.Integer)
    Lot = db.Column(db.Integer)
    Zip_Code = db.Column(db.Float)
    Work_Type = db.Column(db.String(50))
    Permit_Status = db.Column(db.String(50))
    Filing_Status = db.Column(db.String(50))
    Permit_Type = db.Column(db.String(50))
    Permit_Subtype = db.Column(db.String(50))
    Issuance_Date = db.Column(db.String(50))
    Expiration_Date = db.Column(db.String(50))
    Job_Start_Date = db.Column(db.String(50))
    LATITUDE = db.Column(db.Float)
    LONGITUDE = db.Column(db.Float)
    COUNCIL_DISTRICT = db.Column(db.Float)
    CENSUS_TRACT = db.Column(db.Float)
    NTA_NAME = db.Column(db.String(50))
    year = db.Column(db.Integer)
    BBL = db.Column(db.Integer)

    @classmethod
    def get_by_year(cls, year):
        return cls.query.filter_by(year=year)

    @classmethod
    def get_by_BBL(cls, BBL):
        return cls.query.filter_by(BBL=BBL)

    @classmethod
    def get_all(cls,page, per_page):
        return cls.query.filter_by(year=2020).paginate(page=page, per_page=per_page)


    def save(self):
        db.session.add(self)
        db.session.commit()

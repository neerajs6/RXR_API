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
    def get_by_year(cls, year, page, per_page):
        return cls.query.filter_by(year=year)

    @classmethod
    def get_by_BBL(cls, BBL):
        return cls.query.filter_by(BBL=BBL).first()

    @classmethod
    def get_all(cls):
        return cls.query.filter_by(year=2020).order_by(desc(cls.id))

    def data(self):
        return {
            'id': self.id,
            'BOROUGH': self.BOROUGH,
            'Job_Type': self.Job_Type,
            'Block': self.Block,
            'Lot': self.Lot,
            'Zip_Code': self.Zip_Code,
            'Work_Type': self.Work_Type,
            'Permit_Status': self.Permit_Status,
            'Filing_Status': self.Filing_Status,
            'Permit_Type': self.Permit_Type,
            'Permit_Subtype': self.Permit_Subtype,
            'Issuance_Date': self.Issuance_Date,
            'Expiration_Date': self.Expiration_Date,
            'Job_Start_Date': self.Job_Start_Date,
            'LATITUDE': self.LATITUDE,
            'LONGTUDE': self.LONGITUDE,
            'COUNCIL_DISTRICT': self.COUNCIL_DISTRICT,
            'CENSUS_TRACT': self.CENSUS_TRACT,
            'NTA_NAME': self.NTA_NAME,
            'year': self.year,
            'BBL': self.BBL
        }


    def save(self):
        db.session.add(self)
        db.session.commit()

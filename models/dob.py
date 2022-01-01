from extensions import db
from sqlalchemy import  or_


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
    def get_by_year(cls, year,page,per_page):
        return cls.query.filter_by(year=year).paginate(page=page, per_page=per_page)

    @classmethod
    def get_by_BBL(cls, BBL,page,per_page):
        return cls.query.filter_by(BBL=BBL).paginate(page=page, per_page=per_page)

    @classmethod
    def get_all2(cls, q1,q2, page, per_page):
        keyword1 = '%{keyword1}%'.format(keyword1=q1)
        keyword2 = '%{keyword2}%'.format(keyword2=q2)
        return cls.query.filter(cls.year.ilike(q1)).filter(
                                    cls.BBL.ilike(q2)).paginate(page=page, per_page=per_page)



def save(self):
        db.session.add(self)
        db.session.commit()

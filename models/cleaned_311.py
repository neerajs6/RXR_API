from extensions import db
from sqlalchemy import or_


class Cleaned_311(db.Model):
    __tablename__ = '311_cleaned_data'
    UNIQUE_KEY = db.Column(db.Integer, primary_key=True)
    CREATED_DATE = db.Column(db.DateTime)
    CLOSED_DATE = db.Column(db.DateTime)
    AGENCY = db.Column(db.String(50))
    AGENCY_NAME = db.Column(db.String(50))
    COMPLAINT_TYPE = db.Column(db.String(50))
    DESCRIPTOR = db.Column(db.String(50))
    LOCATION_TYPE = db.Column(db.String(50))
    INCIDENT_ZIP = db.Column(db.String(50))
    INCIDENT_ADDRESS = db.Column(db.String(50))
    STREET_NAME = db.Column(db.String(50))
    CROSS_STREET_1 = db.Column(db.String(50))
    CROSS_STREET_2 = db.Column(db.String(50))
    INTERSECTION_STREET_1 = db.Column(db.String(50))
    INTERSECTION_STREET_2 = db.Column(db.String(50))
    CITY = db.Column(db.String(50))
    LANDMARK = db.Column(db.String(50))
    STATUS = db.Column(db.String(50))
    BBL = db.Column(db.Integer)
    BOROUGH = db.Column(db.String(50))
    X_COORD_STATE_PLANE = db.Column(db.Float)
    Y_COORD_STATE_PLANE = db.Column(db.Float)
    OPEN_DATA_CHANNEL_TYPE = db.Column(db.String(50))
    PARK_FACILITY_NAME = db.Column(db.String(50))
    PARK_BOROUGH= db.Column(db.String(50))
    LATITUDE = db.Column(db.Float)
    LONGITUDE = db.Column(db.Float)
    coordinates = db.Column(db.String(50))
    CTYPE = db.Column(db.String(50))
    YEAR = db.Column(db.Integer)
    MONTH = db.Column(db.Integer)
    CTYPE_LOWER= db.Column(db.String(50))

    @classmethod
    def get_all(cls,q,page, per_page):
        keyword = '%{keyword}%'.format(keyword=q)
        return cls.query.filter(or_(cls.YEAR.ilike(keyword) ,
                                    cls.BBL.ilike(keyword))).paginate(page=page, per_page=per_page)


    @classmethod
    def get_all2(cls, q1,q2, page, per_page):
        keyword1 = '%{keyword1}%'.format(keyword1=q1)
        keyword2 = '%{keyword2}%'.format(keyword2=q2)
        return cls.query.filter(cls.YEAR.ilike(q1)).filter(
                                    cls.BBL.ilike(q2)).paginate(page=page, per_page=per_page)



def save(self):
        db.session.add(self)
        db.session.commit()

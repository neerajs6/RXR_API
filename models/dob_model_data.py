from extensions import db
from sqlalchemy import  or_


class Dob_Model_Data(db.Model):
    __tablename__ = 'dob_data_for_the_model'
    year = db.Column(db.Integer)
    BBL = db.Column(db.Integer)
    A1_AL = db.Column(db.Float)
    A1_EQ = db.Column(db.Float)
    A1_FO = db.Column(db.Float)
    A1_FP = db.Column(db.Float)
    A1_PL = db.Column(db.Float)
    A1_SD = db.Column(db.Float)
    A1_SP = db.Column(db.Float)
    A2_BL = db.Column(db.Float)
    A2_EQ = db.Column(db.Float)
    A2_EW = db.Column(db.Float)
    A2_FA = db.Column(db.Float)
    A2_FB = db.Column(db.Float)
    A2_FP = db.Column(db.Float)
    A2_FS = db.Column(db.Float)
    A2_MH = db.Column(db.Float)
    A2_PL = db.Column(db.Float)
    A2_SD = db.Column(db.Float)
    A2_SP = db.Column(db.Float)
    A3_AL = db.Column(db.Float)
    A3_CC = db.Column(db.Float)
    A3_EQ = db.Column(db.Float)
    A3_FO = db.Column(db.Float)
    DM_DM = db.Column(db.Float)
    DM_EQ = db.Column(db.Float)
    NB_EQ = db.Column(db.Float)
    NB_FO = db.Column(db.Float)
    NB_NB = db.Column(db.Float)
    NB_PL = db.Column(db.Float)
    NB_SD = db.Column(db.Float)
    NB_SP = db.Column(db.Float)
    SG_EQ = db.Column(db.Float)
    SG_SG = db.Column(db.Float)
    unique_ID = db.Column(db.Integer, primary_key=True)

    @classmethod
    def get_all(cls,q,page, per_page):
        keyword = '%{keyword}%'.format(keyword=q)
        return cls.query.filter(or_(cls.year.ilike(keyword) ,
                                    cls.BBL.ilike(keyword))).paginate(page=page, per_page=per_page)


    @classmethod
    def get_all2(cls, q1,q2, page, per_page):
        keyword1 = '%{keyword1}%'.format(keyword1=q1)
        keyword2 = '%{keyword2}%'.format(keyword2=q2)
        return cls.query.filter(cls.year.ilike(q1)).filter(
                                    cls.BBL.ilike(q2)).paginate(page=page, per_page=per_page)



def save(self):
        db.session.add(self)
        db.session.commit()

from extensions import db
from sqlalchemy import or_


class Embeddings_311(db.Model):
    __tablename__ = '311_embeddings'
    CTYPE_LOWER = db.Column(db.String(50), primary_key=True)
    CLUSTER = db.Column(db.Integer)
    EMBEDDING = db.Column(db.String(50))

    @classmethod
    def get_all(cls,q,page, per_page):
        keyword = '%{keyword}%'.format(keyword=q)
        return cls.query.filter(or_(cls.CTYPE_LOWER.ilike(keyword) ,
                                    cls.CLUSTER.ilike(keyword)),
                                    cls.EMBEDDING.ilike(keyword)).paginate(page=page, per_page=per_page)


    '''@classmethod
    def get_all2(cls, q1,q2, page, per_page):
        keyword1 = '%{keyword1}%'.format(keyword1=q1)
        keyword2 = '%{keyword2}%'.format(keyword2=q2)
        return cls.query.filter(cls.YEAR.ilike(q1)).filter(
                                    cls.BBL.ilike(q2)).paginate(page=page, per_page=per_page)'''



def save(self):
        db.session.add(self)
        db.session.commit()

from marshmallow import Schema, fields, post_dump, validate, validates,ValidationError
from schemas.pagination import PaginationSchema

class DobSchema(Schema):
    class Meta:
        ordered = True

        id = fields.Integer(dump_only=True)
        BOROUGH = fields.Integer()
        Job_Type = fields.String(validate=[validate.Length(max=50)])
        Block = fields.Integer()
        Lot = fields.Integer()
        Zip_Code = fields.Float()
        Work_Type = fields.String(validate=[validate.Length(max=50)])
        Permit_Status = fields.String(validate=[validate.Length(max=50)])
        Filing_Status = fields.String(validate=[validate.Length(max=50)])
        Permit_Type = fields.String(validate=[validate.Length(max=50)])
        Permit_Subtype = fields.String(validate=[validate.Length(max=50)])
        Issuance_Date = fields.String(validate=[validate.Length(max=50)])
        Expiration_Date = fields.String(validate=[validate.Length(max=50)])
        Job_Start_Date = fields.String(validate=[validate.Length(max=50)])
        LATITUDE = fields.Float()
        LONGITUDE = fields.Float()
        COUNCIL_DISTRICT = fields.Float()
        CENSUS_TRACT = fields.Float()
        NTA_NAME = fields.String(validate=[validate.Length(max=50)])
        year = fields.Float()
        BBL = fields.Float()

class DobPaginationSchema(PaginationSchema):
    data = fields.Nested(DobSchema,attribute='items', many = True)

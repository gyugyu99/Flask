from marshmallow import Schema, fields

class BookSchema(Schema):
    #서버에서 직접 관리를 한다! dump_only=True
    id = fields.Int(dump_only=True)

    title = fields.Str(required=True)
    author = fields.Str(required=True)
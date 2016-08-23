from peewee import *

database = SqliteDatabase('kingco_parcels.sqlite')

class BaseModel(Model):
  class Meta:
    database = database


class Parcel(BaseModel):
  parcel_id = IntegerField()
  formatted_address = CharField()
  address = CharField()
  zip_code = CharField()
  lot_sq_ft = IntegerField()
  appraised_value = IntegerField(null=True)
  present_use = CharField()
  latitude = FloatField()
  longitude = FloatField()


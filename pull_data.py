import requests
from models import Parcel
import urllib
from peewee import DoesNotExist

GMAPS_GEOCODING_API = 'AIzaSyCMjs-apSxTt2oWS_6tkBogUtrB7paq29Q'


Parcel.create_table(fail_silently=True)

search_term = '98004'

url = 'http://gismaps.kingcounty.gov/parcelviewer2/addSearchHandler.ashx?add=98004'


resp = requests.get(url)

parcels = resp.json()['items']
for parcel in parcels:
  parcel_dict = {
    'parcel_id': parcel['PIN'],
    'address': parcel['ADDRESS'],
    'zip_code': parcel['ZIPCODE']
  }

  try:
    Parcel.get(Parcel.parcel_id == int(parcel['PIN']))
  except DoesNotExist:

    parcel_detail_url = 'http://gismaps.kingcounty.gov/parcelviewer2/pvinfoquery.ashx?pin=%s' % parcel['PIN']
    resp = requests.get(parcel_detail_url)


    detail = resp.json()['items'][0]

    parcel_dict['present_use'] = detail['PRESENTUSE']
    parcel_dict['lot_sq_ft'] = int(detail['LOTSQFT'])

    if not detail['APPVALUE'] == '':
      parcel_dict['appraised_value'] = int(detail['APPVALUE'])

    url_params = {
      'address': parcel_dict['address'] + ', ' + parcel_dict['zip_code'],
      'key': GMAPS_GEOCODING_API
    }
    resp = requests.get('https://maps.googleapis.com/maps/api/geocode/json?' + urllib.urlencode(url_params))

    # print resp.text

    geo_api_results = resp.json()['results']
    if len(geo_api_results) == 1:
      parcel_dict['formatted_address'] = geo_api_results[0]['formatted_address']
      parcel_dict['latitude'] = geo_api_results[0]['geometry']['location']['lat']
      parcel_dict['longitude'] = geo_api_results[0]['geometry']['location']['lng']

    print parcel_dict
    Parcel.create(**parcel_dict)
    break




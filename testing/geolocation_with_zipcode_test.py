# Importing required module
import geopy
from geopy.geocoders import Nominatim

# Using Nominatim Api
geopy.geocoders.options.default_user_agent = "locations-application"
geolocator = Nominatim()

# Zipcode input
zipcode = '60 Malboro Street'

# Using geocode()
location = geolocator.geocode(zipcode, addressdetails=True)
location = location.raw['address']

print("Details of the Zipcode:")
if location['region']:
    print(location['region'])
print(location)

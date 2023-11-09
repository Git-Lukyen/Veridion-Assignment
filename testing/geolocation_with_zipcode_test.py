# Importing required module
import geopy
from geopy.geocoders import Nominatim

# Using Nominatim Api
geopy.geocoders.options.default_user_agent = "locations-application"
geolocator = Nominatim()

# Zipcode input
zipcode = 'PO BOX 3411, CO 81435'

# Using geocode()
location = geolocator.geocode(zipcode, addressdetails=True)
location = location.raw['address']

print("Details of the Zipcode:")
print(location)

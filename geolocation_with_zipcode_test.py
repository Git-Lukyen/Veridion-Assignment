# Importing required module
import geopy
from geopy.geocoders import Nominatim

# Using Nominatim Api
geopy.geocoders.options.default_user_agent = "locations-application"
geolocator = Nominatim()

# Zipcode input
zipcode = "USA 60195"

# Using geocode()
location = geolocator.geocode(zipcode)

print("Details of the Zipcode:")
print(location)

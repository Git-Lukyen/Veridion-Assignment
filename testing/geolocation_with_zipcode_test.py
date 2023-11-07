# Importing required module
import geopy
from geopy.geocoders import Nominatim

# Using Nominatim Api
geopy.geocoders.options.default_user_agent = "locations-application"
geolocator = Nominatim()

# Zipcode input
zipcode = "4640 Wyandotte Dr"

# Using geocode()
location = geolocator.geocode(zipcode, addressdetails=True)

print("Details of the Zipcode:")
print(location)

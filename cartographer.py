import os
import json
from pyicloud import PyiCloudService
from math import pi, sqrt, sin, cos, atan2


class Cartographer(object):


    def get_ra_iphone_coords(self):
        location_dict = {}
        with open(
            os.path.expanduser('~') + "/.rabot/iphone_ra_location.json", "r"
        ) as iphone_ra_location_file:
            location_dict = json.loads(iphone_ra_location_file.read())
        coords = (location_dict['latitude'], location_dict['longitude'])
        return coords


    def get_maps_api_key(self):
        api_key = ""
        with open(os.path.expanduser('~') + "/.google/map-api.conf", "r") as conf_file:
            api_key = json.loads(conf_file.read())['api-key']
        return api_key


    def update_location(self):
        with open(os.path.expanduser('~') + '/.rabot/icloud.conf', 'r') as icloud_file:
            icloud_config = icloud_file.read().rstrip('\n').split(',')
        api = PyiCloudService(*icloud_config)
        print("[LOG] Querying device via iCloud")
        iphone_ra = api.devices['6bVMcYPLaUNZIB3AYAUFpkeoUDLTkf4opPflqToK7apYS9ujn5gNiOHYVNSUzmWV']
        iphone_ra_location = iphone_ra.location()
        if iphone_ra_location is None:
            print("[ERROR] location was not available right now")
        else:
            with open(
                os.path.expanduser('~') + "/.rabot/iphone_ra_location.json", "w"
            ) as iphone_ra_location_file:
                iphone_ra_location_file.write(json.dumps(iphone_ra_location))


    def haversine(self, pos1, pos2):
        '''calculate the distance between two lat/long positions'''
        lat1 = float(pos1['lat'])
        long1 = float(pos1['long'])
        lat2 = float(pos2['lat'])
        long2 = float(pos2['long'])

        degree_to_rad = float(pi / 180.0)

        d_lat = (lat2 - lat1) * degree_to_rad
        d_long = (long2 - long1) * degree_to_rad

        a = pow(sin(d_lat / 2), 2) + cos(lat1 * degree_to_rad) * \
            cos(lat2 * degree_to_rad) * pow(sin(d_long / 2), 2)
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        km = 6367 * c
        mi = 3956 * c

        return {"km": km, "miles": mi}


if __name__ == "__main__":
    cort = Cartographer()
    # resptext = cart.get_map_at_coords(cart.get_ra_iphone_coords())
    resptext = cort.get_maps_api_key()
    print(resptext)

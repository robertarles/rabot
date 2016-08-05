import os
import json


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


if __name__ == "__main__":
    cart = Cartographer()
    # resptext = cart.get_map_at_coords(cart.get_ra_iphone_coords())
    resptext = cart.get_maps_api_key()
    print(resptext)

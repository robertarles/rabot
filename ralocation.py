import json
import os
from pyicloud import PyiCloudService


def update_location():
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

if __name__ == '__main__':
    update_location()

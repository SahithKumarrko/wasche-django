import pytz
class settings:
    plan = {"Silver" : {"cost":849,"details":["Upper Wear - 65","Lower Wear - 65","Lower Wear - 65","Other - 15"]},"Gold" : {"cost":999,"details":["Upper Wear - 75","Lower Wear - 75","Lower Wear - 75","Other - 20"]},"Platinum" : {"cost":1299,"details":["Upper Wear - 90","Lower Wear - 90","Lower Wear - 90","Other - 30"]}}
    ist_info = pytz.timezone('Asia/Kolkata')
    secret_key="6729fa7a6f252cf7663f040f4cf937f2206be6e5"
    appId = "12168bced56b2d76070a9fb7c86121"
    regular_count = {"Silver":215,"Platinum":300,"Gold":245}
    other_count = 50
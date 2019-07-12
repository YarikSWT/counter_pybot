import datetime
from dateutil.relativedelta import *

delta = datetime.timedelta(days=30)

d = datetime.datetime.now()

new_d = d + delta

print(new_d, type(new_d))

t = datetime.time(int("08"), int("29"))

print(t)

new_d = d + relativedelta(months=+1)

print(new_d)


DATEBASE_URL="mysql://bd01d531c9c90d:f492d42a@eu-cdbr-west-02.cleardb.net/heroku_c1325c69ad61dfe?reconnect=true".split('?')[0]
print(DATEBASE_URL)


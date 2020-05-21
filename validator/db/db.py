from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

host = 'ia360-currentprod.cw0g3uulplsy.us-east-2.rds.amazonaws.com'
# host = 'hotel-staging-db.cw0g3uulplsy.us-east-2.rds.amazonaws.com'
# host = 'air-dev.cw0g3uulplsy.us-east-2.rds.amazonaws.com'
port = '5432'
user = 'AdvitoAdmin'
pwd = 'B!3k_8cr'

advito_db = 'advito'
hotel_db = 'hotel'

AdvitoEngine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
    user, pwd, host, port, advito_db))
AdvitoSession = sessionmaker(bind=AdvitoEngine)

HotelEngine = create_engine('postgresql://{}:{}@{}:{}/{}'.format(
    user, pwd, host, port, hotel_db))
HotelSession = sessionmaker(bind=HotelEngine)

import random
from datetime import date
from app import db, Data_table

db.drop_all()
db.create_all()
names_list = ['T-shirt', 'chemise', 'kimono', 'overalls', 'swing-blouse', 'fancy dress', 'dress', 'babydoll dress',
              'cocktail dress', 'sari', 'wrap dress', 'jogging suit', 'cardigan', 'blazer', 'vest', 'sundress',
              'blouse', 'camisole', 'sweatshirt', 'evening dress', 'shirt', 'sweater', 'suit']

db_list = []
for i in names_list:
    m = Data_table(date=date(random.randint(2000, 2022), random.randint(1, 12), random.randint(1, 28)),
                   name=i,
                   amount=random.randint(20, 300),
                   distance=random.randint(1, 500))

    db.session.add(m)
db.session.commit()

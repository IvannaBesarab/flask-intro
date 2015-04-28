from app import db
from models import BlogPost
from 

#create the database and db tables
db.create_all()


#insert
db.session.add(BlogPost('Good', 'I\; doing very good'))
db.session.add(BlogPost('Well', 'I\; doing suoer well'))

#commit the changes
db.session.commit()
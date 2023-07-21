from dataclasses import dataclass
import sys
from sqlalchemy import URL

# for creating the mapper code
from sqlalchemy import Column, ForeignKey, Integer, String
# for configuration and class code
from sqlalchemy.ext.declarative import declarative_base
# for creating foreign key relationship between the tables
from sqlalchemy.orm import relationship
# for configuration
from sqlalchemy import create_engine
# create declarative_base instance
Base = declarative_base()
# we'll add classes here
# creates a create_engine instance at the bottom of the file
url_object = URL.create(
    "mysql+mysqlconnector",
    username='root', password='root',
    host='localhost',
    database='internet_store'
)
engine = create_engine(url_object)
Base.metadata.create_all(engine)


@dataclass
class Product(Base):
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    price = Column(Integer)

# Imported to define datatypes.
from sqlalchemy import Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
# Imported to create database in app.  Here is where SQLite & PostgreSQL differ.
from sqlalchemy import create_engine

# Necessary class instance for SQLite databases.
Base = declarative_base() 
class Venue(Base): # Define Venue class that inherits Base class's attributes.
  # Name table this Class is creating/representing.
  __tablename__ = 'venue'

  # Define columns and their respective datatypes.
  id = Column(Integer, primary_key = True)
  venue_name = Column(String)
  venue_address = Column(String)
  venue_image = Column(String)
  
  
  # Add a property decorator to serialize information from this database.
  # Properties are a simple way to return a computed value from an attribute, 
  # read, or call a function on an attribute write.
  @property # descriptor
  def serialize(self):
    return {
      'venue_name': self.venue_name,
      'venue_address': self.venue_address,
      'venue_image' : self.venue_image,
      'id' : self.id
      }

engine = create_engine('sqlite:///venues.db')
 
# Create database.
Base.metadata.create_all(engine)

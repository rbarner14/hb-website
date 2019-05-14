# Imported from findAVenue.py to find venue data to populate our 
from findAVenue import findAVenue
# Database object classes Base and Venue from models.py are used to fulfill
# client requests.
from model import Base, Venue

# Imported to instantiate app (Flask), jsonify results to make them readible by
# front end (jsnoify), and get and update data from database/to endpoints.
from flask import Flask, jsonify, request

# Imported to complete queries of database and establish relationships between 
# tables in database.
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

# import sys
# import codecs
# sys.stdout = codecs.getwriter('utf8')(sys.stdout)
# sys.stderr = codecs.getwriter('utf8')(sys.stderr)


# API Keys
foursquare_client_id = 'QVY0YIACTYI30DRWLK4ZUNT1KFQHAPGPOBKEM5DYWL0CLEJN'
foursquare_client_secret = 'WRCP40LWD1NO0KUEGWINKMQNWO5HCSM4TYUDZCHUMYEMTIKP'
google_api_key = 'AIzaSyBKoTTTlfbbk0wKLFISgiJx_4jCYOdLwZs'

# Create engine by referencing SQLite database venues.db created with
# models.py.  Alternative: PostgreSQL.
engine = create_engine('sqlite:///venues.db')

# Prepare database for use in app (connect to app).
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
# Imported for SQLAlchemy queries and requests.

session = DBSession() 
# Instantiate Flask app.
app = Flask(__name__)

# App decorator to set up venue route that accepts 'GET' (show) and 'POST'
# (update) method requests.
@app.route('/venues', methods = ['GET', 'POST'])
def all_venues_handler():
    # Return all venuess in database.
    # If request method is GET, run a query on the database's Venue table
    # (Class) for all venues. Return value is a list of Venue objects.
    # if request.method == 'GET':

    #     venues = session.query(Venue).all()
    #     print(venues)

    #     # Query results (variable venues which is a list data type) are
    #     # serialized, or, made into a dictionary then added to a list via a list
    #     # comprehension.  This list is then jsonfied for injestion by front end.
    #     return jsonify(venues=[i.serialize for i in venues])

    # # Make a new venue and store it in the database.
    if request.method == 'GET':
        # Flask.Request.args creates a MultiDict (dictionary subclass customized
        # to deal with multiple values for the same key which, is used by the
        # parsing functions in the wrappers. This is necessary because some HTML
        # form elements pass multiple values for the same key.) with the parsed
        # contents of the query string (strings in the URL after the "?").
        # Prototype: get(key, default=None, type=None)
        location = request.args.get('location', '')
        features = request.args.get('features', '')

        # Create venue_info variable by calling the imported
        # findAVenue function.
        venue_info = findAVenue(features, location)

        # If there is venue info, create a venue variable that is
        # equal to the instantiation of the Venue Class defined in our
        # model(models.py).
        if venue_info != "No Venues Found":
            venue = Venue(venue_name=venue_info['name'],
                          venue_address=venue_info['address'],
                          venue_image=venue_info['image'])
            # Add venue variable just created to session.
            # session.add(venue)
            # Commit Venue instance (venue variable created) to db.
            # session.commit()

            # Return jsonified dictionary that results when object is serialized
            # via the Venue serialize attribute method.
            return jsonify(venue=venue.serialize)
        else:
            # If no venue data resulted from running findAVenue on
            # the feature and location passed in the address bar upon url
            # request, return error message.
            return jsonify({"error": f"No Venues Found for {features} in {location}"})

# Delete is in red to emphasize impact.
@app.route('/venues/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def venue_handler(id):
    # Return venue database query result as a string, not list, since we
    # are querying for a line item by a specific id and the ids in our database
    # are unique.
    venue = session.query(Venue).filter_by(id=id).one()

    if request.method == 'GET':
        # Return a specific venue.
        return jsonify(venue=venue.serialize)
    elif request.method == 'PUT':
        # Update a specific venue.
        # Method request.args.get is not passed a 2nd parameter of an empty
        # string since we know forsure the venue object being requested is
        # in the database and has an address (actual or empty string) as we are
        # only updating the lineitem in the database (PUT request).
        address = request.args.get('address')
        image = request.args.get('image')
        name = request.args.get('name')

        if address:
            venue.venue_address = address
        if image:
            venue.venue_image = image
        if name:
            venue.venue_name = name
        # Always commit action to database when manipulating it in someway
        # ('PUT', 'POST', 'DELETE')
        session.commit()

        # Jsonify the result of the venue variable that is serialized after
        # applying the serialize method attribute on it.
        return jsonify(venue=venue.serialize)

    elif request.method == 'DELETE':
        # Delete a specific venue.

        # Delete object instance and commit action to session.
        session.delete(venue)
        session.commit()

        # Return message for DevX purposes.
        return "Venue Deleted"


###############################################################################
# To run app at command line.  Debug mode is on.  Web local host # is 0.0.0.0
# and the port to run app on is 5000.
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


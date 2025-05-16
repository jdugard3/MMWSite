"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.models.instrument import Instrument, Guitar, Piano, Drum, Violin, InstrumentType, InstrumentCategory
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


# @api.route('/hello', methods=['POST', 'GET'])
# def handle_hello():
#     response_body = {
#         "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
#     }
#     return jsonify(response_body), 200

# Helper functions for instrument endpoints
def get_instrument_class(instrument_type):
    """Return the appropriate instrument class based on type"""
    type_map = {
        InstrumentType.GUITAR: Guitar,
        InstrumentType.PIANO: Piano, 
        InstrumentType.DRUM: Drum,
        InstrumentType.VIOLIN: Violin
    }
    return type_map.get(instrument_type)

def handle_error(e, status_code=400):
    """Handle errors consistently"""
    db.session.rollback()
    return jsonify({"error": str(e)}), status_code

# Helper to convert string values to enum members
def string_to_instrument_type(value):
    """Convert a string value to an InstrumentType enum member"""
    if not value:
        return None
    
    # Convert to uppercase for enum member lookup
    value = value.upper()
    try:
        return InstrumentType[value]
    except KeyError:
        raise ValueError(f"Invalid instrument type: {value}. Possible values: {', '.join(t.name.lower() for t in InstrumentType)}")

def string_to_instrument_category(value):
    """Convert a string value to an InstrumentCategory enum member"""
    if not value:
        return None
    
    # Convert to uppercase for enum member lookup
    value = value.upper()
    try:
        return InstrumentCategory[value]
    except KeyError:
        raise ValueError(f"Invalid instrument category: {value}. Possible values: {', '.join(c.name.lower() for c in InstrumentCategory)}")

# Instrument endpoints
@api.route('/instruments', methods=['GET'])
def get_instruments():
    """Get all instruments or filter by type"""
    try:
        instrument_type = request.args.get('type')
        query = Instrument.query
        
        if instrument_type:
            type_enum = string_to_instrument_type(instrument_type)
            query = query.filter_by(type=type_enum)
            
        return jsonify([i.serialize() for i in query.all()]), 200
    except ValueError as e:
        return handle_error(e)

@api.route('/instruments/<int:instrument_id>', methods=['GET'])
def get_instrument(instrument_id):
    """Get a specific instrument by ID"""
    instrument = Instrument.query.get(instrument_id)
    
    if not instrument:
        return jsonify({"error": "Instrument not found"}), 404
        
    return jsonify(instrument.serialize()), 200

@api.route('/instruments', methods=['POST'])
def create_instrument():
    """Create a new instrument"""
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        # Convert string type to enum using our helper function
        instrument_type = string_to_instrument_type(data.get('type'))
        instrument_class = get_instrument_class(instrument_type)
        
        if not instrument_class:
            return jsonify({"error": "Invalid instrument type"}), 400
            
        # Remove any None values from data
        clean_data = {k: v for k, v in data.items() if v is not None}
        
        # Remove type and category from clean_data since we'll set them explicitly
        if 'type' in clean_data:
            del clean_data['type']
        if 'category' in clean_data:
            del clean_data['category']
        
        # Set required enums
        clean_data['type'] = instrument_type
        clean_data['category'] = string_to_instrument_category(data.get('category'))
        
        # Create instrument with all provided data
        instrument = instrument_class(**clean_data)
        
        db.session.add(instrument)
        db.session.commit()
        
        return jsonify(instrument.serialize()), 201
        
    except (ValueError, TypeError) as e:
        return handle_error(e)
    except Exception as e:
        return handle_error(e, 500)

@api.route('/instruments/<int:instrument_id>', methods=['PUT'])
def update_instrument(instrument_id):
    """Update an existing instrument"""
    instrument = Instrument.query.get(instrument_id)
    
    if not instrument:
        return jsonify({"error": "Instrument not found"}), 404
        
    data = request.json
    
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    try:
        # Handle enums using our helper functions
        if 'type' in data:
            data['type'] = string_to_instrument_type(data['type'])
            
        if 'category' in data:
            data['category'] = string_to_instrument_category(data['category'])
            
        # Update attributes that match the instrument
        for key, value in data.items():
            if hasattr(instrument, key):
                setattr(instrument, key, value)
        
        db.session.commit()
        return jsonify(instrument.serialize()), 200
        
    except ValueError as e:
        return handle_error(e)
    except Exception as e:
        return handle_error(e, 500)

@api.route('/instruments/<int:instrument_id>', methods=['DELETE'])
def delete_instrument(instrument_id):
    """Delete an instrument"""
    instrument = Instrument.query.get(instrument_id)
    
    if not instrument:
        return jsonify({"error": "Instrument not found"}), 404
        
    try:
        db.session.delete(instrument)
        db.session.commit()
        return jsonify({"success": "Instrument deleted"}), 200
    except Exception as e:
        return handle_error(e, 500)

"""
Instrument API endpoints
"""
from flask import request, jsonify
from . import api
from api.models import db
from api.models.instrument import Instrument, Guitar, Piano, Drum, Violin, InstrumentType, InstrumentCategory
from api.utils import APIException

# Helper functions
def string_to_instrument_type(value):
    """Convert a string value to an InstrumentType enum member"""
    if not value:
        return None
    
    # Convert to uppercase for enum lookup
    value = value.upper()
    try:
        return InstrumentType[value]
    except KeyError:
        raise APIException(f"Invalid instrument type: {value}. Possible values: {', '.join(t.name.lower() for t in InstrumentType)}", status_code=400)

def string_to_instrument_category(value):
    """Convert a string value to an InstrumentCategory enum member"""
    if not value:
        return None
    
    # Convert to uppercase for enum lookup
    value = value.upper()
    try:
        return InstrumentCategory[value]
    except KeyError:
        raise APIException(f"Invalid instrument category: {value}. Possible values: {', '.join(c.name.lower() for c in InstrumentCategory)}", status_code=400)

@api.route('/instruments', methods=['GET'])
def get_instruments():
    """
    Get all instruments or filter by type/category
    """
    instrument_type = request.args.get('type')
    category = request.args.get('category')
    
    query = Instrument.query
    
    if instrument_type:
        type_enum = string_to_instrument_type(instrument_type)
        query = query.filter(Instrument.type == type_enum)
    
    if category:
        category_enum = string_to_instrument_category(category)
        query = query.filter(Instrument.category == category_enum)
    
    instruments = query.all()
    return jsonify([i.serialize() for i in instruments]), 200

@api.route('/instruments/<int:instrument_id>', methods=['GET'])
def get_instrument(instrument_id):
    """
    Get a specific instrument by ID
    """
    instrument = Instrument.query.get(instrument_id)
    
    if not instrument:
        raise APIException('Instrument not found', status_code=404)
    
    return jsonify(instrument.serialize()), 200

@api.route('/instruments', methods=['POST'])
def create_instrument():
    """
    Create a new instrument
    """
    body = request.get_json()
    
    if not body:
        raise APIException('You need to specify the request body as a JSON object', status_code=400)
    
    # Check required fields
    required_fields = ['name', 'brand', 'model', 'price', 'type', 'category']
    for field in required_fields:
        if field not in body:
            raise APIException(f'You need to specify the {field}', status_code=400)
    
    # Convert enum string values to enum objects
    instrument_type_str = body.get('type')
    instrument_type = string_to_instrument_type(instrument_type_str)
    category = string_to_instrument_category(body.get('category'))
    
    # Create a copy of the body without type and category
    instrument_data = body.copy()
    if 'type' in instrument_data:
        del instrument_data['type']
    if 'category' in instrument_data:
        del instrument_data['category']
    
    # Create the appropriate instrument based on type
    if instrument_type == InstrumentType.GUITAR:
        instrument = Guitar(
            type=instrument_type,
            category=category,
            **instrument_data
        )
    elif instrument_type == InstrumentType.PIANO:
        instrument = Piano(
            type=instrument_type,
            category=category,
            **instrument_data
        )
    elif instrument_type == InstrumentType.DRUM:
        instrument = Drum(
            type=instrument_type,
            category=category,
            **instrument_data
        )
    elif instrument_type == InstrumentType.VIOLIN:
        instrument = Violin(
            type=instrument_type,
            category=category,
            **instrument_data
        )
    else:
        raise APIException('Invalid instrument type', status_code=400)
    
    db.session.add(instrument)
    db.session.commit()
    
    return jsonify(instrument.serialize()), 201

@api.route('/instruments/<int:instrument_id>', methods=['PUT'])
def update_instrument(instrument_id):
    """
    Update an existing instrument
    """
    instrument = Instrument.query.get(instrument_id)
    
    if not instrument:
        raise APIException('Instrument not found', status_code=404)
    
    body = request.get_json()
    
    if not body:
        raise APIException('You need to specify the request body as a JSON object', status_code=400)
    
    # Convert enum values if present
    if 'type' in body:
        body['type'] = string_to_instrument_type(body['type'])
    if 'category' in body:
        body['category'] = string_to_instrument_category(body['category'])
    
    # Update base instrument attributes
    for key, value in body.items():
        if hasattr(instrument, key):
            setattr(instrument, key, value)
    
    db.session.commit()
    
    return jsonify(instrument.serialize()), 200

@api.route('/instruments/<int:instrument_id>', methods=['DELETE'])
def delete_instrument(instrument_id):
    """
    Delete an instrument
    """
    instrument = Instrument.query.get(instrument_id)
    
    if not instrument:
        raise APIException('Instrument not found', status_code=404)
    
    db.session.delete(instrument)
    db.session.commit()
    
    return jsonify({"success": True}), 200 
"""
Instrument API endpoints
"""
from flask import request, jsonify
from . import api
from api.models import db, Instrument, Guitar, Piano, Drum, Violin
from api.utils import APIException

@api.route('/instruments', methods=['GET'])
def get_instruments():
    """
    Get all instruments or filter by type/category
    """
    instrument_type = request.args.get('type')
    category = request.args.get('category')
    
    query = Instrument.query
    
    if instrument_type:
        query = query.filter(Instrument.type == instrument_type)
    
    if category:
        query = query.filter(Instrument.category == category)
    
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
    
    # Create the appropriate instrument based on type
    instrument_type = body.get('type')
    
    if instrument_type == 'guitar':
        instrument = Guitar(
            name=body.get('name'),
            brand=body.get('brand'),
            model=body.get('model'),
            price=body.get('price'),
            description=body.get('description', ''),
            image_url=body.get('image_url', ''),
            stock=body.get('stock', 0),
            type=body.get('type'),
            category=body.get('category'),
            num_strings=body.get('num_strings', 6),
            body_type=body.get('body_type', '')
        )
    elif instrument_type == 'piano':
        instrument = Piano(
            name=body.get('name'),
            brand=body.get('brand'),
            model=body.get('model'),
            price=body.get('price'),
            description=body.get('description', ''),
            image_url=body.get('image_url', ''),
            stock=body.get('stock', 0),
            type=body.get('type'),
            category=body.get('category'),
            num_keys=body.get('num_keys', 88),
            is_weighted=body.get('is_weighted', False)
        )
    elif instrument_type == 'drum':
        instrument = Drum(
            name=body.get('name'),
            brand=body.get('brand'),
            model=body.get('model'),
            price=body.get('price'),
            description=body.get('description', ''),
            image_url=body.get('image_url', ''),
            stock=body.get('stock', 0),
            type=body.get('type'),
            category=body.get('category'),
            num_pads=body.get('num_pads', 4),
            num_cymbals=body.get('num_cymbals', 3),
            has_kick=body.get('has_kick', True)
        )
    elif instrument_type == 'violin':
        instrument = Violin(
            name=body.get('name'),
            brand=body.get('brand'),
            model=body.get('model'),
            price=body.get('price'),
            description=body.get('description', ''),
            image_url=body.get('image_url', ''),
            stock=body.get('stock', 0),
            type=body.get('type'),
            category=body.get('category'),
            size=body.get('size', '4/4'),
            bow_included=body.get('bow_included', True)
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
    
    # Update base instrument attributes
    if 'name' in body:
        instrument.name = body['name']
    if 'brand' in body:
        instrument.brand = body['brand']
    if 'model' in body:
        instrument.model = body['model']
    if 'price' in body:
        instrument.price = body['price']
    if 'description' in body:
        instrument.description = body['description']
    if 'image_url' in body:
        instrument.image_url = body['image_url']
    if 'stock' in body:
        instrument.stock = body['stock']
    
    # Handle type-specific attributes
    if isinstance(instrument, Guitar):
        if 'num_strings' in body:
            instrument.num_strings = body['num_strings']
        if 'body_type' in body:
            instrument.body_type = body['body_type']
    elif isinstance(instrument, Piano):
        if 'num_keys' in body:
            instrument.num_keys = body['num_keys']
        if 'is_weighted' in body:
            instrument.is_weighted = body['is_weighted']
    elif isinstance(instrument, Drum):
        if 'num_pads' in body:
            instrument.num_pads = body['num_pads']
        if 'num_cymbals' in body:
            instrument.num_cymbals = body['num_cymbals']
        if 'has_kick' in body:
            instrument.has_kick = body['has_kick']
    elif isinstance(instrument, Violin):
        if 'size' in body:
            instrument.size = body['size']
        if 'bow_included' in body:
            instrument.bow_included = body['bow_included']
    
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
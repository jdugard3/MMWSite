"""
Instrument models for the music store
"""
from . import db
import enum

class InstrumentType(enum.Enum):
    GUITAR = "guitar"
    PIANO = "piano"
    DRUM = "drum"
    VIOLIN = "violin"

class InstrumentCategory(enum.Enum):
    ELECTRIC = "electric"
    ACOUSTIC = "acoustic"
    CLASSICAL = "classical"
    DIGITAL = "digital"
    KEYBOARD = "keyboard"

class Instrument(db.Model):
    """Base model for all instruments"""
    __tablename__ = 'instrument'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    brand = db.Column(db.String(120), nullable=False)
    model = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    stock = db.Column(db.Integer, nullable=False, default=0)
    type = db.Column(db.Enum(InstrumentType), nullable=False)
    category = db.Column(db.Enum(InstrumentCategory), nullable=False)
    
    # Discriminator column for SQLAlchemy inheritance
    instrument_type = db.Column(db.String(50))
    
    __mapper_args__ = {
        'polymorphic_on': instrument_type,
        'polymorphic_identity': 'instrument'
    }
    
    def __repr__(self):
        return f'<Instrument {self.name} ({self.type}/{self.category})>'
    
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "name": self.name,
            "brand": self.brand,
            "model": self.model,
            "price": self.price,
            "description": self.description,
            "image_url": self.image_url,
            "stock": self.stock,
            "type": self.type.value,
            "category": self.category.value,
        }

class Guitar(Instrument):
    """Guitar specific attributes"""
    __tablename__ = 'guitar'
    
    id = db.Column(db.Integer, db.ForeignKey('instrument.id'), primary_key=True)
    num_strings = db.Column(db.Integer, nullable=False, default=6)
    body_type = db.Column(db.String(50), nullable=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'guitar',
    }
    
    def serialize(self):
        data = super().serialize()
        data.update({
            "num_strings": self.num_strings,
            "body_type": self.body_type
        })
        return data

class Piano(Instrument):
    """Piano specific attributes"""
    __tablename__ = 'piano'
    
    id = db.Column(db.Integer, db.ForeignKey('instrument.id'), primary_key=True)
    num_keys = db.Column(db.Integer, nullable=False, default=88)
    is_weighted = db.Column(db.Boolean, nullable=False, default=False)
    
    __mapper_args__ = {
        'polymorphic_identity': 'piano',
    }
    
    def serialize(self):
        data = super().serialize()
        data.update({
            "num_keys": self.num_keys,
            "is_weighted": self.is_weighted
        })
        return data

class ElectricDrum(Instrument):
    """Electric Drum specific attributes"""
    __tablename__ = 'electric_drum'
    
    id = db.Column(db.Integer, db.ForeignKey('instrument.id'), primary_key=True)
    num_pads = db.Column(db.Integer, nullable=False)
    num_cymbals = db.Column(db.Integer, nullable=False)
    has_kick = db.Column(db.Boolean, nullable=False, default=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'drum',
    }
    
    def serialize(self):
        data = super().serialize()
        data.update({
            "num_pads": self.num_pads,
            "num_cymbals": self.num_cymbals,
            "has_kick": self.has_kick
        })
        return data

class Violin(Instrument):
    """Violin specific attributes"""
    __tablename__ = 'violin'
    
    id = db.Column(db.Integer, db.ForeignKey('instrument.id'), primary_key=True)
    size = db.Column(db.String(20), nullable=False)  # 4/4, 3/4, 1/2, etc.
    bow_included = db.Column(db.Boolean, nullable=False, default=True)
    
    __mapper_args__ = {
        'polymorphic_identity': 'violin',
    }
    
    def serialize(self):
        data = super().serialize()
        data.update({
            "size": self.size,
            "bow_included": self.bow_included
        })
        return data 
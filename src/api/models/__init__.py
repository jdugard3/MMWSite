from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Circular imports are handled by importing models after db is defined
# Import all models here to make them available when importing from this package
from .user import User
from .instrument import Instrument, Guitar, Piano, Drum, Violin, InstrumentType, InstrumentCategory 
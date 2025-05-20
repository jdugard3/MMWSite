import os
from flask_admin import Admin
from .models import db, User
from .models.instrument import Instrument, Guitar, Piano, Drum, Violin, InstrumentType, InstrumentCategory
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import DataRequired
from wtforms import SelectField

# Base configuration for all instrument views
INSTRUMENT_BASE_COLUMNS = ['id', 'name', 'brand', 'model', 'price', 'type', 'category', 'stock']
INSTRUMENT_BASE_SORTABLE = ['id', 'name', 'brand', 'model', 'price', 'stock']
INSTRUMENT_BASE_SEARCHABLE = ['name', 'brand', 'model']
INSTRUMENT_BASE_FILTERS = ['type', 'category', 'brand', 'price']

# Enum field configuration
ENUM_FORM_CONFIG = {
    'type': {
        'choices': [(t.name, t.value) for t in InstrumentType],
        'validators': [DataRequired()]
    },
    'category': {
        'choices': [(c.name, c.value) for c in InstrumentCategory],
        'validators': [DataRequired()]
    }
}

# Custom ModelView for instruments
class InstrumentModelView(ModelView):
    """Base view for all instrument models with common configuration"""
    
    # Form configuration
    form_overrides = {
        'type': SelectField,
        'category': SelectField
    }
    form_args = ENUM_FORM_CONFIG
    
    # Column configuration
    column_list = INSTRUMENT_BASE_COLUMNS
    column_sortable_list = INSTRUMENT_BASE_SORTABLE
    column_searchable_list = INSTRUMENT_BASE_SEARCHABLE
    column_filters = INSTRUMENT_BASE_FILTERS
    
    # Format enum values for display
    column_formatters = {
        'type': lambda v, c, m, p: m.type.value if m.type else '',
        'category': lambda v, c, m, p: m.category.value if m.category else ''
    }
    
    # Common settings
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    page_size = 20

# Specific instrument type views
class GuitarModelView(InstrumentModelView):
    """View for Guitar model with specific configuration"""
    column_list = INSTRUMENT_BASE_COLUMNS + ['num_strings', 'body_type']
    column_sortable_list = INSTRUMENT_BASE_SORTABLE + ['num_strings']
    column_searchable_list = INSTRUMENT_BASE_SEARCHABLE + ['body_type']
    column_filters = INSTRUMENT_BASE_FILTERS + ['num_strings']

class PianoModelView(InstrumentModelView):
    """View for Piano model with specific configuration"""
    column_list = INSTRUMENT_BASE_COLUMNS + ['num_keys', 'is_weighted']
    column_sortable_list = INSTRUMENT_BASE_SORTABLE + ['num_keys']
    column_filters = INSTRUMENT_BASE_FILTERS + ['num_keys', 'is_weighted']

class DrumModelView(InstrumentModelView):
    """View for Drum model with specific configuration"""
    column_list = INSTRUMENT_BASE_COLUMNS + ['num_pads', 'num_cymbals', 'has_kick']
    column_sortable_list = INSTRUMENT_BASE_SORTABLE + ['num_pads', 'num_cymbals']
    column_filters = INSTRUMENT_BASE_FILTERS + ['num_pads', 'num_cymbals', 'has_kick']

class ViolinModelView(InstrumentModelView):
    """View for Violin model with specific configuration"""
    column_list = INSTRUMENT_BASE_COLUMNS + ['size', 'bow_included']
    column_searchable_list = INSTRUMENT_BASE_SEARCHABLE + ['size']
    column_filters = INSTRUMENT_BASE_FILTERS + ['size', 'bow_included']

def setup_admin(app):
    """Configure and initialize the admin interface"""
    # Basic admin configuration
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    
    # Initialize admin
    admin = Admin(
        app, 
        name='MMW Music Store Admin', 
        template_mode='bootstrap3',
        base_template='admin/base.html'
    )
    
    # Register views
    views = [
        (User, ModelView),
        (Instrument, InstrumentModelView),
        (Guitar, GuitarModelView),
        (Piano, PianoModelView),
        (Drum, DrumModelView),
        (Violin, ViolinModelView)
    ]
    
    # Add all views
    for model, view_class in views:
        admin.add_view(view_class(model, db.session))
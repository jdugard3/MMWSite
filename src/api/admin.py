import os
from flask_admin import Admin
from .models import db, User
from .models.instrument import Instrument, Guitar, Piano, Drum, Violin
from flask_admin.contrib.sqla import ModelView
from wtforms.validators import DataRequired

# Use standard ModelView without any patches
def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='MMW Music Store Admin', template_mode='bootstrap3')

    # Add your models here, for example this is how we add the User model to the admin
    admin.add_view(ModelView(User, db.session))
    
    # Add instrument models
    admin.add_view(ModelView(Instrument, db.session))
    admin.add_view(ModelView(Guitar, db.session))
    admin.add_view(ModelView(Piano, db.session))
    admin.add_view(ModelView(Drum, db.session))
    admin.add_view(ModelView(Violin, db.session))

    # You can duplicate that line to add mew models
    # admin.add_view(ModelView(YourModelName, db.session))
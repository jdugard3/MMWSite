import click
from api.models import db, User, Instrument
from flask_migrate import migrate, upgrade, init, downgrade, stamp

"""
In this file, you can add as many commands as you want using the @app.cli.command decorator
Flask commands are useful to run cronjobs or tasks outside of the API but sill in integration 
with your database, for example: Import the price of bitcoin every night as 12am
"""
def setup_commands(app):
    
    """ 
    This is an example command "insert-test-users" that you can run from the command line
    by typing: $ flask insert-test-users 5
    Note: 5 is the number of users to add
    """
    @app.cli.command("insert-test-users") # name of our command
    @click.argument("count") # argument of out command
    def insert_test_users(count):
        print("Creating test users")
        for x in range(1, int(count) + 1):
            user = User()
            user.email = "test_user" + str(x) + "@test.com"
            user.password = "123456"
            user.is_active = True
            db.session.add(user)
            db.session.commit()
            print("User: ", user.email, " created.")

        print("All test users created")

    @app.cli.command("insert-test-data")
    def insert_test_data():
        pass
        
    @app.cli.command("fix-instrument-types")
    def fix_instrument_types():
        """Fix instruments with invalid instrument_type values"""
        print("Fixing invalid instrument types...")
        try:
            # Find all instruments with the invalid type
            invalid_instruments = Instrument.query.filter_by(
                instrument_type='Not sure why this instrument type is here'
            ).all()
            
            if not invalid_instruments:
                print("No invalid instruments found.")
                return
                
            print(f"Found {len(invalid_instruments)} invalid instruments.")
            
            # Update each invalid instrument to a valid type ('instrument')
            for inst in invalid_instruments:
                print(f"Fixing instrument {inst.id}: {inst.name}")
                inst.instrument_type = 'instrument'
                db.session.add(inst)
                
            db.session.commit()
            print("Fixed all invalid instrument types.")
            
        except Exception as e:
            db.session.rollback()
            print(f"Error fixing instrument types: {str(e)}")
            
    @app.cli.command("reset-db")
    def reset_db():
        """Reset the database by dropping all tables and recreating them"""
        print("Resetting database...")
        try:
            # Drop all tables
            print("Dropping all tables...")
            db.drop_all()
            db.session.commit()
            print("All tables dropped.")
            
            # Create all tables again
            print("Creating tables...")
            db.create_all()
            db.session.commit()
            print("Tables created.")
            
            print("Database reset successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"Error resetting database: {str(e)}")
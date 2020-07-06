import os

SERVICES = ['zentopia_product_api']

# APPLICATION_SETTINGS = os.environ.get('APPLICATION_SETTINGS', 'com_limes.settings')

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///{}/db.sqlite3'.format(os.path.dirname(__file__)))
SQLALCHEMY_TRACK_MODIFICATIONS = False

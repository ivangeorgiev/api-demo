import os

SERVICES = ['api_demo.product']

# APPLICATION_SETTINGS = os.environ.get('APPLICATION_SETTINGS', 'com_limes.settings')

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///:memory:')
SQLALCHEMY_TRACK_MODIFICATIONS = False

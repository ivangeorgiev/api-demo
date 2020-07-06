from zentopia import db
import datetime

class Product(db.Model):
    __tablename__ = 'products'
    __table_args__ = {'extend_existing': True} 

    id = db.Column('product_id', db.Integer, primary_key=True)
    name = db.Column('product_name', db.String(255), unique=True, nullable=False, )
    slug = db.Column('product_slug', db.String(255), unique=True, nullable=False)
    price = db.Column('product_price', db.Integer, nullable=False)
    image = db.Column('product_image', db.String(255), unique=False, nullable=True)
    added_at = db.Column('product_added_at', db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column('product_updated_at', db.DateTime, onupdate=datetime.datetime.utcnow)
    
    def asDict(self):
        col_names = [col for col in sorted(vars(self).keys()) if not col.startswith('_')]
        return {name:getattr(self,name) for name in col_names}

    def __repr__(self):
        col_names = [col for col in sorted(vars(self).keys()) if not col.startswith('_')]
        db.Columns_repr = ["{}={}".format(name,repr(getattr(self, name))) for name in col_names]
        return "{}({})".format(self.__class__.__name__, ", ".join(db.Columns_repr))

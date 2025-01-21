from .extensions import db

class Product(db.Model):
    __tablename__ = 'Products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    userId = db.Column(db.String(255))
    image_data = db.Column(db.LargeBinary)  # Aquí guardamos la imagen en formato binario
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    category_id = db.Column(db.Integer, db.ForeignKey('Categories.id'), nullable=True)  # Relación con la tabla Category

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "userId": self.userId,
            "image_data": self.image_data.decode('latin1') if self.image_data else None,  # Decodificamos si es necesario
            "created_at": self.created_at,
            "category_id": self.category_id
        }

class Category(db.Model):
    __tablename__ = 'Categories'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    products = db.relationship('Product', backref='category', lazy=True)  # Relación con la tabla Product

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

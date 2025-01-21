import base64
from flask import Blueprint, jsonify, request
from app.models import Product, Category
from app import db

read_bp = Blueprint('read', __name__)

@read_bp.route('/items', methods=['GET'])
def get_all_products():
    products = Product.query.all()
    if not products:
        return jsonify({"message": "No products found"}), 404

    products_list = [product.to_dict() for product in products]
    return jsonify({"message": "Products fetched successfully", "products": products_list}), 200

@read_bp.route('/items/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    
    if not product:
        return jsonify({"message": "Product not found"}), 404

    return jsonify({"message": "Product fetched successfully", "product": product.to_dict()}), 200

@read_bp.route('/categories', methods=['GET'])
def get_all_categories():
    categories = Category.query.all()
    if not categories:
        return jsonify({"message": "No categories found"}), 404

    categories_list = [category.to_dict() for category in categories]
    return jsonify({"message": "Categories fetched successfully", "categories": categories_list}), 200

@read_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category_by_id(category_id):
    category = Category.query.get(category_id)
    
    if not category:
        return jsonify({"message": "Category not found"}), 404

    return jsonify({"message": "Category fetched successfully", "category": category.to_dict()}), 200

# Ruta para manejar datos recibidos por webhook
@read_bp.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({"message": "No data received"}), 400

    # Validar si los datos corresponden a un producto o una categoría
    if 'price' in data:  # Es un producto
        product_id = data.get('id')
        name = data.get('name')
        description = data.get('description')
        price = data.get('price')
        userId = data.get('userId')
        image_data = data.get('image_data')
        created_at = data.get('created_at')
        category_id = data.get('category_id')  # Nuevo campo para categoría

        if not product_id or not name or not description or not price:
            return jsonify({"message": "Invalid product data"}), 400

        # Convertir imagen de Base64 a binario si existe
        image_data_binary = base64.b64decode(image_data) if image_data else None

        # Manejo de categoría
        if category_id:
            category = Category.query.filter_by(id=category_id).first()
            if not category:
                return jsonify({"message": "Category not found"}), 404

        # Buscar si el producto ya existe
        product = Product.query.filter_by(id=product_id).first()
        if not product:
            product = Product(
                id=product_id,
                name=name,
                description=description,
                price=price,
                userId=userId,
                image_data=image_data_binary,
                created_at=created_at,
                category_id=category_id  # Asigna la categoría al producto
            )
            db.session.add(product)
        else:
            # Actualizar producto existente
            product.name = name
            product.description = description
            product.price = price
            product.userId = userId
            product.image_data = image_data_binary
            product.created_at = created_at
            product.category_id = category_id

        db.session.commit()
        return jsonify({"message": "Product synchronized successfully"}), 200

    elif 'description' in data and 'name' in data:  # Es una categoría
        category_id = data.get('id')
        name = data.get('name')
        description = data.get('description')

        if not category_id or not name:
            return jsonify({"message": "Invalid category data"}), 400

        # Buscar si la categoría ya existe
        category = Category.query.filter_by(id=category_id).first()
        if not category:
            category = Category(
                id=category_id,
                name=name,
                description=description
            )
            db.session.add(category)
        else:
            # Actualizar categoría existente
            category.name = name
            category.description = description

        db.session.commit()
        return jsonify({"message": "Category synchronized successfully"}), 200

    return jsonify({"message": "Invalid data"}), 400
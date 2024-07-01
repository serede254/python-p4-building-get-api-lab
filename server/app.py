#!/usr/bin/env python3

from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    all_bakeries = Bakery.query.all()
    bakeries_list = []
    
    for bakery in all_bakeries:
        baked_goods = []
        for good in bakery.baked_goods:
            baked_goods.append({
                'id': good.id,
                'name': good.name,
                'price': good.price,
                'created_at': str(good.created_at),
                'updated_at': str(good.updated_at) if good.updated_at else None,
                'bakery_id': good.bakery_id
            })
        
        bakery_data = {
            'id': bakery.id,
            'name': bakery.name,
            'created_at': str(bakery.created_at),
            'updated_at': str(bakery.updated_at) if bakery.updated_at else None,
            'baked_goods': baked_goods
        }
        bakeries_list.append(bakery_data)
    
    return jsonify(bakeries_list)


@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.get_or_404(id)
    baked_goods = [{
        'id': good.id,
        'name': good.name,
        'price': good.price,
        'bakery_id': good.bakery_id,
        'created_at': str(good.created_at),
        'updated_at': str(good.updated_at) if good.updated_at else None
    } for good in bakery.baked_goods]
    
    response_data = {
        'id': bakery.id,
        'name': bakery.name,
        'created_at': str(bakery.created_at),
        'updated_at': str(bakery.updated_at) if bakery.updated_at else None,
        'baked_goods': baked_goods
    }
    
    response = make_response(jsonify(response_data))
    response.headers['Content-Type'] = 'application/json'
    
    return response


@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    sorted_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    
    baked_goods_list = []
    for good in sorted_goods:
        bakery_data = None
        if good.bakery:
            bakery_data = {
                'id': good.bakery.id,
                'name': good.bakery.name,
                'created_at': str(good.bakery.created_at),
                'updated_at': str(good.bakery.updated_at) if good.bakery.updated_at else None
            }
        
        baked_good_data = {
            'id': good.id,
            'name': good.name,
            'price': good.price,
            'created_at': str(good.created_at),
            'updated_at': str(good.updated_at) if good.updated_at else None,
            'bakery_id': good.bakery_id,
            'bakery': bakery_data
        }
        
        baked_goods_list.append(baked_good_data)
    
    return jsonify(baked_goods_list)



@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive_good = BakedGood.query.order_by(BakedGood.price.desc()).first_or_404()
    
    bakery_data = None
    if most_expensive_good.bakery:
        bakery_data = {
            'id': most_expensive_good.bakery.id,
            'name': most_expensive_good.bakery.name,
            'created_at': str(most_expensive_good.bakery.created_at),
            'updated_at': str(most_expensive_good.bakery.updated_at) if most_expensive_good.bakery.updated_at else None
        }
    
    response_data = {
        'id': most_expensive_good.id,
        'name': most_expensive_good.name,
        'price': most_expensive_good.price,
        'created_at': str(most_expensive_good.created_at),
        'updated_at': str(most_expensive_good.updated_at) if most_expensive_good.updated_at else None,
        'bakery_id': most_expensive_good.bakery_id,
        'bakery': bakery_data
    }
    
    return jsonify(response_data)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
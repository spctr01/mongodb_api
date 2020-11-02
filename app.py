from flask import Flask
import pymongo
import json
import requests
from flask import jsonify
from flask import request

app = Flask(__name__)
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["greendeck"]
collection = mydb["gd"]



# returns all the data in database collection
@app.route('/read', methods=['GET'])
def get():
    documents = collection.find()
    response = []
    for document in documents:
        document['_id'] = str(document['_id'])
        response.append(document)
    return jsonify({'result':response})



#insert new record to database collection
@app.route('/create', methods=['POST'])
def add_star():
    '''
    gets all new entries from the json and create a new record
    record = insert new record in collection
    new_id = id of the new created record
    output = all the data with new id
    '''

    name = request.json['name']
    brand_name = request.json['brand_name']
    regular_price_value = request.json['regular_price_value']
    offer_price_value = request.json['offer_price_value']
    currency = request.json['currency']
    classification_l1= request.json['classification_l1']
    classification_l2= request.json['classification_l2']
    classification_l3 = request.json['classification_l3']
    classification_l4= request.json['classification_l4']
    image_url= request.json['image_url']


    record = collection.insert_one({'name': name, 'brand_name': brand_name, 
                            'regular_price_value':regular_price_value, 'offer_price_value':offer_price_value,
                            'currency':currency, 'classification_l1':classification_l1,
                            'classification_l2':classification_l2, 'classification_l3':classification_l3,
                           'classification_l4':classification_l4, 'image_url':image_url })

    new_id = collection.find_one({'_id': record.inserted_id })
    output = {'name' : new_id['name'], 'brand_name': new_id['brand_name'], 
                            'regular_price_value':new_id['regular_price_value'], 'offer_price_value':new_id['offer_price_value'],
                            'currency':new_id['currency'], 'classification_l1':new_id['classification_l1'],
                            'classification_l2':new_id['classification_l2'], 'classification_l3':new_id['classification_l3'],
                           'classification_l4':new_id['classification_l4'], 'image_url':new_id['image_url'] }
    return jsonify({'result' : output})



#update the existing record
#take input as json  first old record & 2nd new record
@app.route('/update', methods=['PATCH'])
def update():
    old_data = request.json['old']
    new_data = {"$set":request.json['new']}
   
    update = collection.update_one(old_data,new_data)
    if update:
        return jsonify({'status' : 'updated successfully'})
    else:
        return jsonify({'status' : 'updated unsuccessfull'})


# delete one record only
@app.route('/delete_one',methods=['POST'])
def delete():
    name = request.json['name']
    collection.delete_one({'name':name})

    return jsonify({'status':'Record {} deleted successfully'.format(name)})


#delete multiple records
@app.route('/delete_many',methods=['POST'])
def deletel_many():
    name = request.json['name']
    collection.delete_many({'name':name})

    return jsonify({'status':'Records {} deleted successfully'.format(name)})


if __name__ == '__main__':
    app.run(debug=True)

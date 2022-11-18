from flask import Flask, request, json, Response
from model.mongodb_api import MongoAPI
import logging

app = Flask(__name__)
logging.basicConfig(filename='log.txt', level=logging.DEBUG,
        format='[%(asctime)s %(levelname)-8s] %(message)s',
        datefmt='%Y%m%d %H:%M:%S')

@app.route('/')
def index():
    return Response(response=json.dumps({'Status': 'Up'}),
                    status=200, 
                    mimetype='application/json')

# search houses by filter
@app.route('/mongodb', methods=['GET'])
def mongo_read():
    try:
        data = request.get_json()
        if data is None or data == {}:
            return Response(response=json.dumps({"error": "Please provide correct information"}),
                        status=400, 
                        mimetype='application/json')

        mongo_api = MongoAPI()
        documents = mongo_api.read(data)
        return Response(response=json.dumps(documents),
                    status=200, 
                    mimetype='application/json')
    
    except Exception as e:
            return Response(response=json.dumps({'error': f'cannot read houses, {e}'}),
                status=500, 
                mimetype='application/json')

# create one document
@app.route('/mongodb', methods=['POST'])
def mongo_create():
    try:
        data = request.get_json()
        if data is None or data == {}:
            return Response(response=json.dumps({"error": "Please provide correct information"}),
                        status=400, 
                        mimetype='application/json')

        mongo_api = MongoAPI()
        output = mongo_api.create(data)
        return Response(response=json.dumps(output),
                    status=200, 
                    mimetype='application/json')

    except Exception as e:
            return Response(response=json.dumps({'error': f'cannot create a house, {e}'}),
                status=500, 
                mimetype='application/json')

# update the first occurrence from query
@app.route('/mongodb', methods=['PUT'])
def mongo_update():
    try:
        data = request.get_json()
        if data is None or data == {}:
            return Response(response=json.dumps({"error": "Please provide correct information"}),
                        status=400, 
                        mimetype='application/json')

        mongo_api = MongoAPI()
        output = mongo_api.update(data)
        return Response(response=json.dumps(output),
                    status=200, 
                    mimetype='application/json')

    except Exception as e:
            return Response(response=json.dumps({'error': f'cannot update a house, {e}'}),
                status=500, 
                mimetype='application/json')

# delete the first occurrence from query
@app.route('/mongodb', methods=['DELETE'])
def mongo_delete():
    try:
        data = request.get_json()
        if data is None or data == {}:
            return Response(response=json.dumps({"error": "Please provide correct information"}),
                        status=400, 
                        mimetype='application/json')

        mongo_api = MongoAPI()
        output = mongo_api.delete(data)
        return Response(response=json.dumps(output),
                    status=200, 
                    mimetype='application/json')

    except Exception as e:
            return Response(response=json.dumps({'error': f'cannot delete a house, {e}'}),
                status=500, 
                mimetype='application/json')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
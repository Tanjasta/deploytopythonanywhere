from flask import Flask, jsonify, request, abort, send_from_directory
from carDAO import carDAO

app = Flask(__name__, static_url_path='', static_folder='.')


# Route to serve the main page of the web app. 
# Serve a static HTML file, 'carviewer.html'.
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'carviewer.html')


# Route to get all cars.
@app.route('/cars')
def getAll():
    # Retrieve all cars from the database using the carDAO.
    results = carDAO.getAll()
    return jsonify(results)

# Route to find a car by its ID.
@app.route('/cars/<int:id>')
def findById(id):
    foundCar = carDAO.findByID(id)

    return jsonify(foundCar)

# Route to create a new car entry.
@app.route('/cars', methods=['POST'])
def create():
    
    if not request.json:
        abort(400)
    # other checking 
    car = {
        "name": request.json['name'],
        "model": request.json['model'],
        "price": request.json['price'],
    }
    values =(car['name'],car['model'],car['price'])
    newId = carDAO.create(values)
    car['id'] = newId
    return jsonify(car)

# Route to update car's details.
@app.route('/cars/<int:id>', methods=['PUT'])
def update(id):
    foundCar = carDAO.findByID(id)
    if not foundCar:
        abort(404)
    
    if not request.json:
        abort(400)
    reqJson = request.json
    if 'price' in reqJson and type(reqJson['price']) is not int:
        abort(400)

    if 'name' in reqJson:
        foundCar['name'] = reqJson['name']
    if 'model' in reqJson:
        foundCar['model'] = reqJson['model']
    if 'price' in reqJson:
        foundCar['price'] = reqJson['price']
    values = (foundCar['name'],foundCar['model'],foundCar['price'],foundCar['id'])
    carDAO.update(values)
    return jsonify(foundCar)
        

    
# Route to delete a car by its ID.
@app.route('/cars/<int:id>' , methods=['DELETE'])
def delete(id):
    carDAO.delete(id)
    return jsonify({"done":True})

if __name__ == '__main__' :
    app.run(debug= True)
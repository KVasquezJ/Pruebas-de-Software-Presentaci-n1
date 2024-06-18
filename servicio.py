from flask import Flask, request, jsonify
app = Flask(__name__)

# Simulación de base de datos en memoria
users = {}
nextID = 1

@app.route('/CreateUsers', methods=['POST'])
def createUser():
    global nextID
    if request.method == 'POST':
        data = request.get_json()
    userId = nextID
    nextID += 1
    users[ userId ] = data
    with open('storedData.txt', 'r') as fr:
        lines = fr.readlines()
        with open('storedDataAux.txt', 'w') as fw:
            for line in lines:
                if line.split(":")[0] != userId:
                    fw.write(line)
    with open('storedDataAux.txt', 'r') as fr:
        lines = fr.readlines()
        with open('storedData.txt', 'w') as fw:
            for line in lines:
                fw.write(line)
    f = open("storedData.txt", "a")
    f.write('\n' + userId + ': ' + data)
    f.close()
    return jsonify({'id':  userId , 'user': data}), 201
@app.route('/GetAllUsers', methods=['GET'])
def getAllUsers():
    return jsonify(users), 200

@app.route('/GetUser/<int:userId>', methods=['GET'])
def get_user( userId ):
    user = users.get( userId )
    if user:
        return jsonify(user), 200
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/DeleteUser/<int:userId>', methods=['DELETE'])
def delete_user(userId):
    with open('storedData.txt', 'r') as fr:
        lines = fr.readlines()
        with open('storedDataAux.txt', 'w') as fw:
            for line in lines:
                if line.split(":")[0] != userId:
                    fw.write(line)
    with open('storedDataAux.txt', 'r') as fr:
        lines = fr.readlines()
        with open('storedData.txt', 'w') as fw:
            for line in lines:
                fw.write(line)
    if  userId  in users:
        del users[ userId ]
        return jsonify({'message': 'User deleted'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
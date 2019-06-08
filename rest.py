from flask import Flask, jsonify, request
import json 

app = Flask(__name__)

counter = 0

DATABASE = {
}

class Entry(object):
	def __init__(self, entry_id, title, content):
		self.entry_id = entry_id 
		self.title = title
		self.content = content

	def json(self):
		return jsonify(vars(self))

@app.route('/entry/<int:entry_id>')
def get_entry(entry_id):


	if entry_id in DATABASE:
		return DATABASE[entry_id].json(),200
	else:
		return jsonify({ 'error': 'Not in DATABASE'}), 404

@app.route('/entry', methods=["POST"])
def post_entry():
	request_body = request.get_json()
	global counter
	new_entry = Entry(counter, request_body['title'], request_body['content'])
	counter += 1
	DATABASE[new_entry.entry_id] = new_entry

	return jsonify({ 'entry_id': new_entry.entry_id })

@app.route('/entry/<int:entry_id>', methods=["DELETE"])
#dont forget id is int
def delete_entry(entry_id):

	if entry_id in DATABASE:
		del DATABASE[entry_id]
		return jsonify({}), 200
	else:
		return jsonify({ 'error': 'Not in DATABASE'}), 404

@app.route('/entry/<int:entry_id>', methods=["PATCH"])
def update_entry(entry_id):

	if entry_id not in DATABASE:
		return jsonify({}), 404

	entry = DATABASE[entry_id]

	request_body = request.get_json()
	
	if 'title' in request_body:
		entry.title = request_body['title']

	if 'content' in request_body:
		entry.content = request_body['content']

	DATABASE[entry_id] = entry

	return jsonify({}),200


@app.route('/entries')
def get_all_entries():

	entries = list(DATABASE.keys())
	entries.sort()


	return jsonify({ 'entries': entries })


if __name__ == '__main__':
	app.run(debug=True)
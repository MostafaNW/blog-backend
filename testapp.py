from flask import Flask, jsonify, request
from model.requesthandler import RequestHandler
from model.validator import Validator
import os
request_handler = RequestHandler(os.path.abspath('config.ini'))
validator = Validator()
app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route("/api/ping")
def ping():
    return jsonify({"success": True}), 200

@app.route("/api/posts")
def posts():
    tags = request.args.get('tags')
    if tags == None or tags.strip(' ') == '':
        return jsonify({"error": 'Tag parameter is required'}),  400
    sortBy = request.args.get('sortBy')
    direction = request.args.get('direction')
    if sortBy:
        if not (validator.v_sortBy(sortBy)):
            return jsonify({"error": "sortBy parameter is invalid"}), 400
    if direction:
        if not (validator.v_direction(direction)):
            return jsonify({"error": 'direction parameter is invalid'}), 400
    posts = request_handler.get_posts(tags.split(','))
    sorted_posts = list(map(lambda post: post.data, request_handler.sort_posts(posts, sortBy, direction)))
    return jsonify({"posts" : sorted_posts}), 200

@app.route("/api/authors")
def authors():
    return jsonify({"authors": request_handler.get_author_data()}), 200

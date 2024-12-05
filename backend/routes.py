from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return jsonify(data)

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture:
        return jsonify(picture)
    else:
        return jsonify({"error": "Picture not found"}), 404
 


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    pic_data = request.get_json()

    for pic in data:
        if int(pic["id"]) == int(pic_data["id"]):
            return {"Message": f"picture with id {pic_data.get('id')} already present"}, 302

    data.append(pic_data)
    return jsonify(pic_data), 201

######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pic_data = request.get_json()

    for pic in data:
        if int(pic["id"]) == int(pic_data["id"]):
            pic.update(pic_data)
            return jsonify(pic), 200

    return {"message": "picture not found"}, 404


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    picture = next((pic for pic in data if pic["id"] == id), None)
    if picture:
        data.remove(picture)
        return {}, 204

    # for pic in data:
    #     if int(pic[id]) == int(pic_data["id"]):
    #         data.remove(pic)
    #         return {}, 204

    return {"message": "picture not found"}, 404

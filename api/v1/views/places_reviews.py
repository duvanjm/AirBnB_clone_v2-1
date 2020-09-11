#!/usr/bin/python3
""" Places """

from flask import jsonify, request, abort
from flask import make_response
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews_from_place(place_id):
    """Retrieves the list of all Places objects"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == "GET":
        review = storage.all(Review).values()
        all_review = []
        for key in review.values():
            if key.place_id == place_id:
                all_review.append(key.to_dict())
        return jsonify(all_review)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review_id(review_id):
    """Gets a review object"""
    for key, val in storage.all('Review').items():
        if val.id == review_id:
            return jsonify((val.to_dict()))
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review based on id"""
    review_object = storage.get(Review, review_id)
    if review_object is None:
        abort(404)
    else:
        storage.delete(review_object)
        storage.save()
        return (jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a new review object"""
    if storage.get(Place, place_id) is None:
        abort(404)
    if not request.get_json():
        return (jsonify({"error": "Not a JSON"}), 400)
    responce = request.get_json()
    if "user_id" not in responce:
        return (jsonify({"error": "Missing user_id"}), 400)
    if storage.get(User, responce["user_id"]) is None:
        abort(404)
    if "text" not in responce:
        return (jsonify({"error": "Missing text"}), 400)
    responce["place_id"] = place_id
    new_review_obj = Review(**responce)
    new_review_obj.save()
    return jsonify(new_review_obj.to_dict(), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a review object"""
    ignore_ = ["id", "user_id", "city_id", "created_at", "updated_at"]
    responce = request.get_json()
    all_the_reviews = storage.get(Review, review_id)
    if all_the_reviews is None:
        abort(404)
    if not responce:
        return (jsonify({"error": "Not a JSON"}), 400)
    for key, value in responce.items():
        if key not in ignore_:
            setattr(all_the_reviews, key, value)
    storage.save()
    return jsonify(all_the_reviews.to_dict(), 200)

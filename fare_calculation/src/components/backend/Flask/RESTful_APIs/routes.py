from db_scripts import database
from flask import Blueprint, request, jsonify

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/fares?from=<id>&to=<id>', methods=['GET'])
def get_fare():
    from_station = request.args.get('from')
    to_station = request.args.get('to')
    query = """
        SELECT fare
        from fares
        WHERE origin_station = ? AND destination_station = ?
    """

    fare = database.fetch_one(query, (from_station, to_station))
    if fare:
        return jsonify({"fare": fare[0]}), 200
    else:
        return jsonify({"error": "Fare not found"}), 404
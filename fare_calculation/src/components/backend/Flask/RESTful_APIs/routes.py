from flask import Blueprint, request, jsonify
from db_scripts.database import fetch_one, fetch_all   # ✅ make sure this exists

routes_bp = Blueprint("routes", __name__)

@routes_bp.route('/stations', methods=["GET"])
def get_stations():
    
    query = "SELECT * FROM stations"
    
    stations = fetch_all(query)
    
    if stations:
        return jsonify({"station": stations}), 200
    else:
        return jsonify({"error": "Station not found"}), 404

@routes_bp.route("/fares", methods=["GET"])
def get_fare():
    from_station = request.args.get("from")
    to_station = request.args.get("to")

    query = """
        SELECT fare
        FROM fares
        WHERE origin_id = ? AND destination_id = ?
    """

    fare = fetch_one(query, (from_station, to_station))

    if fare:
        return jsonify({"fare": fare[0]}), 200
    else:
        return jsonify({"error": "Fare not found"}), 404
@routes_bp.route("/route", methods=["GET"])
def get_route():
    from_station = request.args.get("from")
    to_station = request.args.get("to")

    # Get station info
    station_query = "SELECT * FROM stations WHERE id = ?"
    origin = fetch_one(station_query, (from_station,))
    destination = fetch_one(station_query, (to_station,))

    if not origin or not destination:
        return jsonify({"error": "Invalid station(s)"}), 404

    # Get fare (direct only)
    fare_query = """
        SELECT fare FROM fares
        WHERE origin_id = ? AND destination_id = ?
    """
    fare = fetch_one(fare_query, (from_station, to_station))

    if not fare:
        return jsonify({"error": "No direct route found"}), 404

    return jsonify({
        "origin": {
            "id": origin[0],
            "name": origin[1],
            "lat": origin[2],
            "lon": origin[3]
        },
        "destination": {
            "id": destination[0],
            "name": destination[1],
            "lat": destination[2],
            "lon": destination[3]
        },
        "fare": fare[0],
        "path": [origin[1], destination[1]]  # just names in order
    }), 200

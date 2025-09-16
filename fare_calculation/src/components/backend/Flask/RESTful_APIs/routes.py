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

    # Validate stations
    station_query = "SELECT id, station_name, lat, lon FROM stations WHERE station_name = ?"
    origin = fetch_one(station_query, (from_station,))
    destination = fetch_one(station_query, (to_station,))

    if not origin or not destination:
        return jsonify({"error": "Invalid station(s)"}), 404

    # Get fare
    fare_query = """
        SELECT fare FROM fares
        WHERE origin_station = ? AND destination_station = ?
    """
    fare = fetch_one(fare_query, (from_station, to_station))

    if not fare:
        return jsonify({"error": "No direct fare found"}), 404

    # For now, just return direct route (you can expand to multiple hops later)
    path = [from_station, to_station]

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
        "path": path,
        "total_hops": len(path) - 1,
        "total_fare": float(fare[0])
    }), 200

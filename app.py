from flask import Flask, render_template, request,redirect,url_for, session, jsonify
import requests
import rasterio
from rasterio.features import shapes
from shapely.geometry import shape, mapping
from shapely.ops import transform
from pyproj import Transformer

app = Flask(__name__)
app.secret_key = "test"

CORRECT_USERNAME = "zorphious"
CORRECT_PASSWORD = "1234"

@app.route("/", methods=["GET","POST"])
def home():

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username==CORRECT_USERNAME and password==CORRECT_PASSWORD:

            session["logged in"] = True
            session["username"]= username

            return redirect(url_for("dashboard"))

        return "Invalid username or password"

    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if not session.get("logged in"):
        return redirect(url_for("home"))
    return render_template("dashboard.html")

@app.route("/logout")
def logout():
    session.clear()

    return redirect(url_for("home"))

#geocoding route and boundary marking of the district on map using openstreetmap api and leaflet.js

@app.route("/geocode")
def geocode():

    state = request.args.get("state")
    district = request.args.get("district")

    if not state or not district:
        return jsonify({
            "error": "State and district are required."
        }), 400

    query = f"{district} district, {state}, India"

    url = "https://nominatim.openstreetmap.org/search"

    parameters = {
        "q": query,
        "format": "jsonv2",
        "limit": 1,
        "countrycodes": "in",
        "polygon_geojson" :1 ,
        "addressdetails": 1
    }

    headers = {
        "User-Agent": "SIH26191-Disaster-Risk-Management/1.0"
    }

    response = requests.get(
        url,
        params=parameters,
        headers=headers,
        timeout=10
    )

    if response.status_code != 200:
        return jsonify({
            "error": "Geocoding service unavailable."
        }), 502

    results = response.json()

    if not results:
        return jsonify({
            "error": "Location not found."
        }), 404

    location = None

    for result in results:

        if result.get("type") in ["administrative", "boundary"]:
            location = result
            break


    if location is None:
        location = results[0]

    return jsonify({
        "latitude": float(location["lat"]),
        "longitude": float(location["lon"]),
        "display_name": location["display_name"],
        "geometry": location.get("geojson")
    })

#habitaion marking of district which includes information about the district like population, literacy rate,etc using openstreetmap api and leaflet.js

@app.route("/habitations")
def habitations():

    south = request.args.get("south")
    west = request.args.get("west")
    north = request.args.get("north")
    east = request.args.get("east")

    if not all([south, west, north, east]):
        return jsonify({
            "error": "Bounding box is required."
        }), 400

    query = f"""
    [out:json][timeout:60];

    (node["place"~"city|town|village|hamlet"]({south},{west},{north},{east});
    );

    out;
    """

    url = "https://overpass.kumi.systems/api/interpreter"

    response = requests.get(
        url,
        params={"data": query},
        timeout=70
    )

    if response.status_code != 200:
        return jsonify({
            "error": "Unable to retrieve habitation data."
        }), 502

    data = response.json()

    habitations = []

    for element in data["elements"]:

        tags = element.get("tags", {})

        if "name" not in tags:
            continue

        habitations.append({
            "name": tags["name"],
            "type": tags.get("place", "unknown"),
            "latitude": element["lat"],
            "longitude": element["lon"],
            "population": tags.get("population")
        })

    return jsonify({
        "habitations": habitations
    })

# -------------------------------------------------
# Red-zone layer
# -------------------------------------------------

@app.route("/red-zone")
def red_zone():

    state = request.args.get("state")
    district = request.args.get("district")

    if not state or not district:
        return jsonify({
            "error": "State and district are required."
        }), 400

    # Currently ML red-zone data is available only for Pune
    if state.lower() != "maharashtra" or district.lower() != "pune":

        return jsonify({
            "error": "Red-zone data is currently available only for Pune."
        }), 404

    raster_path = "data/processed/pune_landslide_red_zone.tif"

    try:

        with rasterio.open(raster_path) as src:

            red_zone = src.read(1)

            # Red zone pixels have value 1
            mask = red_zone == 1

            # Raster CRS -> Leaflet CRS
            transformer = Transformer.from_crs(
                src.crs,
                "EPSG:4326",
                always_xy=True
            )

            features = []

            for geometry, value in shapes(
                red_zone,
                mask=mask,
                transform=src.transform
            ):

                if value == 1:

                    polygon = shape(geometry)

                    # Convert UTM coordinates
                    # to longitude/latitude
                    polygon_wgs84 = transform(
                        transformer.transform,
                        polygon
                    )

                    features.append({
                        "type": "Feature",
                        "properties": {
                            "zone": "Landslide Red Zone"
                        },
                        "geometry": mapping(
                            polygon_wgs84
                        )
                    })

            geojson = {
                "type": "FeatureCollection",
                "features": features
            }

            print(
                f"Red-zone polygons created: {len(features)}"
            )

            return jsonify(geojson)

    except Exception as e:

        print("Red-zone error:", e)

        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
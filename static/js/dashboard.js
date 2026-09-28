const districts = {

    maharashtra: [
        "Pune",
        "Mumbai Suburban",
        "Mumbai City",
        "Nashik",
        "Kolhapur"
    ],

    uttarakhand: [
        "Dehradun",
        "Chamoli",
        "Rudraprayag",
        "Uttarkashi"
    ],

    kerala: [
        "Ernakulam",
        "Idukki",
        "Wayanad",
        "Kozhikode"
    ]

};

//state selection and district selection


const stateSelect = document.getElementById("state");

const districtSelect = document.getElementById("district");


stateSelect.addEventListener("change", function () {

    const selectedState = stateSelect.value;

    districtSelect.innerHTML =
        '<option value="">Select District</option>';

    if (!selectedState) {
        return;
    }

    const stateDistricts = districts[selectedState];

    stateDistricts.forEach(function (district) {

        const option = document.createElement("option");

        option.value = district;
        option.textContent = district;

        districtSelect.appendChild(option);

    });

});

//analyse button click event


const analyseButton = document.getElementById("analyse-button");

const selectedArea = document.getElementById("selected-area");

let districtBoundary = null;
let redZoneLayer = null;

analyseButton.addEventListener("click", async function () {

    const selectedState = stateSelect.value;

    const selectedDistrict = districtSelect.value;

    if (!selectedState || !selectedDistrict) {
        alert("Please select a state and district.");
        return;
    }

    const stateName = stateSelect.options[stateSelect.selectedIndex].text;

    selectedArea.textContent =
        "Finding location...";


    try {

        const response = await fetch(
            `/geocode?state=${encodeURIComponent(stateName)}&district=${encodeURIComponent(selectedDistrict)}`
        );


        const data = await response.json();


        if (!response.ok) {

            throw new Error(
                data.error || "Unable to find location."
            );

        }


        selectedArea.textContent =
            "Selected Area: " +
            selectedDistrict +
            ", " +
            stateName;


        map.setView(
            [data.latitude, data.longitude],
            10
        );
        if (districtBoundary) {
            map.removeLayer(districtBoundary);
            districtBoundary = null;
        }

        if (data.geometry) {
            districtBoundary = L.geoJSON(data.geometry).addTo(map);
            map.fitBounds(districtBoundary.getBounds());
        }

// -------------------------------------------------
// Load landslide red zone
// -------------------------------------------------

if (redZoneLayer) {
    map.removeLayer(redZoneLayer);
    redZoneLayer = null;
}

try {

    const redZoneResponse = await fetch(
        `/red-zone?state=${encodeURIComponent(stateName)}&district=${encodeURIComponent(selectedDistrict)}`
    );

    const redZoneData = await redZoneResponse.json();

    if (redZoneResponse.ok) {

        redZoneLayer = L.geoJSON(
    redZoneData,
    {
        style: {
            color: "red",
            weight: 1,
            fillColor: "red",
            fillOpacity: 0.45
        }
    }
).addTo(map);

redZoneLayer.bringToBack();
districtBoundary.bringToFront();

    }

} catch (error) {

    console.error(
        "Red-zone loading error:",
        error
    );

}
        //for north south east west boundary of district
        const bounds = districtBoundary.getBounds();
        const south = bounds.getSouth();
        const west = bounds.getWest();
        const north = bounds.getNorth();
        const east = bounds.getEast();
              
        const habitationResponse = await fetch(`/habitations?south=${south}&west=${west}&north=${north}&east=${east}`);
        const habitationData = await habitationResponse.json();
        if (!habitationResponse.ok) {
            throw new Error(
            habitationData.error ||
            "Unable to load habitation data."
            );
            }
        console.log("Habitations:", habitationData.habitations);

    } catch (error) {

        console.error("Geocoding error:", error);

        selectedArea.textContent =
            "Unable to locate selected area.";

        alert(
            "Could not find the selected district."
        );

    }

});


//leaftlet map

    //setting leaflet map view at pune co-ordinates with 10 zoom level
const map = L.map("map").setView( [18.5204, 73.8567] , 10);

    //map tiles
L.tileLayer(
    "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
        maxZoom: 19,
        attribution: "&copy; OpenStreetMap contributors"
    }
).addTo(map);
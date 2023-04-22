<!DOCTYPE html>
<html>
<head>
  <title>Leaflet and Turf.js Spatial Join</title>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
  <script src="https://unpkg.com/@turf/turf/turf.min.js"></script>
</head>
<body>
  <div id="map" style="width: 100%; height: 100vh;"></div>
  <script>
    // Initialize the map
    const map = L.map('map').setView([48.896465, 10.996526], 13);

    // Add a base map layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // Load the points and polygons GeoJSON files
    Promise.all([
      fetch('points.geojson').then(response => response.json()),
      fetch('polygons.geojson').then(response => response.json())
    ]).then(([points, polygons]) => {
      // Perform the spatial join
      points.features.forEach(point => {
        const matchedPolygons = polygons.features.filter(polygon =>
          turf.booleanPointInPolygon(point, polygon)
        );

        // Add the polygon property values to the point
        point.properties.poly_boundary = matchedPolygons.map(p => p.properties.iso).join(',');
      });

      // Add the layers to the map
      const pointsLayer = L.geoJSON(points).addTo(map);
      const polygonsLayer = L.geoJSON(polygons).addTo(map);

      // Print poly_boundary values for each point
      points.features.forEach(feature => {
        console.log(feature.properties.poly_boundary);
      });
    });
  </script>
</body>
</html>

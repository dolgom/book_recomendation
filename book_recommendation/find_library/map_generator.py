import json


def generate_html(lat, lng, libraries, api_key, output_file="lib.html"):
    libs_json = json.dumps(libraries, ensure_ascii=False)

    html = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>도서관 지도</title>
        <script src="https://maps.googleapis.com/maps/api/js?key={api_key}&callback=initMap" async defer></script>
        <script>
            function initMap() {{
                var center = {{ lat: {lat}, lng: {lng} }};
                var map = new google.maps.Map(document.getElementById('map'), {{
                    zoom: 12,
                    center: center
                }});

                new google.maps.Marker({{
                    position: center,
                    map: map,
                    title: "사용자 위치",
                    icon: "http://maps.google.com/mapfiles/ms/icons/blue-dot.png"
                }});

                var libraries = {libs_json};
                libraries.forEach(lib => {{
                    var marker = new google.maps.Marker({{
                        position: {{ lat: lib.lat, lng: lib.lng }},
                        map: map,
                        title: lib.name,
                        icon: "http://maps.google.com/mapfiles/ms/icons/red-dot.png"
                    }});

                    var infoWindow = new google.maps.InfoWindow({{
                        content: `<strong>${{lib.name}}</strong><br>거리: ${{lib.distance.toFixed(2)}}km<br><a href=\"${{lib.url}}\" target=\"_blank\">도서관 홈페이지</a>`
                    }});

                    marker.addListener("click", () => infoWindow.open(map, marker));
                }});
            }}
        </script>
    </head>
    <body>
        <h2>가까운 도서관 지도</h2>
        <div id="map" style="height: 500px; width: 100%;"></div>
    </body>
    </html>
    """

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html)

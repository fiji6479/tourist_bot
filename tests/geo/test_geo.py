from geo.geo import Points, Point


def test_get_closest_only_one_coordinate():
    js = [
        {
            "@id": "relation/227970",
            "tourism": "museum",
            "name": "Хач магаз",
            "centroid_coordinates": [59.901386, 30.455475]
        },
        {
            "@id": "relation/238571",
            "tourism": "museum",
            "alt_name": "Магнит",
            "name": "Магнит",
            "website": "http://www.rusmuseum.ru/info/",
            "centroid_coordinates": [59.900974, 30.457073]
        },
        {
            "@id": "relation/969622",
            "tourism": "museum",
            "name": "Школа",
            "website": "http://www.rusmuseum.ru/marble-palace/",
            "centroid_coordinates": [59.901552, 30.449005]
        }
    ]

    # ar = [js[k].get('centroid_coordinates') for k in range(len(js))]
    point_arr = []
    for e in js:
        coordinates = e.get('centroid_coordinates')
        point = Point(coordinates[0], coordinates[1], e.get("@id"))
        point_arr.append(point)

    points = Points(point_arr)
    latitude = 59.901606
    longitude = 30.454751
    radius = 100

    actual = points.get_closest(latitude, longitude, radius)
    expected = [Point(59.901386, 30.455475,'relation/227970')]
    print(expected)
    print(actual)
    assert actual == expected


def test_get_closest_no_coordinate():
    js = [
        {
            "@id": "relation/227970",
            "tourism": "museum",
            "name": "Хач магаз",
            "centroid_coordinates": [59.901386, 30.455475]
        },
        {
            "@id": "relation/238571",
            "tourism": "museum",
            "alt_name": "Магнит",
            "name": "Магнит",
            "website": "http://www.rusmuseum.ru/info/",
            "centroid_coordinates": [59.900974, 30.457073]
        },
        {
            "@id": "relation/969622",
            "tourism": "museum",
            "name": "Школа",
            "website": "http://www.rusmuseum.ru/marble-palace/",
            "centroid_coordinates": [59.901552, 30.449005]
        }
    ]



    point_arr = []
    for e in js:
        coordinates = e.get('centroid_coordinates')
        point = Point(coordinates[0], coordinates[1], e.get("@id"))
        point_arr.append(point)

    points = Points(point_arr)
    latitude = 59.901606
    longitude = 30.454751
    radius = 10

    actual = points.get_closest(latitude, longitude, radius)
    expected = []

    assert actual == expected


def test_get_closest_two_coordinate():
    js = [
        {
            "@id": "relation/227970",
            "tourism": "museum",
            "name": "Хач магаз",
            "centroid_coordinates": [59.901386, 30.455475]
        },
        {
            "@id": "relation/238571",
            "tourism": "museum",
            "alt_name": "Магнит",
            "name": "Магнит",
            "website": "http://www.rusmuseum.ru/info/",
            "centroid_coordinates": [59.900974, 30.457073]
        },
        {
            "@id": "relation/969622",
            "tourism": "museum",
            "name": "Школа",
            "website": "http://www.rusmuseum.ru/marble-palace/",
            "centroid_coordinates": [59.901552, 30.449005]
        }
    ]

    point_arr = []
    for e in js:
        coordinates = e.get('centroid_coordinates')
        point = Point(coordinates[0], coordinates[1], e.get("@id"))
        point_arr.append(point)

    points = Points(point_arr)
    latitude = 59.901606
    longitude = 30.454751
    radius = 250

    actual = points.get_closest(latitude, longitude, radius)
    expected = [Point(59.901386, 30.455475, 'relation/227970'), Point(59.900974, 30.457073,'relation/238571')]

    assert actual == expected

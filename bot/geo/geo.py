from geopy.distance import geodesic


class Points:
    def __init__(self, points: list):
        self.points = points

    def get_closest(self, lat, lon, radius) -> []:
        closest_points = []
        center_point = (lat, lon)

        for point in self.points:
            lat_lon = [point.lat, point.lon]
            distance = geodesic(center_point, lat_lon).meters
            if float(distance) <= float(radius):
                closest_points.append(point)

        return closest_points


class Point:
    def __init__(self, lat, lon, id):
        self.id = id
        self.lat = lat
        self.lon = lon

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.id == other.id \
                and self.lat == other.lat \
                and self.lon == other.lon
        return False

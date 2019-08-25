from math import *
from com.honwaii.learning.entity.coordinate import Coordinate
from com.honwaii.learning.entity.gps import Gps

semi_major_axis = 6378137
semi_minor_axis = 6356752.3142
first_rate_pow = 0.00669437999013
second_rate_pow = 0.006739496742227
first_rate = 0.0818191908425523
base_latitude = 30 * pi / 180
base_longitude = 120 * pi / 180


# 将经纬度坐标转换为墨卡托坐标
def lat_and_lng_to_mercator(gps):
    k = pow(semi_major_axis, 2) * cos(base_latitude) / (
            semi_minor_axis * sqrt(1 + second_rate_pow * pow(cos(base_latitude), 2)))
    q = log(tan(pi / 4 + gps.latitude / 2)) + (first_rate / 2) * log(
        (1 - first_rate * sin(gps.latitude) / (1 + first_rate * sin(gps.latitude))))
    y = k * q
    x = k * (gps.longitude - base_longitude)
    return Coordinate(x, y)


# 将墨卡托坐标转换为经纬度坐标
def mercator_to_lat_and_lng(coordinate):
    k = pow(semi_major_axis, 2) * cos(base_latitude) / (
            semi_minor_axis * sqrt(1 + second_rate_pow * pow(cos(base_latitude), 2)))
    lng = coordinate.x / k + base_longitude
    b = 40
    for i in range(50):
        b = pi / 2 - 2 * atan(pow(e, -coordinate.y / k) * pow(e, (first_rate / 2) * log(
            (1 - first_rate * sin(b) / (1 + first_rate * sin(b))))))
    return Gps(lng, b)


def degree_to_rad(degree):
    return degree * pi / 180


def rad_to_degree(rad):
    return rad * 180 / pi


gps = Gps(degree_to_rad(120.196581014400), degree_to_rad(30.18696840955181))
# gps = Gps(degree_to_rad(53), degree_to_rad(53))
mercator = lat_and_lng_to_mercator(gps)
print(mercator.x, ",", mercator.y)
g = mercator_to_lat_and_lng(mercator)
print(rad_to_degree(g.longitude), ",", rad_to_degree(g.latitude))

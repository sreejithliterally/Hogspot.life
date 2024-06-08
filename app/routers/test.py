from shapely.geometry import Polygon, Point

hyde_park_coordinates = [
    (9.997851713766739, 76.27272509479019),
    (9.997136615798388, 76.2725054061471),
    (9.996977880836917, 76.27278815157582),
     (9.997818542622017, 76.27304916336834),
     (9.997851713766739, 76.27272509479019),
    
]
hyde_park = Polygon(hyde_park_coordinates)
print(hyde_park)
someone_inside = Point(9.997553411062999, 76.27269458131059)

value = hyde_park.contains(someone_inside)  # returns True
print(value)

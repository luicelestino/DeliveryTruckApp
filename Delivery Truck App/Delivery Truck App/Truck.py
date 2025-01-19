# Creates a class for trucks
class Truck:
    # Create initializer that includes miles, location, package count, and the time of departure
    def __init__(self, speed, miles, address, packages, departureTime):
        self.speed = speed
        self.miles = miles
        self.address = address
        self.packages = packages
        self.departureTime = departureTime
        self.time = departureTime

    # Returns the truck object as a formatted string
    def __str__(self):
        return "%s, %s, %s, %s, %s" % (self.speed, self.miles, self.address, self.packages, self.departureTime)

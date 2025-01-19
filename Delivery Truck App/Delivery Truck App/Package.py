# Create a class for packages
import datetime


class Package:
    # Create initializer that includes the package ID, the address information, the weight, and the delivery status
    def __init__(self, ID, address, city, state, zipcode, deadline, weight, notes, deliveryStatus, departureTime,
                 deliveryTime):
        self.ID = ID
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.deliveryStatus = deliveryStatus
        self.departureTime = None
        self.deliveryTime = None

    # Returns the package object as a formatted string
    def __str__(self):
        return ("%s, %s, %s, %s, %s, %s, %s, %s, %s, Departure Time: %s, Delivery Time: %s" %
                (self.ID, self.address, self.city, self.state,
                 self.zipcode, self.deadline, self.weight, self.notes,
                 self.deliveryStatus, self.departureTime,
                 self.deliveryTime))

    def updateDeliveryStatus(self, convert_timedelta):
        if self.deliveryTime < convert_timedelta:
            self.deliveryStatus = "Delivered"
        elif self.departureTime > convert_timedelta:
            self.deliveryStatus = "En route"
        else:
            self.deliveryStatus = "At delivery hub"
        # Correct the package address for package 9
        if self.ID == 9:
            if convert_timedelta > datetime.timedelta(hours=10, minutes=20):
                self.address = "410 S State St"
                self.zipcode = "84111"

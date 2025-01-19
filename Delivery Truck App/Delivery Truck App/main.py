import csv
import datetime

from ChainingHashTable import ChainingHashTable
from Package import Package
from Truck import Truck

with open("CSV/addressCSV.csv") as csvfile:
    CSV_Address = csv.reader(csvfile)
    CSV_Address = list(CSV_Address)
    # print(CSV_Address)

with open("CSV/distanceCSV.csv") as csvfile:
    CSV_Distance = csv.reader(csvfile)
    CSV_Distance = list(CSV_Distance)
    # print(CSV_Distance)

with open("CSV/packageCSV.csv") as csvfile:
    CSV_Package = csv.reader(csvfile)
    CSV_Package = list(CSV_Package)
    # print(CSV_Package)


# Create package data from CSV package file
# Load package objects into the hash table
def loadPackageData(fileName):
    with open(fileName) as packageInfo:
        packageData = csv.reader(packageInfo, delimiter=',')
        for package in packageData:
            pID = int(package[0])
            pAddress = package[1]
            pCity = package[2]
            pState = package[3]
            pZipcode = package[4]
            pDeadline = package[5]
            pWeight = package[6]
            pNotes = package[7]
            pDeliveryStatus = "At delivery hub"
            pDepartureTime = None
            pDeliveryTime = None

            # Package object
            package = Package(pID, pAddress, pCity, pState, pZipcode, pDeadline, pWeight, pNotes,
                              pDeliveryStatus, pDepartureTime, pDeliveryTime)

            # insert it into the hash table
            packageHashTable.insert(pID, package)


# Finds address number from list of addresses
def findAddress(address):
    for row in CSV_Address:
        if address in row[2]:
            return int(row[0])


# Create a method that finds the distance between two addresses
def distanceBetween(xVal, yVal):
    distance = CSV_Distance[xVal][yVal]
    if distance == '':
        distance = CSV_Distance[yVal][xVal]

    return float(distance)


# Creates a ChainingHashTable object
packageHashTable = ChainingHashTable()

# Loads packages from the CSV file
loadPackageData('CSV/packageCSV.csv')

# Manually load the trucks with their package assignments

# Truck 1: 1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40
# Truck 2: 2, 3, 4, 5, 9, 10, 11, 17, 19, 22, 24, 26, 27, 35
# Truck 3: 6, 7, 8, 12, 18, 21, 23, 25, 28, 32, 33, 36, 38, 39

truck1 = Truck(18, 0, "4001 South 700 East", [1, 13, 14, 15, 16, 20, 29, 30, 31, 34, 37, 40],
               datetime.timedelta(hours=8))
truck2 = Truck(18, 0, "4001 South 700 East", [2, 3, 4, 5, 9, 10, 11, 17, 25, 22, 24, 26, 27, 35],
               datetime.timedelta(hours=10, minutes=20))
truck3 = Truck(18, 0, "4001 South 700 East", [6, 7, 8, 12, 18, 19, 21, 23, 28, 32, 33, 36, 38, 39],
               datetime.timedelta(hours=9, minutes=5))


# Orders package using nearest neighbor greedy algorithm
def deliverPackages(truck):
    # Put the packages that need to be delivered into an array
    needsDelivery = []
    for packageID in truck.packages:
        package = packageHashTable.search(packageID)
        needsDelivery.append(package)

    truck.packages.clear()

    # Loop through array needsDelivery
    # Append the nearest package until there are no more packages left
    while len(needsDelivery) > 0:
        nextAddress = 2000
        nextPackage = None
        # Loop through packages in array needsDelivery
        for package in needsDelivery:
            if distanceBetween(findAddress(truck.address), findAddress(package.address)) <= nextAddress:
                nextAddress = distanceBetween(findAddress(truck.address), findAddress(package.address))
                nextPackage = package
        # Adds package to the truck using the nextPackage ID
        truck.packages.append(nextPackage.ID)
        # Pops package from the needsDelivery list
        needsDelivery.remove(nextPackage)
        # Tallies up the miles driven by the truck
        truck.miles += nextAddress
        # Sets the trucks current address to the location it traveled to
        truck.address = nextPackage.address
        # Updates how long it took the truck to get to the package
        truck.time += datetime.timedelta(hours=nextAddress / 18)
        nextPackage.deliveryTime = truck.time
        nextPackage.departureTime = truck.departureTime


# Call function to deliver the packages for each truck object
deliverPackages(truck1)
deliverPackages(truck2)

# Makes sure truck 3 doesn't leave until a driver is available
truck3.departureTime = min(truck1.time, truck2.time)
deliverPackages(truck3)

class Main:
    # Create the user interface
    print("|***WGUPS Information***| \nThe total mileage for the deliveries are: ")
    print(truck1.miles + truck2.miles + truck3.miles)
    # Prompt user to start the program with the input "Start"
    startInput = input("To begin the search, please type 'start'")
    if startInput == "start":
        try:
            # Prompt user to input whether they want to view a single package or all of them
            typeInput = input("Please type 'single' if you would like to view a single package or 'all' to view all packages")
            # Prompt user to input a time to check the packages
            timeInput = input("Please enter a given time to check the status of your package. Use the format 'HH:MM'")
            (h, m) = timeInput.split(":")
            convert_timedelta = datetime.timedelta(hours=int(h), minutes=int(m))
            if typeInput == "single":
                try:
                    # Prompt the user to input a package ID for a single package
                    idInput = input("Enter the ID for the package you would like to view: ")
                    package = packageHashTable.search(int(idInput))
                    package.updateDeliveryStatus(convert_timedelta)
                    print(str(package))
                except ValueError:
                    print("Input was invalid. The program will now shut down.")
                    exit()
            elif typeInput == "all":
                try:
                    for packageID in range(1, 41):
                        package = packageHashTable.search(packageID)
                        package.updateDeliveryStatus(convert_timedelta)
                        print(str(package))
                except ValueError:
                    print("Input was invalid. The program will now shut down.")
                    exit()
            else:
                exit()
        except ValueError:
            print("Input was invalid. The program will now shut down.")
            exit()
    elif input != "start":
        print("The input was not 'start'. The program will now shut down.")

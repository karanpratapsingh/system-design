from parking_lot import ParkingLot
from vehicle import Car, Truck, Motorcycle, Van

name = input("Enter parking lot operator name: ")
parking_lot = ParkingLot(name)
while True:
    choice = input("Enter Parking choice.\n"
                   "1 Parking entry Gate.\n"
                   "2 Parking exit Gate.\n"
                   "3 Check parking status.\n"
                   "4 Check vehicle status.\n")
    try:
        choice = int(choice)
    except ValueError:
        print('Invalid choice type.')
    else:
        if choice == 1:
            vehicle_type = input("Enter vehicle type. \n"
                                 "1 Car.\n"
                                 "2 Motorcycle, \n"
                                 "3 Truck.\n"
                                 "4 Van\n")
            try:
                vehicle_type = int(vehicle_type)
            except ValueError:
                print('Invalid vehicle type.')
            else:
                if vehicle_type < 0 or vehicle_type > 4:
                    print('Invalid vehicle type.')
                else:
                    vehicle_number = input("Enter vehicle Number: ")
                    if vehicle_type == 1:
                        vehicle = Car(vehicle_number)
                    elif vehicle_type == 2:
                        vehicle = Motorcycle(vehicle_number)
                    elif vehicle_type == 3:
                        vehicle = Truck(vehicle_number)
                    else:
                        vehicle = Van(vehicle_number)

                    ticket_number = parking_lot.get_new_parking_ticket(vehicle)
                    print(f"Ticket number: {ticket_number}")
        elif choice == 2:
            ticket_number = input("Enter ticket Number: ")
            try:
                ticket_number = int(ticket_number)
            except ValueError:
                print("Invalid ticket number.")
            else:
                vehicle_number, parking_cost = parking_lot.leave_parking(ticket_number)
                print(f"Vehicle Number: {vehicle_number}. Parking cost: {parking_cost}.")
        elif choice == 3:
            parking_status = parking_lot.get_empty_spot_number()
            print(parking_status)
        elif choice == 4:
            ticket_number = input("Enter ticket Number: ")
            try:
                ticket_number = int(ticket_number)
            except ValueError:
                print("Invalid ticket number.")
            else:
                vehicle_status = parking_lot.vehicle_status(ticket_number)
                print(vehicle_status)

        else:
            print('Invalid choice')

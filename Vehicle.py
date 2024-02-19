from datetime import datetime

class Vehicle:
    def __init__(self, vehicle_type, entry_time, license_plate, ticket_id):
        self.vehicle_type = vehicle_type
        self.entry_time = entry_time
        self.license_plate = license_plate
        self.ticket_id = ticket_id


class ManageVehicles:
    def __init__(self):
        self.parking_lot = []

    def add_entry(self, vehicle):
        self.parking_lot.append(vehicle)

    def add_exit(self, vehicle_type, exit_time, license_plate, ticket_id, payment):
        for vehicle in self.parking_lot:
            if (vehicle.vehicle_type == vehicle_type and
                    vehicle.license_plate == license_plate and
                    vehicle.ticket_id == ticket_id):
                # Perform exit operations
                self.parking_lot.remove(vehicle)
                return True, payment
        return False, 0

    def count_parked_vehicles(self):
        return len(self.parking_lot)

    def display_sorted_vehicles(self, sort_by_entry_time=True, sort_ascending=True, filter_vehicle_type=None):
        sorted_list = sorted(self.parking_lot, key=lambda x: x.entry_time, reverse=not sort_ascending) if sort_by_entry_time else self.parking_lot
        if filter_vehicle_type:
            sorted_list = [vehicle for vehicle in sorted_list if vehicle.vehicle_type == filter_vehicle_type]
        for vehicle in sorted_list:
            print(f"Type: {vehicle.vehicle_type}, Entry Time: {vehicle.entry_time}, License Plate: {vehicle.license_plate}, Ticket ID: {vehicle.ticket_id}")

    def calculate_payment(self, vehicle_type, entry_time, exit_time):
        entry_hour = datetime.strptime(entry_time, "%H:%M").time().hour
        exit_hour = datetime.strptime(exit_time, "%H:%M").time().hour

        if entry_hour < 8 and exit_hour > 22:
            # Xe gửi qua ngày
            if vehicle_type == "Xe đạp":
                return 15000
            elif vehicle_type == "Xe máy":
                return 35000
        else:
            if entry_hour < 18 and exit_hour < 18:
                # Xe gửi và lấy trong ngày trước 18h
                if vehicle_type == "Xe đạp":
                    return 2000
                elif vehicle_type == "Xe máy":
                    return 3000
            elif entry_hour < 18 and 18 <= exit_hour <= 22:
                # Xe gửi trong ngày, lấy sau 18h và trước 22h
                if vehicle_type == "Xe đạp":
                    return 4000
                elif vehicle_type == "Xe máy":
                    return 6000
            else:
                # Xe gửi và lấy sau 22h
                if vehicle_type == "Xe đạp":
                    return 0  # Không tính phí cho xe đạp sau 22h
                elif vehicle_type == "Xe máy":
                    return 0  # Không tính phí cho xe máy sau 22h
        # Xử lý cho trường hợp xe bị mất thẻ gửi xe
        return "Phạt nộp thẻ gửi xe bị mất"

    def calculate_daily_revenue(self):
        current_time = datetime.now().time().hour
        if 8 <= current_time <= 22:
            total_revenue_bicycle = 0
            total_revenue_motorbike = 0
            for vehicle in self.parking_lot:
                entry_hour = datetime.strptime(vehicle.entry_time, "%H:%M").time().hour
                if entry_hour >= 8 and entry_hour <= 22:
                    payment = self.calculate_payment(vehicle.vehicle_type, vehicle.entry_time, datetime.now().strftime("%H:%M"))
                    if vehicle.vehicle_type == "Xe đạp":
                        total_revenue_bicycle += payment
                    elif vehicle.vehicle_type == "Xe máy":
                        total_revenue_motorbike += payment

            print("Doanh thu xe đạp:", total_revenue_bicycle)
            print("Doanh thu xe máy:", total_revenue_motorbike)
        else:
            print("Ngoài khung giờ tính doanh thu (8h-22h)")


    def get_alert_list(self):
        alert_list = []
        current_date = datetime.now().date()
        for vehicle in self.parking_lot:
            entry_date = datetime.strptime(vehicle.entry_time, "%Y-%m-%d").date()
            if vehicle.vehicle_type == "Xe đạp":
                if (current_date - entry_date) >= timedelta(days=3):
                    alert_list.append(vehicle)
            elif vehicle.vehicle_type == "Xe máy":
                if (current_date - entry_date) >= timedelta(days=5):
                    alert_list.append(vehicle)

        return alert_list

    def get_lost_ticket_vehicles(self):
        lost_ticket_vehicles = []
        current_time = datetime.now().time().hour
        if 8 <= current_time <= 22:
            current_date = datetime.now().date()
            for vehicle in self.parking_lot:
                entry_hour = datetime.strptime(vehicle.entry_time, "%H:%M").time().hour
                if entry_hour >= 8 and entry_hour <= 22:
                    if vehicle.ticket_id == "lost":
                        lost_ticket_vehicles.append(vehicle)

        return lost_ticket_vehicles

    def get_multiple_entries_vehicles(self):
        multiple_entries_vehicles = []
        current_time = datetime.now().time().hour
        if 8 <= current_time <= 22:
            current_date = datetime.now().date()
            entries_count = defaultdict(int)
            for vehicle in self.parking_lot:
                entry_hour = datetime.strptime(vehicle.entry_time, "%H:%M").time().hour
                if entry_hour >= 8 and entry_hour <= 22:
                    if vehicle.vehicle_type == "Xe máy":
                        entries_count[vehicle.license_plate] += 1

            for license_plate, count in entries_count.items():
                if count >= 2:
                    multiple_entries_vehicles.append(license_plate)

        return multiple_entries_vehicles

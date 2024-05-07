import datetime

class Vehicle:
    def __init__(self, make, model, year, mileage):
        self.make = make
        self.model = model
        self.year = year
        self.mileage = mileage
        self.maintenance_log = []
        self.insurance_details = {}

    def log_maintenance(self, type_of_service, date, mileage):
        service_record = {
            'type_of_service': type_of_service,
            'date': date,
            'mileage': mileage
        }
        self.maintenance_log.append(service_record)
        self.mileage = mileage

    def get_maintenance_history(self):
        return self.maintenance_log

    def update_mileage(self, new_mileage):
        self.mileage = new_mileage

    def get_average_mileage(self):
        if not self.maintenance_log:
            return 0
        total_mileage = sum(entry['mileage'] for entry in self.maintenance_log)
        return total_mileage / len(self.maintenance_log)

    def get_last_maintenance_details(self):
        if not self.maintenance_log:
            return None
        return self.maintenance_log[-1]

    def set_insurance_details(self, provider, policy_number):
        self.insurance_details = {'provider': provider, 'policy_number': policy_number}

    def get_insurance_info(self):
        return self.insurance_details

    def check_maintenance_due(self):
        if not self.maintenance_log:
            return True
        last_maintenance_date = datetime.datetime.strptime(self.maintenance_log[-1]['date'], '%Y-%m-%d')
        return (datetime.datetime.now() - last_maintenance_date).days > 180

    def __str__(self):
        return f"{self.year} {self.make} {self.model}, Mileage: {self.mileage} miles"

class FleetManager:
    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, make, model, year, mileage):
        new_vehicle = Vehicle(make, model, year, mileage)
        self.vehicles.append(new_vehicle)
        return new_vehicle

    def remove_vehicle(self, vehicle):
        self.vehicles.remove(vehicle)

    def find_vehicle_by_model(self, model):
        return [vehicle for vehicle in self.vehicles if vehicle.model == model]

    def record_maintenance(self, vehicle, type_of_service, date, mileage):
        vehicle.log_maintenance(type_of_service, date, mileage)

    def calculate_fuel_efficiency(self, vehicle, start_mileage, end_mileage, fuel_used):
        if fuel_used <= 0:
            raise ValueError("Fuel used must be greater than zero")
        distance_traveled = end_mileage - start_mileage
        if distance_traveled <= 0:
            raise ValueError("End mileage must be greater than start mileage")
        return distance_traveled / fuel_used

    def print_fleet_details(self):
        for vehicle in self.vehicles:
            print(vehicle)

    def find_vehicles_by_year_range(self, start_year, end_year):
        return [vehicle for vehicle in self.vehicles if start_year <= vehicle.year <= end_year]

    def find_vehicles_by_make(self, make):
        return [vehicle for vehicle in self.vehicles if vehicle.make == make]

    def get_fleet_maintenance_due(self):
        return [vehicle for vehicle in self.vehicles if vehicle.check_maintenance_due()]

    def get_fleet_insurance_info(self):
        return {vehicle: vehicle.get_insurance_info() for vehicle in self.vehicles}

    def log_fuel_usage(self, vehicle, date, mileage, fuel_used):
        vehicle.log_maintenance('Fuel Usage', date, mileage)
        maintenance_record = vehicle.get_last_maintenance_details()
        maintenance_record['fuel_used'] = fuel_used

    def print_maintenance_history(self, vehicle):
        print(f"Maintenance History for {vehicle.model}:")
        for entry in vehicle.maintenance_log:
            print(f"Date: {entry['date']}, Type of Service: {entry['type_of_service']}, Mileage: {entry['mileage']}")
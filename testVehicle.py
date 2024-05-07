import unittest
from vehicle_management_system import Vehicle, FleetManager

class TestVehicle(unittest.TestCase):
    def setUp(self):
        self.vehicle = Vehicle("Toyota", "Corolla", 2020, 25000)

    def test_log_maintenance(self):
        self.vehicle.log_maintenance("Oil change", "2023-05-10", 26000)
        self.assertEqual(len(self.vehicle.maintenance_log), 1)
        self.assertEqual(self.vehicle.mileage, 26000)

    def test_get_maintenance_history(self):
        self.vehicle.log_maintenance("Oil change", "2023-05-10", 26000)
        history = self.vehicle.get_maintenance_history()
        self.assertEqual(len(history), 1)

    def test_update_mileage(self):
        self.vehicle.update_mileage(27000)
        self.assertEqual(self.vehicle.mileage, 27000)

    def test_get_average_mileage(self):
        self.vehicle.log_maintenance("Service", "2023-05-10", 26000)
        self.vehicle.log_maintenance("Service", "2023-06-10", 27000)
        self.assertAlmostEqual(self.vehicle.get_average_mileage(), 26500)

    def test_get_last_maintenance_details(self):
        self.vehicle.log_maintenance("Oil change", "2023-05-10", 26000)
        last_maintenance = self.vehicle.get_last_maintenance_details()
        self.assertEqual(last_maintenance['type_of_service'], "Oil change")

    def test_set_insurance_details(self):
        self.vehicle.set_insurance_details("InsureCo", "12345")
        self.assertEqual(self.vehicle.get_insurance_info(), {'provider': 'InsureCo', 'policy_number': '12345'})

    def test_check_maintenance_due(self):
        self.vehicle.log_maintenance("Oil change", "2021-05-10", 26000)
        self.assertTrue(self.vehicle.check_maintenance_due())

    def test_log_multiple_maintenance(self):
        self.vehicle.log_maintenance("Oil change", "2023-05-10", 26000)
        self.vehicle.log_maintenance("Brake inspection", "2023-06-01", 26500)
        self.assertEqual(len(self.vehicle.maintenance_log), 2)
        self.assertIn('Brake inspection', [m['type_of_service'] for m in self.vehicle.maintenance_log])

    def test_insurance_details_update(self):
        self.vehicle.set_insurance_details("NewInsureCo", "54321")
        info = self.vehicle.get_insurance_info()
        self.assertEqual(info['provider'], "NewInsureCo")
        self.assertEqual(info['policy_number'], "54321")

    def test_maintenance_due_after_update(self):
        self.vehicle.log_maintenance("Oil change", "2022-11-01", 25000)
        self.assertFalse(self.vehicle.check_maintenance_due())

    def test_vehicle_str(self):
        self.assertEqual(str(self.vehicle), "2020 Toyota Corolla, Mileage: 25000 miles")

class TestFleetManager(unittest.TestCase):
    def setUp(self):
        self.fleet = FleetManager()
        self.vehicle1 = self.fleet.add_vehicle("Toyota", "Corolla", 2020, 25000)
        self.vehicle2 = self.fleet.add_vehicle("Honda", "Civic", 2019, 30000)

    def test_add_vehicle(self):
        self.assertEqual(len(self.fleet.vehicles), 2)

    def test_remove_vehicle(self):
        self.fleet.remove_vehicle(self.vehicle1)
        self.assertEqual(len(self.fleet.vehicles), 1)

    def test_find_vehicle_by_model(self):
        result = self.fleet.find_vehicle_by_model("Corolla")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], self.vehicle1)

    def test_record_maintenance(self):
        self.fleet.record_maintenance(self.vehicle1, "Oil change", "2023-05-10", 26000)
        self.assertEqual(len(self.vehicle1.maintenance_log), 1)

    def test_calculate_fuel_efficiency(self):
        efficiency = self.fleet.calculate_fuel_efficiency(self.vehicle1, 25000, 26000, 100)
        self.assertEqual(efficiency, 10.0)

    def test_find_vehicles_by_year_range(self):
        result = self.fleet.find_vehicles_by_year_range(2019, 2021)
        self.assertEqual(len(result), 2)

    def test_get_fleet_maintenance_due(self):
        self.vehicle1.log_maintenance("Oil change", "2021-05-10", 26000)
        due_vehicles = self.fleet.get_fleet_maintenance_due()
        self.assertIn(self.vehicle1, due_vehicles)

    def test_get_fleet_insurance_info(self):
        self.vehicle1.set_insurance_details("InsureCo", "12345")
        insurance_info = self.fleet.get_fleet_insurance_info()
        self.assertEqual(insurance_info[self.vehicle1], {'provider': 'InsureCo', 'policy_number': '12345'})

    def test_print_maintenance_history(self):
        self.vehicle1.log_maintenance("Oil change", "2023-05-10", 26000)
        with self.assertLogs(level='INFO') as log:
            self.fleet.print_maintenance_history(self.vehicle1)
            self.assertIn("Maintenance History for Corolla:", log.output[0])

    def test_find_vehicle_by_make(self):
        result = self.fleet.find_vehicles_by_make("Honda")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].make, "Honda")

    def test_fleet_fuel_efficiency(self):
        self.fleet.log_fuel_usage(self.vehicle1, "2023-05-12", 26000, 50)
        self.fleet.log_fuel_usage(self.vehicle2, "2023-05-12", 30500, 60)
        self.assertRaises(ValueError, self.fleet.calculate_fuel_efficiency, self.vehicle1, 26000, 26500, 0)

    def test_no_maintenance_due(self):
        self.vehicle1.log_maintenance("Oil change", "2023-04-01", 26000)
        self.assertFalse(self.vehicle1 in self.fleet.get_fleet_maintenance_due())

    def test_multiple_vehicles_by_year_range(self):
        vehicle3 = self.fleet.add_vehicle("Ford", "Focus", 2021, 15000)
        result = self.fleet.find_vehicles_by_year_range(2020, 2022)
        self.assertEqual(len(result), 2)

    def test_print_fleet_details(self):
        with self.assertLogs(level='INFO') as log:
            self.fleet.print_fleet_details()
            self.assertIn("Toyota Corolla", log.output[0])
            self.assertIn("Honda Civic", log.output[0])

if __name__ == '__main__':
    unittest.main()
from get_data import get_device_info
from database import Database_Config


database_config = Database_Config("124.71.179.195", "1433", "Kangde_Test", "sa", "Admin_1")
device_info = get_device_info(database_config)
print(device_info)
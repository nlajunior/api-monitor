from model.device import Device

class DeviceController():
    def __init__(self):
        self.device_model = Device()

    def get_devices_online(self, user_id=2):
       devices = []
       try:
           self.device_model.userid=user_id
           res = self.device_model.get_devices_online()

           for device in res:
               devices.append({
                   'device_id': device.id,
                   'device_status': device.status,
                   'device_mac': device.mac
                })

           status = 200
       except Exception as e:
            print(e)
            devices= []
            status = 400
       finally:
           
            return {
                'result': devices                
            }
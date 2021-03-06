from datetime import datetime
from datetime import date

from model.medicao import Medicao

class MedicaoController():

    def __init__(self):
        self.medicao_model = Medicao()

    def get_tests(self, limit):
        medicoes = []
        try:
            res = self.medicao_model.get_all(limit=limit)
            for registro in res:
                medicoes.append({
                    'id': registro.id,
                    'session_id': registro.session_id,
                    'fhr_value': registro.fhr_value,
                    'duration': registro.duration,
                    'date_created': registro.date_created.strftime('%d/%m/%Y'),
                    'device_id': registro.device_id 
                })
            status = 200
        except Exception as e:
            print(e)
            medicoes = []
            status = 400
        finally:
            return {
                'result': medicoes,
                'status': status
            }

    def get_tests_session_id(self, session_id, date_created, limit):
        medicoes = []
        try:
            print(session_id)
            self.medicao_model.session_id = session_id
            self.medicao_model.date_created=date_created

            res = self.medicao_model.get_for_session_id(limit=limit)
            for registro in res:
                medicoes.append({
                    'id': registro.id,
                    'session_id': registro.session_id,
                    'fhr_value': registro.fhr_value,
                    'duration': registro.duration,
                    'date_created': registro.date_created.strftime('%d/%m/%Y'),
                    'device_id': registro.device_id 
                })
            status = 200
        except Exception as e:
            print(e)
            medicoes = []
            status = 400
        finally:
            return {
                'result': medicoes,
                'status': status
            }
        
    def get_tests_date_created(self, date_created=date.today()):
        medicoes = []
        try:
            self.medicao_model.date_created = date_created
            res = self.medicao_model.get_for_date_created()

            for registro in res:
                medicoes.append({
                    'id': registro.id,
                    'session_id': registro.session_id,
                    'fhr_value': registro.fhr_value,
                    'duration': registro.duration,
                    'date_created': registro.date_created.strftime('%d/%m/%Y'), 
                    'device_id': registro.device_id 
                })
            status = 200
        except Exception as e:
            print(e)
            medicoes = []
            status = 400
        finally:
            return {
                'result': medicoes,
                'status': status
            }
    
    def save_test(self, obj):
        self.medicao_model.session_id = obj['session_id']
        self.medicao_model.fhr_value = obj['fhr_value']
        self.medicao_model.duration = obj['duration']
        self.medicao_model.device_id = obj['device_id']
        self.medicao_model.date_created = date.today()

        return self.medicao_model.save_test()  
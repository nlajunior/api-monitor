from datetime import datetime

from model.medicao import Medicao

class MedicaoController():

    def __init__(self):
        self.medicao_model = Medicao()

    def get_medicoes(self, limit):
        medicoes = []
        try:
            res = self.medicao_model.get_all(limit=limit)
            for registro in res:
                medicoes.append({
                    'id': registro.id,
                    'session_id': registro.session_id,
                    'fhr_value': registro.fhr_value,
                    'duration': registro.duration,
                    'date_created ': registro.date_created
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

    def get_medicoes_token(self, limit):
        medicoes = []
        try:
            res = self.medicao_model.get_medicoes_toquen(limit=limit)
            for registro in res:
                medicoes.append({
                    'id': registro.id,
                    'session_id': registro.session_id,
                    'fhr_value': registro.fhr_value,
                    'duration': registro.duration,
                    'date_created ': registro.date_created
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
        
    def get_medicoes_date_created(self, date_created):
        medicoes = []
        try:
            self.medicao_model.date_created=date_created
            
            res = self.medicao_model.get_medicoes_date()

            for registro in res:
                medicoes.append({
                    'id': registro.id,
                    'session_id': registro.session_id,
                    'fhr_value': registro.fhr_value,
                    'duration': registro.duration,
                    'date_created': registro.date_created
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
    
    def save_medicao(self, obj):
        self.medicao_model.session_id = obj['session_id']
        self.medicao_model.fhr_value = obj['fhr_value']
        self.medicao_model.duration = obj['duration']
        self.medicao_model.date_created = datetime.now()

        return self.medicao_model.save_medicao()  
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
                    'token': registro.token,
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
                    'token': registro.token,
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
        

  
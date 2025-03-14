import grpc
from concurrent import futures
import sumadorVector_pb2
import sumadorVector_pb2_grpc

class CentroCalculo(sumadorVector_pb2_grpc.CentroCalculoServicer):
    def __init__(self):
        #Se hace la conexión y stub con el operador 1
        self.canalOP1 = grpc.insecure_channel('10.43.96.56:50051')
        self.stubOP1 = sumadorVector_pb2_grpc.Operador1Stub(self.canalOP1)
        
        #Se hace la conexión y stub con el operador 2
        self.canalOP2 = grpc.insecure_channel('10.43.96.56:50052')
        self.stubOP2 = sumadorVector_pb2_grpc.Operador2Stub(self.canalOP2)

    def SumarVector(self, request, context):
        try:
            numeros = request.numeros
            mitad = len(numeros) // 2
            primeraParte = numeros[:mitad]
            segundaParte = numeros[mitad:]

            #Impresiones de confirmación
            print(f"[CentroCalculo] Recibido vector completo: {numeros}")
            print(f"[CentroCalculo] Primera parte enviada a Operador1: {primeraParte}")
            print(f"[CentroCalculo] Segunda parte pendiente de enviar a Operador2: {segundaParte}")

            #Se envia la primera parte al operador 1, mandando el vector como parte del request y queda almacenado el resultado en response1
            try:
                responseOP1 = self.stubOP1.SumarParcial(sumadorVector_pb2.SumaParcialRequest(numeros=primeraParte))
                print(f"[CentroCalculo] Respuesta de Operador1 (suma parcial): {responseOP1.sumaParcial}")
                suma_parcial = responseOP1.sumaParcial
            except grpc.RpcError as e:
                print(f"[CentroCalculo] Error al contactar Operador1: {e.code()} - {e.details()}")
                suma_parcial = sum(primeraParte)
                print(f"[CentroCalculo] Suma parcial calculada localmente: {suma_parcial}")

            #Se envia la segunda parte al operador 2, se manda la segunda parte del vector y la suma parcial anteriormente obtenida
            try:
                responseOP2 = self.stubOP2.SumarFinal(sumadorVector_pb2.SumaFinalRequest(
                    sumaParcial=suma_parcial,
                    numeros=segundaParte
                ))
                print(f"[CentroCalculo] Respuesta de Operador2 (suma final): {responseOP2.resultado}")
                resultado_final = responseOP2.resultado
            except grpc.RpcError as e:
                print(f"[CentroCalculo] Error al contactar Operador2: {e.code()} - {e.details()}")
                resultado_final = suma_parcial + sum(segundaParte)
                print(f"[CentroCalculo] Suma final calculada localmente: {resultado_final}")

            #Finalmente se manda el mensaje final al cliente
            return sumadorVector_pb2.SumaResponse(resultado=resultado_final)

        except grpc.RpcError as e:
            print(f"[CentroCalculo] Error: {e.code()} - {e.details()}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Error en la respuesta del servidor")
            return sumadorVector_pb2.SumaResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sumadorVector_pb2_grpc.add_CentroCalculoServicer_to_server(CentroCalculo(), server)
    server.add_insecure_port('[::]:50050')
    print("[CentroCalculo] Servidor iniciado en el puerto 50050")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

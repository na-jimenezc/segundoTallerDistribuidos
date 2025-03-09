import grpc
from concurrent import futures
import sumadorVector_pb2
import sumadorVector_pb2_grpc

class ServidorCalculo2(sumadorVector_pb2_grpc.CentroCalculoServicer):
    TIMEOUT1 = 5
    TIMEOUT2 = 5

    def __init__(self):
        # Conexión al Operador 1 en el puerto 50051
        self.canalOP1 = grpc.insecure_channel('localhost:50051')
        self.stubOP1 = sumadorVector_pb2_grpc.Operador1Stub(self.canalOP1)

        # Conexión al Operador 2 en el puerto 50052
        self.canalOP2 = grpc.insecure_channel('localhost:50052')
        self.stubOP2 = sumadorVector_pb2_grpc.Operador2Stub(self.canalOP2)

    def SumarVector(self, request, context):
        try:
            numeros = request.numeros

            # Separamos el vector en dos grupos:
            # - Números en posiciones pares (0, 2, 4, ...)
            # - Números en posiciones impares (1, 3, 5, ...)
            numeros_pares = [num for i, num in enumerate(numeros) if i % 2 == 0]
            numeros_impares = [num for i, num in enumerate(numeros) if i % 2 != 0]

            # Enviar los números en posiciones pares al Operador 1 para obtener una suma parcial
            responseOP1 = self.stubOP1.SumarParcial(
                sumadorVector_pb2.VectorRequest(numeros=numeros_pares),
                timeout=self.TIMEOUT1
            )

            # Enviar la suma parcial y los números en posiciones impares al Operador 2 para obtener la suma final
            responseOP2 = self.stubOP2.SumarFinal(
                sumadorVector_pb2.SumaParcialRequest(
                    sumaParcial=responseOP1.sumaParcial,
                    numeros=numeros_impares
                ),
                timeout=self.TIMEOUT2
            )

            # Devolver el resultado final al cliente
            return sumadorVector_pb2.SumaResponse(resultado=responseOP2.resultado)

        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                print(f"Error: Tiempo de espera agotado en alguno de los operadores ({e.code()})")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Error en la respuesta del servidor de operaciones")
            else:
                print(f"Error: {e.code()} - {e.details()}")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Error interno en el servidor de cálculo 2")
            return sumadorVector_pb2.SumaResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    # Se añade el servicio del Servidor de Cálculo 2
    sumadorVector_pb2_grpc.add_CentroCalculoServicer_to_server(ServidorCalculo2(), server)
    # Se utiliza un puerto diferente para evitar conflictos (por ejemplo, 50060)
    server.add_insecure_port('[::]:50060')
    server.start()
    print("Servidor de Cálculo 2 iniciado en el puerto 50060")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

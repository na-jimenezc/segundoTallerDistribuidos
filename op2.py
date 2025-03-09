import grpc
from concurrent import futures
import sumadorVector_pb2
import sumadorVector_pb2_grpc

class Operador2(sumadorVector_pb2_grpc.Operador2Servicer):
    def SumarFinal(self, request, context):
        try:
            # Se extrae la suma parcial y la lista de números recibida
            suma_parcial = request.sumaParcial
            numeros = request.numeros

            # Se calcula la suma final: suma parcial + suma de los números adicionales
            suma_final = suma_parcial + sum(numeros)

            # Se retorna el resultado en un mensaje SumaResponse
            return sumadorVector_pb2.SumaResponse(resultado=suma_final)
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error en Operador2: {str(e)}")
            return sumadorVector_pb2.SumaResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sumadorVector_pb2_grpc.add_Operador2Servicer_to_server(Operador2(), server)
    # Se define el puerto en el que Operador 2 escuchará (50052 en este ejemplo)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Operador 2 escuchando en el puerto 50052...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
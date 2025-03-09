import grpc
from concurrent import futures
import sumadorVector_pb2
import sumadorVector_pb2_grpc

class Operador1(sumadorVector_pb2_grpc.Operador1Servicer):
    def SumarParcial(self, request, context):
        try:
            # vectorsito
            numeros = request.numeros
            suma_parcial = sum(numeros)
            # devolver la suma y el arreglo vacio para el centrico de calculo
            return sumadorVector_pb2.SumaParcialResponse(sumaParcial=suma_parcial,numeros=[])
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error en Operador1: {str(e)}")
            return sumadorVector_pb2.SumaParcialResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sumadorVector_pb2_grpc.add_Operador1Servicer_to_server(Operador1(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Operador 1 escuchando en el puerto 50051...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
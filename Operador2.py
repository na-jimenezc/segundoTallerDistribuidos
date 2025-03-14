import grpc
from concurrent import futures
import sumadorVector_pb2
import sumadorVector_pb2_grpc

class Operador2(sumadorVector_pb2_grpc.Operador2Servicer):
    def SumarFinal(self, request, context):
        try:
            print(f"[Operador2] Recibido suma parcial: {request.sumaParcial}")
            print(f"[Operador2] Recibido vector para sumar: {request.numeros}")

            suma_final = request.sumaParcial + sum(request.numeros)
            print(f"[Operador2] Resultado suma final: {suma_final}")

            return sumadorVector_pb2.SumaResponse(resultado=suma_final)
        except Exception as e:
            print(f"[Operador2] Error: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Error en Operador2: {str(e)}")
            return sumadorVector_pb2.SumaResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    sumadorVector_pb2_grpc.add_Operador2Servicer_to_server(Operador2(), server)
    server.add_insecure_port('[::]:50052')
    print("[Operador2] Servidor iniciado en el puerto 50052")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

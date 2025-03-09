import grpc
from concurrent import futures
import sumadorVector_pb2
import sumadorVector_pb2_grpc

class CentroCalculo(sumadorVector_pb2_grpc.CentroCalculoServicer):
    TIMEOUT1 = 5
    TIMEOUT2 = 5
    #aqui defino los timeouts para ver si se tarda mucho la respuesta de los operadores, si es asi lanza error
    def __init__(self):
        #Se da la conexión al operador 1 en 50051
        self.canalOP1 = grpc.insecure_channel('localhost:50051')
        self.stubOP1 = sumadorVector_pb2_grpc.Operador1Stub(self.canalOP1)

        #Se da la conexión al operador 2 en 50052
        self.canalOP2 = grpc.insecure_channel('localhost:50052')
        self.stubOP2 = sumadorVector_pb2_grpc.Operador2Stub(self.canalOP2)

    def SumarVector(self, request, context):
        try:
            '''Se divide al vector recibido en 2 partes'''
            numeros = request.numeros
            mitad = len(numeros)//2
            primeraParte = numeros[:mitad]
            segundaParte = numeros[mitad:]

            '''Se envia la primera parte al operador 1 y se espera al response para enviar a la otra parte'''
            responseOP1 = self.stubOP1.SumarParcial(sumadorVector_pb2.VectorRequest(numeros=primeraParte),timeout=TIMEOUT1) #type: ignore

            '''Se envia segunda parte al operador 2 y se espera al response final'''
            responseOP2 = self.stubOP2.SumarFinal(sumadorVector_pb2.SumaParcialRequest(
                sumaParcial=responseOP1.sumaParcial,
                numeros=segundaParte
            ),timeout=TIMEOUT2) # type: ignore

            '''Una vez se tiene el response final, se devuelve al cliente. De lo contrario sale el error'''
            return sumadorVector_pb2.SumaResponse(resultado=responseOP2.resultado)

        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                print(f"Error: {e.code()}")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Error en la respuesta del servidor")
            else :
                print(f"Error: {e.code()}")
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Error interno del servidor")
        return sumadorVector_pb2.SumaResponse()

    def serve():
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        sumadorVector_pb2_grpc.add_CentroCalculoServicer_to_server(CentroCalculo(), server)

        #Se escucha en el puerto 50050 por el cliente
        server.add_insecure_port('[::]:50050')
        server.start()
        server.wait_for_termination()

    if __name__ == '__main__':
        serve()
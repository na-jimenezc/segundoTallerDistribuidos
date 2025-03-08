import grpc
import sumadorVector_pb2
import sumadorVector_pb2_grpc

def run():
        '''Se solicita ingresar los números y después se convierten a un vector entero tomando en cuenta
        ///las comas'''
        input_numeros = input("Ingrese los números separados por comas (ejemplo: 1,2,3,4): ")
        numeros = [int(numero) for numero in input_numeros.split(",")]  

        '''Nos conectamos al canal para recibir y enviar mensajes con el centro de calculo y se llama
        ///al STUB para poder usar los métodos necesarios'''
        channel = grpc.insecure_channel('localhost:50050')
        stub = sumadorVector_pb2_grpc.CentroCalculoStub(channel)

        '''Finalmente se envia el vector en el forma del VECTORREQUEST y se espera a la respuesta'''
        response = stub.SumarVector(sumadorVector_pb2.VectorRequest(numeros=numeros))
        print(f"Resultado de la suma: {response.resultado}")

if __name__ == '__main__':
        run()

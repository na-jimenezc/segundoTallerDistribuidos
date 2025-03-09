import grpc
import sumadorVector_pb2
import sumadorVector_pb2_grpc
import time

TIMEOUTCLIENT = 10
MAX_INTENTOS = 3  

def run():
        '''Se solicita ingresar los números y después se convierten a un vector entero tomando en cuenta
        ///las comas'''
        input_numeros = input("Ingrese los números separados por comas (ejemplo: 1,2,3,4): ")
        numeros = [int(numero) for numero in input_numeros.split(",")]

        '''Nos conectamos al canal para recibir y enviar mensajes con el centro de calculo y se llama
        ///al STUB para poder usar los métodos necesarios'''
        channel = grpc.insecure_channel('127.0.0.1:50050')
        stub = sumadorVector_pb2_grpc.CentroCalculoStub(channel)

        '''Finalmente se envia el vector en el forma del VECTORREQUEST y se espera a la respuesta'''
        reintentos = 0
        while reintentos < MAX_INTENTOS:
                try:
                        response = stub.SumarVector(sumadorVector_pb2.VectorRequest(numeros=numeros), timeout=TIMEOUTCLIENT)
                        print(f"Resultado de la suma: {response.resultado}")
                        return

                except grpc.RpcError as e:
                        reintentos += 1
                        if e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
                                print(f"\nError: Tiempo de espera agotado ({TIMEOUTCLIENT}s).")
                        elif e.code() == grpc.StatusCode.UNAVAILABLE:
                                print("\nError: Servidor no disponible.")
                        elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
                                print("\nError: Datos enviados inválidos, solo se pueden ingresar enteros.")
                        else:
                                print(f"\nError inesperado: {e.details()}")
                                break
                        if reintentos < MAX_INTENTOS:
                                print(f"Reintentando ({reintentos}/{MAX_INTENTOS})...")
                                time.sleep(1) #Y se pone a dormir para dar espacio entre intentos de conexión
                        else:
                                print("No se pudo completar la operación.")
                                break

if __name__ == '__main__':
        run()

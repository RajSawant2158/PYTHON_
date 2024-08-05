# import cv2
# import socket
# import struct
# import pickle
#
# # Client (Receiving Device)
# def client_receive(host='192.168.140.226', port=9999):
#     # Set up the socket
#     client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     client_socket.connect((host, port))
#
#     data = b""
#     payload_size = struct.calcsize("Q")
#
#     while True:
#         while len(data) < payload_size:
#             packet = client_socket.recv(1*360)  # 4K buffer size
#             if not packet: break
#             data += packet
#
#         packed_msg_size = data[:payload_size]
#         data = data[payload_size:]
#         msg_size = struct.unpack("Q", packed_msg_size)[0]
#
#         while len(data) < msg_size:
#             data += client_socket.recv(1*360)
#
#         frame_data = data[:msg_size]
#         data = data[msg_size:]
#
#         frame = pickle.loads(frame_data)
#         cv2.imshow("Receiving Video", frame)
#
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#
#     # Release resources
#     client_socket.close()
#     cv2.destroyAllWindows()
#
# if __name__ == '__main__':
#     client_receive()
#
#
#
#
#
import socket
import threading

def start_client(host='192.168.140.56', port=9999):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f"Connected to server at {host}:{port}")

        def receive_messages():
            while True:
                try:

                    message = client_socket.recv(1024).decode()
                    if not message:
                        print("Connection closed by server")
                        break
                    print(f"Server: {message}")
                except Exception as e:
                    print(f"Error receiving message: {e}")
                    break

        def send_messages():
            while True:
                try:
                    message = input("Client: ")
                    client_socket.sendall(message.encode())
                except Exception as e:
                    print(f"Error sending message: {e}")
                    break

        recv_thread = threading.Thread(target=receive_messages)
        send_thread = threading.Thread(target=send_messages)

        recv_thread.start()
        send_thread.start()

        recv_thread.join()
        send_thread.join()

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == '__main__':
    start_client()

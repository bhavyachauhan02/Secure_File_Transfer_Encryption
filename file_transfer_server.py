import socket
from encryption_utils import derive_key, receive_file

def main():
    host = '127.0.0.1'
    port = 12345
    password = input("Enter a password for encryption: ")
    salt = b'\x82\x1c\x92\xff\xa3\xeb\x98\xc3\xbc\xb0\xa1(\x10|\xdf\x19'  # Use a secure method to generate salt
    key = derive_key(password, salt)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)

    print(f"Server listening on {host}:{port}")

    connection, address = server_socket.accept()
    print(f"Connection from {address}")

    # Example: Receiving a file securely
    receive_file(connection, 'received_example.txt', key)

    connection.close()
    server_socket.close()

if __name__ == "__main__":
    main()

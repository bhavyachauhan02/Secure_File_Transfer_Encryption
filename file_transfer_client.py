import socket
from encryption_utils import derive_key, send_file

def main():
    host = '127.0.0.1'
    port = 12345
    password = input("Enter a password for encryption: ")
    salt = b'\x82\x1c\x92\xff\xa3\xeb\x98\xc3\xbc\xb0\xa1(\x10|\xdf\x19'  # Use the same salt as the server
    key = derive_key(password, salt)

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Example: Sending a file securely
    send_file(client_socket, 'example.txt', key)

    client_socket.close()

if __name__ == "__main__":
    main()

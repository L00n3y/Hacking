import os, re, socket, threading, struct
from ctypes import *


def read_file(filename):  # ctypes
    file_handle = windll.Kernel32.CreateFileA(filename, 0x10000000, 0, 0, 3, 0x80, 0)

    if file_handle == -1:
        return -1

    data = create_string_buffer(4096)
    data_read = c_int(0)
    bool_succes = windll.Kernel32.ReadFile(file_handle, byref(data), 4096, byref(data_read), 0)
    windll.CloseHandle(file_handle)

    if bool_succes == 0:
        return -1

    return data.value


def create_file(filename, data):  # ctypes
    file_handle = windll.Kernel32.CreateFileA(filename, 0x10000000, 0, 0, 2, 0x80, 0)
    if file_handle == -1:

        return -1

    data_writen = c_int(0)
    bool_succes = windll.Kernel32.WriteFile(file_handle, data, len(data), byref(data_writen), 0)
    windll.Kernel32.CloseHandle(file_handle)

    if bool_succes == 0:
        return -1

    return


def recv_data(sock):  # Implement a networking protocol
    data_len = struct.unpack("!I", sock.recv(4))
    return sock.recv(data_len)


def send_data(sock, data):  # Implement a networking protocol
    data_len = len(data)
    sock.send(struct.pack("!I", data_len))
    sock.send(data)
    return


def search_drive(file_name):  # DRIVESEARCH
    re_obj = re.compile(file_name)
    for root, dirs, files in os.walk("C:\\"):
        for i in files:
            if re.search(re_obj, i):
                return os.path.join(root, i)

    return - 1


def search_directory(file_name):  # DIRSEARCH
    re_obj = re.compile(file_name)
    for root, dirs, files in os.walk(os.getcwd()):
        for i in files:
            if re.search(re_obj, i):
                return os.path.join(root, i)

    return -1


def send_file_contents(file_name, usersock, userinfo):  # DOWNLOADS
    send_data(usersock, read_file(file_name))
    return


def recieve_file_contents(file_name, usersock): # UPLOADS
    if create_file(file_name, recv_data(usersock)) == -1:
        send_data(usersock, "FILE CREATION FAILED!")
    return


def handle_connections(usersock, userinfo):

    command_list = ["DRIVESEARCH", "DIRSEARCH", "DOWNLOADS", "UPLOADS", "CLOSE"]
    continue_bool = True

    while continue_bool:
        send_data(usersock, "COMMAND")
        command = recv_data(usersock).upper()

        if command == "DRIVESEARCH":
            send_data(usersock, "Filename: ")
            search_results = search_drive(recv_data(usersock))

            if search_results == -1:
                send_data(usersock, "FILE NOT FOUND")
            else:
                send_data(usersock, search_results)

        elif command == "DIRSEARCH":
            send_data(usersock, "Filename: ")
            search_results = search_directory(recv_data(usersock))

            if search_results == -1:
                send_data(usersock, "FILE NOT FOUND")
            else:
                send_data(usersock, search_results)

        elif command == "DOWNLOAD":
            send_data(usersock, "Filename: ")
            send_file_contents(recv_data(usersock), usersock, userinfo)

        elif command == "UPLOAD":
            send_data(usersock, "Filename: ")
            recieve_file_contents(recv_data(usersock), usersock)

        elif command == "CLOSE":
            # exits
            continue_bool = False

        else:
            send_data(usersock, "INVALID COMMAND")

    return


def main():

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('', 55555))
    server_sock.listen(0)
    usersock, userinfo = server_sock.accept()
    conn_thread = threading.Thread(None, handle_connections, None, (usersock, userinfo))
    conn_thread.start()

    return


if __name__ == '__main__':
    main()

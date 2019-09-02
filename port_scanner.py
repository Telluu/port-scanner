#!/usr/bin/python3

import socket
import threading
import time
import json


def main():
    while True:
        target = socket.gethostbyname(input('Enter target IP: '))

        print('1. Load custom lists')
        print('2. Specify range')
        print('3. Specify port')
        option = input('Option: ')

        if option == '1':
            print('\nAvaliable lists:')
            with open('custom_lists.json') as custom_lists:
                custom_lists = json.load(custom_lists)

            for i, k in enumerate(custom_lists):
                print(f'{i + 1}. {k}')
            option = int(input('Option: '))

            if option > 0 and option <= len(custom_lists):
                for index, category in enumerate(custom_lists):
                    if (option - 1) == index:
                        custom_list = custom_lists[category]
                        choise = category
                        break
            else:
                print(f'There is no category with index {option}.\n')
                time.sleep(2)
                main()

        elif option == '2':
            start_from = int(input('From: '))
            stop_on = int(input('To: '))
            custom_list = range(start_from, stop_on)
            choise = f'Custom range FROM: {start_from} TO: {stop_on}'

        elif option == '3':
            port = int(input('Port: '))
            custom_list = [port]
            choise = f'Check port {port}'

        else:
            print(f'Invalid option {option}!\n')
            time.sleep(1)
            main()

        clock_start = time.time()

        print(f'\n\nStarting port scan for {target} | OPTION: {choise}')
        print('========================================================')
        print('PORT    STATE  SERVICE')
        for port in custom_list:
            t = threading.Thread(target=port_scan, args=(target, port))
            t.start()
        t.join()
        print('========================================================')
        print(f'Scan done in {round((time.time() - clock_start), 2)}s\n\n')


def port_scan(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((ip, port))
        sock.close()
        state = 'open'
    except:
        return
    service = socket.getservbyport(port)
    print(f'{port}{" " * (8 - len(str(port)))}{state}{" " * (7 - len(state))}{service}')


if __name__ == '__main__':
    main()

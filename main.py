
import argparse

from app import Main_Window

from wallet import Wallet

def check_port(port):
    if int(port) < 0 or int(port) > 9999:
        raise argparser.ArgumentTypeError("input port {} out of range [0-9999]".format(int(port)))
    return int(port)

if __name__ == '__main__':
   
    parser = argparse.ArgumentParser(description="Build-My-Own-Blockchain")
    parser.add_argument("-u", "--user-interface", action="store_true", default=False,  help="enable user interface")
    parser.add_argument("-i", "--ip-hosting", type=str, default="127.0.0.1", help="specify hosting ip address")
    parser.add_argument("-p", "--port-hosting", type=check_port, default="9527", help="specift hosting port number")

    args = parser.parse_args()

    wallet = Wallet(args.ip_hosting, args.port_hosting, 'mykey.txt')
    wallet.listen()

    App = Main_Window(wallet, args.user_interface)

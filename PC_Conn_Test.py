import socket
import subprocess

def get_ip_address():
    try:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return ip_address
    except socket.error:
        return None

def ping(host):
    try:
        output = subprocess.check_output(['ping', '-n', '1', host], stderr=subprocess.STDOUT, universal_newlines=True)
        if "TTL=" in output:
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False

def nslookup(host):
    try:
        output = subprocess.check_output(['nslookup', host], stderr=subprocess.STDOUT, universal_newlines=True)
        return output
    except subprocess.CalledProcessError as e:
        return str(e)

def main():
    ip_address = get_ip_address()
    if not ip_address:
        print("No IP found")
        return

    print(f"IP Address detected: {ip_address}")

    # Assuming the local gateway is the first IP in the subnet
    gateway = '.'.join(ip_address.split('.')[:-1]) + '.1'
    if not ping(gateway):
        print("No connection: Unable to reach local gateway")
        return

    print("Local gateway ping successful")

    if not ping('8.8.8.8'):
        print("No connection: Unable to reach Google DNS")
        return

    print("Google DNS ping successful")

    nslookup_result = nslookup('google.com')
    print("NSLookup result for google.com:")
    print(nslookup_result)

if __name__ == "__main__":
    main()
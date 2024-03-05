# ----------------------------------------------
#                  ><~|~/<  
# ----------------------------------------------

import sys, argparse, requests
from concurrent.futures import ThreadPoolExecutor
from requests.exceptions import RequestException

# Setup command-line argument parsing
parser = argparse.ArgumentParser(description='Port Scanner with Proxy Support')
parser.add_argument('-p', '--proxy_url', type=str, help='Proxy URL (e.g., http://127.0.0.1:8080)', required=False)
args = parser.parse_args()

# Check if the proxy_url argument is provided, if not log usage and exit
if not args.proxy_url:
    print("Usage: python3 scanner.py --proxy_url <PROXY_URL> (e.g., http://127.0.0.1:8080)")
    sys.exit(1)

# Configuration variables:
proxy_url = args.proxy_url  # Use the proxy_url from the command-line argument
num_workers = 100  # Adjust number of concurrent workers
num_ports = 65535  # Adjust the range of ports to scan

session = requests.Session()
session.proxies = {'http': proxy_url, 'https': proxy_url}

def check_port(port):
    address = f"http://127.0.0.1:{port}"
    try:
        response = session.get(address, timeout=3)
        if "The requested URL could not be retrieved" not in response.text:
            print(f"Port {port} found!")
            return port
    except RequestException:
        pass
    return None

def main():
    print(f"\nLooking for open ports... ")
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        results = list(executor.map(check_port, range(1, num_ports + 1), chunksize=len(range(1, num_ports + 1))//num_workers))
        open_ports = [port for port in results if port is not None]

if __name__ == "__main__":
    main()

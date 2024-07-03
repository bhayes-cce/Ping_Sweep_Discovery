import argparse
import ping3
import socket

def ping_sweep(start_ip, end_ip):
    # Perform ping sweep
    reachable_hosts = []
    start_ip_split = start_ip.split('.')
    end_ip_split = end_ip.split('.')

    for i in range(int(start_ip_split[3]), int(end_ip_split[3]) + 1):
        ip = f'{start_ip_split[0]}.{start_ip_split[1]}.{start_ip_split[2]}.{i}'
        print(f"Pinging {ip}...")
        response = ping3.ping(ip, timeout=1)  # Adjust timeout as needed
        if response is not None:
            print(f"  {ip} is reachable (round-trip time: {response} ms)")
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                print(f"  Hostname: {hostname}")
            except socket.herror:
                print(f"  Hostname: (not available)")
            reachable_hosts.append((ip, hostname if 'hostname' in locals() else None))
        else:
            print(f"  {ip} is not reachable")

    return reachable_hosts

def export_to_file(reachable_hosts, output_file):
    with open(output_file, 'w') as file:
        for ip, hostname in reachable_hosts:
            if hostname:
                file.write(f"{ip},{hostname}\n")
            else:
                file.write(f"{ip}\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform IP ping sweep and export online hosts to a file.')
    parser.add_argument('start_ip', type=str, help='Starting IP address (e.g., 192.168.1.1)')
    parser.add_argument('end_ip', type=str, help='Ending IP address (e.g., 192.168.1.254)')
    parser.add_argument('--output', '-o', type=str, default='reachable_hosts.txt', help='Path to output file (default: reachable_hosts.txt)')
    
    args = parser.parse_args()

    start_ip = args.start_ip
    end_ip = args.end_ip
    output_file = args.output

    reachable_hosts = ping_sweep(start_ip, end_ip)

    export_to_file(reachable_hosts, output_file)

    print(f"\nOnline hosts exported to {output_file}.")

import socket
import dns.resolver
import threading
import argparse


class DNSResolverApp:
    def __init__(self):
        self.resolver = dns.resolver.Resolver()

    def set_dns_server(self, dns_ip):
        """Set a custom DNS server."""
        self.resolver.nameservers = [dns_ip]
        print(f"DNS server set to {dns_ip}")

    def resolve_domain(self, domain):
        """Resolve a domain to multiple IP addresses using threads."""
        try:
            ips = set()
            threads = []

            def resolve_in_thread():
                nonlocal ips
                try:
                    answers = self.resolver.resolve(domain, 'A', lifetime=5)
                    ips.update(answer.to_text() for answer in answers)
                except Exception as e:
                    print(f"Error resolving domain {domain} in thread: {e}")

            for _ in range(5):
                thread = threading.Thread(target=resolve_in_thread)
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            if ips:
                print(f"IP addresses for {domain}: {', '.join(ips)}")
            else:
                print(f"No IP addresses found for {domain}")
        except Exception as e:
            print(f"Error resolving domain {domain}: {e}")

    @staticmethod
    def resolve_ip(ip):
        """Resolve an IP address to its associated domain names."""
        try:
            hostnames = socket.gethostbyaddr(ip)
            print(f"Domains for IP {ip}: {', '.join(hostnames[1])}")
        except Exception as e:
            print(f"Error resolving IP {ip}: {e}")

    @staticmethod
    def is_valid_ip(ip):
        """Validate an IP address."""
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False


def main():
    parser = argparse.ArgumentParser(description="DNS Resolver App")

    parser.add_argument('-u', '--dns', type=str, help="Custom DNS server IP")
    parser.add_argument('-d', '--domain', type=str, help="Domain to resolve")
    parser.add_argument('-i', '--ip', type=str, help="IP address to resolve")

    args = parser.parse_args()

    app = DNSResolverApp()

    if args.dns:
        if app.is_valid_ip(args.dns):
            app.set_dns_server(args.dns)
        else:
            print(f"Invalid DNS server IP: {args.dns}")
            return

    if args.domain:
        app.resolve_domain(args.domain)
    elif args.ip:
        app.resolve_ip(args.ip)
    else:
        print("Please provide either a domain with '-d' or an IP with '-i'.")


if __name__ == "__main__":
    main()

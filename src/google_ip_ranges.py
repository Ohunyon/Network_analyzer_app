# Google IP ranges
# Source: https://www.gstatic.com/ipranges/goog.json
GOOGLE_IP_RANGES = [
    '34.64.0.0/10',     # Google Cloud
    '34.128.0.0/10',    # Google Cloud
    '35.184.0.0/13',    # Google Cloud
    '35.192.0.0/14',    # Google Cloud
    '35.196.0.0/15',    # Google Cloud
    '35.198.0.0/16',    # Google Cloud
    '35.199.0.0/17',    # Google Cloud
    '35.200.0.0/13',    # Google Cloud
    '35.208.0.0/12',    # Google Cloud
    '35.224.0.0/12',    # Google Cloud
    '35.240.0.0/13',    # Google Cloud
    '64.233.160.0/19',  # Google Services
    '66.102.0.0/20',    # Google Services
    '66.249.64.0/19',   # Google Services
    '70.32.128.0/19',   # Google Services
    '72.14.192.0/18',   # Google Services
    '74.125.0.0/16',    # Google Services
    '108.177.0.0/17',   # Google Services
    '142.250.0.0/15',   # Google Services
    '172.217.0.0/16',   # Google Services
    '173.194.0.0/16',   # Google Services
    '209.85.128.0/17',  # Google Services
    '216.58.192.0/19',  # Google Services
    '216.239.32.0/19'   # Google Services
]

def is_ip_in_range(ip, ip_range):
    """Check if an IP address is within a CIDR range."""
    from ipaddress import ip_network, ip_address
    try:
        return ip_address(ip) in ip_network(ip_range)
    except ValueError:
        return False

def is_google_ip(ip):
    """Check if an IP address belongs to Google."""
    try:
        for ip_range in GOOGLE_IP_RANGES:
            if is_ip_in_range(ip, ip_range):
                return True
        return False
    except Exception:
        return False

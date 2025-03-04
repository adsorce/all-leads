import os
import psycopg2
import socket
from urllib.parse import urlparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Parse the URL to get the hostname
parsed_url = urlparse(DATABASE_URL)
hostname = parsed_url.hostname

# Print DNS resolution information
print(f"Trying to resolve hostname: {hostname}")

# Try to get both IPv4 and IPv6 addresses
try:
    # Get IPv4 address
    ipv4_address = socket.getaddrinfo(hostname, None, socket.AF_INET)[0][4][0]
    print(f"IPv4 address: {ipv4_address}")
except socket.gaierror:
    print("Could not resolve hostname to IPv4 address")
    ipv4_address = None

try:
    # Get IPv6 address
    ipv6_address = socket.getaddrinfo(hostname, None, socket.AF_INET6)[0][4][0]
    print(f"IPv6 address: {ipv6_address}")
except socket.gaierror:
    print("Could not resolve hostname to IPv6 address")
    ipv6_address = None

# Function to test the connection
def test_db_connection():
    success = False
    conn = None
    
    try:
        # Try connecting with the original URL first
        print("\nAttempting connection with original URL...")
        conn = psycopg2.connect(DATABASE_URL)
        success = True
    except Exception as original_error:
        print(f"❌ Original connection failed: {original_error}")
        
        # Try IPv6 if available
        if ipv6_address and not success:
            try:
                # Add brackets around IPv6 address
                print("\nAttempting connection with IPv6 address...")
                bracketed_ipv6 = f"[{ipv6_address}]"
                ipv6_url = DATABASE_URL.replace(hostname, bracketed_ipv6)
                conn = psycopg2.connect(ipv6_url)
                success = True
                print(f"✅ Connection successful using IPv6 address: {bracketed_ipv6}")
                print(f"Consider updating your .env file with this connection string:")
                print(f"DATABASE_URL={ipv6_url}")
            except Exception as ipv6_error:
                print(f"❌ IPv6 connection failed: {ipv6_error}")
        
        # If we have an IPv4 address, try using that instead
        if ipv4_address and not success:
            try:
                print("\nAttempting connection with IPv4 address...")
                # Replace the hostname with the IPv4 address in the connection string
                ipv4_url = DATABASE_URL.replace(hostname, ipv4_address)
                conn = psycopg2.connect(ipv4_url)
                success = True
                print(f"✅ Connection successful using IPv4 address: {ipv4_address}")
                print(f"Consider updating your .env file with this connection string:")
                print(f"DATABASE_URL={ipv4_url}")
            except Exception as ipv4_error:
                print(f"❌ IPv4 connection failed: {ipv4_error}")
    
    if success and conn:
        try:
            cur = conn.cursor()
            # Run a test query
            cur.execute("SELECT 1;")
            result = cur.fetchone()

            # Check if query ran successfully
            if result and result[0] == 1:
                print("✅ Successfully connected to the Supabase database!")
            else:
                print("⚠ Database connection test failed.")

            # Close connections
            cur.close()
            conn.close()
        except Exception as query_error:
            print(f"❌ Query execution failed: {query_error}")

# Run the test
if __name__ == "__main__":
    test_db_connection()
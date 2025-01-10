from netmiko import ConnectHandler
import os
from datetime import datetime

# Device details - Add more devices as needed
devices = [
    {
        'device_type': 'cisco_ios',
        'host': '10.20.1.1',  # Replace with your device IP
        'username': 'admin',     # Replace with device username
        'password': 'adminpassword',  # Replace with device password
        'secret': 'adminpassword',      # Optional, if your device uses enable mode
    }
    # You can add more device dictionaries here.
]

# Directory to store backups
BACKUP_DIR = "backups"
os.makedirs(BACKUP_DIR, exist_ok=True)


def backup_device_config(device):
    """Backs up the running configuration of a device."""
    try:
        # Connect to the device
        connection = ConnectHandler(**device)
        connection.enable()  # Enter enable mode if required

        # Get the running configuration
        config = connection.send_command("show running-config")

        # Create a filename based on the device IP and timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{BACKUP_DIR}/{device['host']}_backup_{timestamp}.txt"

        # Save the configuration to a file
        with open(filename, "w") as backup_file:
            backup_file.write(config)

        print(f"Backup complete for {device['host']}, saved as {filename}")

        # Disconnect from the device
        connection.disconnect()

    except Exception as e:
        print(f"Failed to backup {device['host']}: {e}")


def push_device_config(device, config_commands):
    """Pushes a list of configuration commands to a device."""
    try:
        # Connect to the device
        connection = ConnectHandler(**device)
        connection.enable()

        # Send the configuration commands
        output = connection.send_config_set(config_commands)
        print(f"Configuration applied to {device['host']}:")
        print(output)

        # Disconnect from the device
        connection.disconnect()

    except Exception as e:
        print(f"Failed to configure {device['host']}: {e}")


def monitor_device(device):
    """Monitors the device's CPU and memory usage."""
    try:
        # Connect to the device
        connection = ConnectHandler(**device)
        connection.enable()

        # Get CPU and memory usage
        cpu_usage = connection.send_command("show processes cpu")
        memory_usage = connection.send_command("show processes memory")

        # Print the status
        print(f"Monitoring {device['host']}:")
        print(f"CPU Usage:\n{cpu_usage}")
        print(f"Memory Usage:\n{memory_usage}")

        # Disconnect from the device
        connection.disconnect()

    except Exception as e:
        print(f"Failed to monitor {device['host']}: {e}")


# Example configuration commands (can be customized)
config_commands = [
    "hostname GNS3Router",
    "interface FastEthernet0/0",
    "description Configured via Netmiko",
    "ip address 10.20.1.1 255.255.255.0",
    "no shutdown",
    "line vty 0 4",
    "login local",
    "transport input ssh",
]

# Main execution
if __name__ == "__main__":
    for device in devices:
        # Backup configuration
        backup_device_config(device)

        # Push configuration updates
        push_device_config(device, config_commands)

        # Monitor device status
        monitor_device(device)

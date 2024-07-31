import csv
import re
import configparser

def sanitize_name(name):
    """Sanitize the metric name to be a valid Terraform resource name."""
    # Replace invalid characters with underscores
    name = re.sub(r'[^a-zA-Z0-9_-]', '_', name)
    # Ensure the name starts with a letter or underscore
    if not re.match(r'^[a-zA-Z_]', name):
        name = '_' + name
    return name

def read_csv(filename):
    """Read CSV file and return a list of metric names."""
    metric_names = []
    with open(filename, mode='r', encoding='utf-8-sig') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            for key in row:
                normalized_key = key.lstrip('\ufeff').lower()
                if normalized_key in ['metric name', 'metric_name']:
                    metric_names.append(row[key])
                    break
    return metric_names

def read_config(config_file):
    """Read configuration parameters from the config file."""
    config = configparser.ConfigParser()
    config.read(config_file)
    auth_token = config.get('Settings', 'auth_token')
    realm = config.get('Settings', 'realm')
    destination = config.get('Settings', 'destination')
    
    if destination not in ["Drop", "RealTime", "Archived"]:
        raise ValueError("Invalid destination value. Must be 'Drop', 'RealTime', or 'Archived'.")
    
    return auth_token, realm, destination

def generate_terraform_config(auth_token, realm, metric_names, destination):
    """Generate Terraform configurations for the given metric names."""
    provider_config = f"""
terraform {{
  required_providers {{
    signalfx = {{
      source  = "splunk-terraform/signalfx"
      version = ">= 9.1.5"
    }}
  }}
}}

provider "signalfx" {{
  auth_token = "{auth_token}"
  api_url    = "https://api.{realm}.signalfx.com"
}}
"""
    resource_config = ""
    for metric in metric_names:
        sanitized_name = sanitize_name(metric)
        resource_config += f"""
resource "signalfx_metric_ruleset" "{sanitized_name}" {{
  metric_name = "{metric}"

  routing_rule {{
    destination = "{destination}"
  }}
}}
"""
    return provider_config + resource_config

def write_terraform_config(filename, config):
    """Write the Terraform configuration to a file."""
    with open(filename, mode='w') as file:
        file.write(config)

def main():
    input_filename = input("Enter the CSV filename: ")
    config_file = 'config.conf'

    try:
        auth_token, realm, destination = read_config(config_file)
    except Exception as e:
        print(f"Error reading config file: {e}")
        return

    metric_names = read_csv(input_filename)
    if not metric_names:
        print("No metric names found in the CSV file.")
        return

    terraform_config = generate_terraform_config(auth_token, realm, metric_names, destination)
    output_filename = "metric_ruleset.tf"
    write_terraform_config(output_filename, terraform_config)
    print(f"Terraform configuration written to {output_filename}")

if __name__ == "__main__":
    main()

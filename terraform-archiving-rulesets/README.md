# Terraform [Splunk Observability] Metric Ruleset Generator
## v1.0

💡 **Note:** Routing to the Archived tier is not supported yet in version 9.1.6 of the SignalFx Terraform provider, but it will be available soon. This script will work with the upcoming release. Other routing options like Drop and RealTime work as expected.


## Overview

This script generates a Terraform configuration file for creating SignalFx metric rulesets in order to route metrics to the desired destination (real-time tier, archiving tier or drop). 

*Metric names* are read from a CSV file, User is asked to enter name of the file (i.e. myfile.csv) 
*Configuration* parameters are taken from a `config.conf` file.
*Output* file `metric_ruleset.tf` contains resources (rulesets) for all metrics and required provider config.

This tf file is ready for working with Terraform:
`terraform init`
`terraform plan`
and then `terraform apply/destroy` as required.


## Prerequisites

- Python 3.x
- Required Python libraries (e.g., `configparser`)

### Dependencies

The script uses the following Python libraries:

- `csv` (built-in, no installation required)
- `re` (built-in, no installation required)
- `configparser` (included in Python 3.x standard library)

Ensure you have Python 3.x installed, which includes `csv`, `re`, and `configparser` as part of the standard library. No additional installation is required for these libraries.

If you still need to install them manually - run `pip install configparser`


## How to Run the Script

1. **Create `config.conf`**: Define your SignalFx `auth_token`, `realm`, and `destination` values in a `config.conf` file. The `destination` can be one of `"Drop"`, `"RealTime"`, or `"Archived"`.

   Example `config.conf`:
   ```ini
   [Settings]
   auth_token = your_auth_token_here
   realm = your_realm_here
   destination = Drop

2. **Prepare CSV File**: Ensure your CSV file contains a column named either Metric Name or metric_name with the metric names you wish to include in the Terraform configuration.

   Example `CSV File`:

    ```csv
    Metric Name,Custom MTS,Charts,Detectors
    container_cpu_utilization_aggregate,6,,
    queueSize,14,,
    ri.normalized_cost,32,,
    te.bgp.metrics.path.changes,94,,
    te.bgp.metrics.reachability,94,,
    te.bgp.metrics.updates,94,,
    ```

3. **Run the Script**: Execute the script and provide the CSV filename when prompted.

    `python generate_terraform.py`


4. **Output**: The script will generate a metric_ruleset.tf file with the appropriate Terraform configuration.

    Example Output (`metric_ruleset.tf`):
    ```tf
    terraform {
    required_providers {
        signalfx = {
        source  = "splunk-terraform/signalfx"
        version = ">= 9.1.5"
        }
    }
    }

    provider "signalfx" {
    auth_token = "your_auth_token_here"
    api_url    = "https://api.your_realm_here.signalfx.com"
    }

    resource "signalfx_metric_ruleset" "container_cpu_utilization_aggregate" {
    metric_name = "container_cpu_utilization_aggregate"

    routing_rule {
        destination = "Drop"
    }
    }

    resource "signalfx_metric_ruleset" "queueSize" {
    metric_name = "queueSize"

    routing_rule {
        destination = "Drop"
    }
    }

    # Additional resources for other metrics...
    ```
**Notes**

Ensure that the `config.conf` file is in the same directory as the script.
Verify the `destination` value in `config.conf` is one of the allowed values: `"Drop"`, `"RealTime"`, or `"Archived"`.

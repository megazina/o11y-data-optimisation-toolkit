
terraform {
  required_providers {
    signalfx = {
      source  = "splunk-terraform/signalfx"
      version = ">= 9.1.5"
    }
  }
}

provider "signalfx" {
  auth_token = "test"
  api_url    = "https://api.us1.signalfx.com"
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

resource "signalfx_metric_ruleset" "ri_normalized_cost" {
  metric_name = "ri.normalized_cost"

  routing_rule {
    destination = "Drop"
  }
}

resource "signalfx_metric_ruleset" "te_bgp_metrics_path_changes" {
  metric_name = "te.bgp.metrics.path.changes"

  routing_rule {
    destination = "Drop"
  }
}

resource "signalfx_metric_ruleset" "te_bgp_metrics_reachability" {
  metric_name = "te.bgp.metrics.reachability"

  routing_rule {
    destination = "Drop"
  }
}

resource "signalfx_metric_ruleset" "te_bgp_metrics_updates" {
  metric_name = "te.bgp.metrics.updates"

  routing_rule {
    destination = "Drop"
  }
}

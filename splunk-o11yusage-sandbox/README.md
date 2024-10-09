# Splunk Enterprise/Cloud App with Dashboards used to help with Splunk Observability Data Optimisation
## v1.5.0
This app will create an o11yusage index - this is what you should use to Upload reports into.

## Sourcetypes:
`o11yusage:metric:usage:report` -- use this for *SWAT Metrics Usage* report, and SWAT Dimensions Usage report if required

`o11yusage:per:dimension:dpm` - use this for *Datapoints per dimension* report, and Dimensions report (both from o11y UI/API) as required.

## Loookup (for Dashboard that shows Metric Ingest Breakdown by Tokens)

Dashboard uses a lookup for tokenId-tokenName mapping.
You can get by running this in your org (or Splunkers can get it in MON (just add the orgId))

### Steps
  1. Plot this on this chart (or use any sf.org metric that you know that has both tokenId and TokenName).
  
  `A = data('sf.org.*ByToken', filter=filter('orgId', '*'), rollup='sum').sum(by=['tokenName', 'tokenId']).publish(label='A')`
  
  2. Download the csv from Data table of the above chart.

## Important
When uploading the files, make sure you put the ReportName-Date into the HOST field.

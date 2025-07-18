Azure Web Application Firewall on Azure Front Door provides extensive logging and telemetry to help you understand how your web application
firewall (WAF) is performing and the actions it takes.

The Azure Front Door WAF log is integrated with Azure Monitor. Azure Monitor enables you to track diagnostic information, including WAF
alerts and logs. You can configure WAF monitoring within the Azure Front Door resource in the Azure portal under the **Diagnostics** tab, through
infrastructure as code approaches, or by using Azure Monitor directly.

### **Metrics**

Azure Front Door automatically records metrics to help you understand the behavior of your WAF.

To access your WAF's metrics:

1. Sign in to the Azure portal and go to your Azure Front Door profile.
2. On the leftmost pane under **Monitoring**, select the **Metrics** tab.
3. Add the **Web Application Firewall Request Count** metric to track the number of requests that match WAF rules.

You can create custom filters based on action types and rule names. Metrics include requests with terminating actions like Block and Allow as
well as requests where the WAF took no action. Since multiple non-terminating Log actions can be triggered by a single request, they are excluded
from this metric to avoid duplicating request counts.

### **JavaScript challenge (preview) metrics**

To access your JavaScript challenge WAF metrics:

Add the Web Application Firewall JS Challenge Request Count metric to track the number of requests that match JavaScript
challenge WAF rules.

The following filters are provided as part of this metric:

**PolicyName**: This is the WAF policy name
**Rule**: This can be any custom rule or bot rule
**Action**: There are four possible values for JS Challenge action

**Issued**: JS Challenge is invoked the first time
**Passed**: JS Challenge computation succeeded and an answer was received
**Valid**: JS Challenge validity cookie was present
**Blocked**: JS Challenge computation failed

# **Azure Web Application Firewall monitoring and logging**

7/7/25, 8:44 AM
Azure Web Application Firewall monitoring and logging

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fweb-application-firewall%2Fafds%2Fwaf-front-door-monitor…
1/4

![Image](images/image_page1_0.png)

![Image](images/image_page1_1.png)

---
*Page 2*

### **Logs and diagnostics**

The Azure Front Door WAF provides detailed reporting on each request and each threat that it detects. Logging is integrated with Azure's
diagnostics logs and alerts by using Azure Monitor logs.

Logs aren't enabled by default. You must explicitly enable logs. You can configure logs in the Azure portal by using the **Diagnostic settings** tab.

If logging is enabled and a WAF rule is triggered, any matching patterns are logged in plain text to help you analyze and debug the WAF policy
behavior. You can use exclusions to fine-tune rules and exclude any data that you want to be excluded from the logs. For more information, see
Web application firewall exclusion lists in Azure Front Door.

You can enable three types of Azure Front Door logs:

WAF logs
Access logs
Health probe logs

Activity logs are enabled by default and provide visibility into the operations performed on your Azure resources, such as configuration changes
to your Azure Front Door profile.

7/7/25, 8:44 AM
Azure Web Application Firewall monitoring and logging

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fweb-application-firewall%2Fafds%2Fwaf-front-door-monitor…
2/4

![Image](images/image_page2_0.png)

---
*Page 3*

**WAF logs**

The log FrontDoorWebApplicationFirewallLog includes requests that match a WAF rule.

The log FrontdoorWebApplicationFirewallLog includes any request that matches a WAF rule.

The following table shows the values logged for each request.

**Property**
**Description**

Action
Action taken on the request. Logs include requests with all actions. Actions are:

Allow and allow: The request was allowed to continue processing.

Block and block: The request matched a WAF rule configured to block the request. Alternatively, the anomaly scoring
threshold was reached and the request was blocked.

Log and log: The request matched a WAF rule configured to use the Log action.

AnomalyScoring and logandscore: The request matched a WAF rule. The rule contributes to the anomaly score. The
request might or might not be blocked depending on other rules that run on the same request.

JS Challenge and JSChallengeIssued: Issued due to missing/invalid challenge clearance, missing answer.

The log is created when a client requests access to a web application for the first time and has not been challenged
previously. This client receives the JS challenge page and proceeds to compute the JS challenge. Upon successful
computation, the client is granted the validity cookie.

JS Challenge and JSChallengePass: Passed due to valid challenge answer.

This log is created when a client solves the JS challenge and resubmits the request with the correct answer. In this
case, Azure WAF validates the cookie and proceeds to process the remaining rules without generating another JS
challenge.

JS Challenge and JSChallengeValid: Logged/passthrough due to valid challenge.

This log is created when a client has previously solved a challenge. In this case, Azure WAF logs the request and
proceeds to process the remaining rules.

JS Challenge and JSChallengeBlock: Blocked

This log is created when a JS challenge computation fails.

ClientIP
The IP address of the client that made the request. If there was an X-Forwarded-For header in the request, the client IP
address is taken from that header field instead.

ClientPort
The IP port of the client that made the request.

Details
More details on the request, including any threats that were detected.

matchVariableName: HTTP parameter name of the request matched, for example, header names (up to 100 characters
maximum).

matchVariableValue: Values that triggered the match (up to 100 characters maximum).

Host
The Host header of the request.

Policy
The name of the WAF policy that processed the request.

PolicyMode
Operations mode of the WAF policy. Possible values are Prevention and Detection.

RequestUri
Full URI of the request.

RuleName
The name of the WAF rule that the request matched.

SocketIP
The source IP address seen by WAF. This IP address is based on the TCP session and doesn't consider any request
headers.

TrackingReference
The unique reference string that identifies a request served by Azure Front Door. This value is sent to the client in the X-

Azure-Ref response header. Use this field when you search for a specific request in the log.

The following example query shows the requests that the Azure Front Door WAF blocked:
Kusto
AzureDiagnostics
| where ResourceProvider == "MICROSOFT.CDN" and Category == "FrontDoorWebApplicationFirewallLog"

7/7/25, 8:44 AM
Azure Web Application Firewall monitoring and logging

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fweb-application-firewall%2Fafds%2Fwaf-front-door-monitor…
3/4

| Property
Action | Description
Action taken on the request. Logs include requests with all actions. Actions are:
Allow and allow: The request was allowed to continue processing.
Block and block: The request matched a WAF rule configured to block the request. Alternatively, the anomaly scoring
threshold was reached and the request was blocked.
Log and log: The request matched a WAF rule configured to use the Log action.
AnomalyScoring and logandscore: The request matched a WAF rule. The rule contributes to the anomaly score. The
request might or might not be blocked depending on other rules that run on the same request.
JS Challenge and JSChallengeIssued: Issued due to missing/invalid challenge clearance, missing answer.
The log is created when a client requests access to a web application for the first time and has not been challenged
previously. This client receives the JS challenge page and proceeds to compute the JS challenge. Upon successful
computation, the client is granted the validity cookie.
JS Challenge and JSChallengePass: Passed due to valid challenge answer.
This log is created when a client solves the JS challenge and resubmits the request with the correct answer. In this
case, Azure WAF validates the cookie and proceeds to process the remaining rules without generating another JS
challenge.
JS Challenge and JSChallengeValid: Logged/passthrough due to valid challenge.
This log is created when a client has previously solved a challenge. In this case, Azure WAF logs the request and
proceeds to process the remaining rules.
JS Challenge and JSChallengeBlock: Blocked
This log is created when a JS challenge computation fails. |
| --- | --- |
| ClientIP | The IP address of the client that made the request. If there was an X-Forwarded-For header in the request, the client IP
address is taken from that header field instead. |
| ClientPort | The IP port of the client that made the request. |
| Details | More details on the request, including any threats that were detected.
matchVariableName: HTTP parameter name of the request matched, for example, header names (up to 100 characters
maximum).
matchVariableValue: Values that triggered the match (up to 100 characters maximum). |
| Host | The Host header of the request. |
| Policy | The name of the WAF policy that processed the request. |
| PolicyMode | Operations mode of the WAF policy. Possible values are Prevention and Detection. |
| RequestUri | Full URI of the request. |
| RuleName | The name of the WAF rule that the request matched. |
| SocketIP | The source IP address seen by WAF. This IP address is based on the TCP session and doesn't consider any request
headers. |
| TrackingReference | The unique reference string that identifies a request served by Azure Front Door. This value is sent to the client in the X-
Azure-Ref response header. Use this field when you search for a specific request in the log. |

---
*Page 4*

| where action_s == "Block"
Kusto
AzureDiagnostics
| where ResourceType == "FRONTDOORS" and Category == "FrontdoorWebApplicationFirewallLog"
| where action_s == "Block"

The following snippet shows an example log entry, including the reason that the request was blocked:
JSON
{
  "time": "2020-06-09T22:32:17.8376810Z",
  "category": "FrontdoorWebApplicationFirewallLog",
  "operationName": "Microsoft.Cdn/Profiles/Write",
  "properties": {
    "clientIP": "xxx.xxx.xxx.xxx",
    "clientPort": "52097",
    "socketIP": "xxx.xxx.xxx.xxx",
    "requestUri": "https://wafdemofrontdoorwebapp.azurefd.net:443/?q=%27%20or%201=1",
    "ruleName": "Microsoft_DefaultRuleSet-1.1-SQLI-942100",
    "policy": "WafDemoCustomPolicy",
    "action": "Block",
    "host": "wafdemofrontdoorwebapp.azurefd.net",
    "trackingReference": "08Q3gXgAAAAAe0s71BET/QYwmqtpHO7uAU0pDRURHRTA1MDgANjMxNTAwZDAtOTRiNS00YzIwLTljY2YtNjFhNzMyOWQyYTgy",
    "policyMode": "prevention",
    "details": {
      "matches": [
        {
          "matchVariableName": "QueryParamValue:q",
          "matchVariableValue": "' or 1=1"
        }
      ]
    }
  }
}
JSON
{
  "time": "2020-06-09T22:32:17.8376810Z",
  "category": "FrontdoorWebApplicationFirewallLog",
  "operationName": "Microsoft.Network/FrontDoorWebApplicationFirewallLog/Write",
  "properties": {
    "clientIP": "xxx.xxx.xxx.xxx",
    "clientPort": "52097",
    "socketIP": "xxx.xxx.xxx.xxx",
    "requestUri": "https://wafdemofrontdoorwebapp.azurefd.net:443/?q=%27%20or%201=1",
    "ruleName": "Microsoft_DefaultRuleSet-1.1-SQLI-942100",
    "policy": "WafDemoCustomPolicy",
    "action": "Block",
    "host": "wafdemofrontdoorwebapp.azurefd.net",
    "trackingReference": "08Q3gXgAAAAAe0s71BET/QYwmqtpHO7uAU0pDRURHRTA1MDgANjMxNTAwZDAtOTRiNS00YzIwLTljY2YtNjFhNzMyOWQyYTgy",
    "policyMode": "prevention",
    "details": {
      "matches": [
        {
          "matchVariableName": "QueryParamValue:q",
          "matchVariableValue": "' or 1=1"
        }
      ]
    }
  }
}

For more information about the other Azure Front Door logs, see Monitor metrics and logs in Azure Front Door.

### **Next step**

Learn more about Azure Front Door.

7/7/25, 8:44 AM
Azure Web Application Firewall monitoring and logging

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fweb-application-firewall%2Fafds%2Fwaf-front-door-monitor…
4/4
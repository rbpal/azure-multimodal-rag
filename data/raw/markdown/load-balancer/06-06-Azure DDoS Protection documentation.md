# **What is Azure DDoS Protection?**

Distributed denial of service (DDoS) attacks are some of the largest availability and security concerns
facing customers that are moving their applications to the cloud. A DDoS attack attempts to exhaust an
application's resources, making the application unavailable to legitimate users. DDoS attacks can be
targeted at any endpoint that is publicly reachable through the internet.

Azure DDoS Protection, combined with application design best practices, provides enhanced DDoS
mitigation features to defend against DDoS attacks. It's automatically tuned to help protect your
specific Azure resources in a virtual network. Protection is simple to enable on any new or existing
virtual network, and it requires no application or resource changes.

Azure DDoS Protection protects at layer 3 and layer 4 network layers. For web applications protection
at layer 7, you need to add protection at the application layer using a WAF offering. For more
information, see Application DDoS protection.

Note

Azure DDoS Protections is one of the services that make up the Network Security category in Azure.
Other services in this category include Azure Firewall and Azure Web Application Firewall. Each
service has its own unique features and use cases. For more information on this service category, see
Network Security.

# **Tiers**

## **DDoS Network Protection**

# **Azure DDoS Protection documentation**

7/7/25, 8:29 AM
Azure DDoS Protection documentation

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fddos-protection%2Fddos-protection-overview
1/4

![Image](images/image_page1_0.png)

---
*Page 2*

Azure DDoS Network Protection, combined with application design best practices, provides enhanced
DDoS mitigation features to defend against DDoS attacks. It's automatically tuned to help protect your
specific Azure resources in a virtual network. For more information about enabling DDoS Network
Protection, see Quickstart: Create and configure Azure DDoS Network Protection using the Azure
portal.

## **DDoS IP Protection**

DDoS IP Protection is a pay-per-protected IP model. DDoS IP Protection contains the same core
engineering features as DDoS Network Protection, but will differ in the following value-added
services: DDoS rapid response support, cost protection, and discounts on WAF. For more information
about enabling DDoS IP Protection, see Quickstart: Create and configure Azure DDoS IP Protection
using Azure PowerShell.

For more information about the tiers, see DDoS Protection tier comparison.

# **Key Features**

**Always-on traffic monitoring:** Your application traffic patterns are monitored 24 hours a
day, 7 days a week, looking for indicators of DDoS attacks. Azure DDoS Protection
instantly and automatically mitigates the attack, once it's detected.

**Adaptive real time tuning:** Intelligent traffic profiling learns your application's traffic over
time, and selects and updates the profile that is the most suitable for your service. The
profile adjusts as traffic changes over time.

**DDoS Protection analytics, metrics, and alerting:** Azure DDoS Protection applies three
auto-tuned mitigation policies (TCP SYN, TCP, and UDP) for each public IP of the
protected resource, in the virtual network that has DDoS enabled. The policy thresholds are
auto-configured via machine learning-based network traffic profiling. DDoS mitigation
occurs for an IP address under attack only when the policy threshold is exceeded.

**Attack analytics:** Get detailed reports in five-minute increments during an
attack, and a complete summary after the attack ends. Stream mitigation flow
logs to Microsoft Sentinel or an offline security information and event
management (SIEM) system for near real-time monitoring during an attack. See
View and configure DDoS diagnostic logging to learn more.

**Attack metrics:** Summarized metrics from each attack are accessible through
Azure Monitor. See View and configure DDoS protection telemetry to learn
more.

**Attack alerting:** Alerts can be configured at the start and stop of an attack, and
over the attack's duration, using built-in attack metrics. Alerts integrate into your
operational software like Microsoft Azure Monitor logs, Splunk, Azure Storage,
Email, and the Azure portal. See View and configure DDoS protection alerts to
learn more.

**Azure DDoS Rapid Response:** During an active attack, Azure DDoS Network Protection
enabled customers have access to the DDoS Rapid Response (DRR) team, who can help

7/7/25, 8:29 AM
Azure DDoS Protection documentation

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fddos-protection%2Fddos-protection-overview
2/4

---
*Page 3*

with attack investigation during an attack and post-attack analysis. For more information,
see Azure DDoS Rapid Response.

**Native platform integration:** Natively integrated into Azure. Includes configuration
through the Azure portal. Azure DDoS Protection understands your resources and resource
configuration.

**Turnkey protection:** Simplified configuration immediately protects all resources on a
virtual network as soon as DDoS Network Protection is enabled. No intervention or user
definition is required. Similarly, simplified configuration immediately protects a public IP
resource when DDoS IP Protection is enabled for it.

**Multi-Layered protection:** When deployed with a web application firewall (WAF), Azure
DDoS Protection protects both at the network layer (Layer 3 and 4, offered by Azure DDoS
Protection) and at the application layer (Layer 7, offered by a WAF). WAF offerings include
Azure Application Gateway WAF SKU and third-party web application firewall offerings
available in the Azure Marketplace.

**Extensive mitigation scale:** All L3/L4 attack vectors can be mitigated, with global
capacity, to protect against the largest known DDoS attacks.

**Cost guarantee:** Receive data-transfer and application scale-out service credit for resource
costs incurred as a result of documented DDoS attacks.

# **Architecture**

Azure DDoS Protection is designed for services that are deployed in a virtual network. For other
services, the default infrastructure-level DDoS protection applies, which defends against common
network-layer attacks. To learn more about supported architectures, see DDoS Protection reference
architectures.

# **Pricing**

For DDoS Network Protection, under a tenant, a single DDoS protection plan can be used across
multiple subscriptions, so there's no need to create more than one DDoS protection plan. For DDoS IP
Protection, there's no need to create a DDoS protection plan. Customers can enable DDoS IP protection
on any public IP resource.

To learn about Azure DDoS Protection pricing, see Azure DDoS Protection pricing.

# **Best Practices**

Maximize the effectiveness of your DDoS protection and mitigation strategy by following these best
practices:

Design your applications and infrastructure with redundancy and resilience in mind.
Implement a multi-layered security approach, including network, application, and data
protection.
Prepare an incident response plan to ensure a coordinated response to DDoS attacks.

7/7/25, 8:29 AM
Azure DDoS Protection documentation

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fddos-protection%2Fddos-protection-overview
3/4

---
*Page 4*

To learn more about best practices, see Fundamental best practices.

# **FAQ**

For frequently asked questions, see the DDoS Protection FAQ.

# **Next steps**

7/7/25, 8:29 AM
Azure DDoS Protection documentation

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Fddos-protection%2Fddos-protection-overview
4/4
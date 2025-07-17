The term *load balancing* refers to the distribution of workloads across multiple computing resources.
Load balancing aims to optimize resource use, maximize throughput, minimize response time, and
avoid overloading any single resource. It can also improve availability by sharing a workload across
redundant computing resources.

Azure provides various load-balancing services that you can use to distribute your workloads across
multiple computing resources. These resources include Azure Application Gateway, Azure Front Door,
Azure Load Balancer, and Azure Traffic Manager.

This article describes some considerations to determine an appropriate load-balancing solution for your
workload's needs.

# **Service categorizations**

Azure load-balancing services can be categorized along two dimensions: global versus regional and
HTTP(S) versus non-HTTP(S).

## **Global vs. regional**

**Global:** These load-balancing services distribute traffic across regional back-ends, clouds,
or hybrid on-premises services. These services support managing a single control plane
responsible for globally routing end-user traffic to an available back-end. They often react
to changes in service reliability or performance to maximize availability and performance.
You can think of them as systems that load balance between application stamps, endpoints,
or scale-units hosted across different regions/geographies.
**Regional:** These load-balancing services distribute traffic within virtual networks across
virtual machines (VMs) or zonal and zone-redundant service endpoints within a region. You
can think of them as systems that load balance between VMs, containers, or clusters within
a region in a virtual network.

## **HTTP(S) vs. non-HTTP(S)**

**HTTP(S):** These load-balancing services are Layer 7 load balancers that only accept
HTTP(S) traffic. They're intended for web applications or other HTTP(S) endpoints. They
might have features such as SSL offload, web application firewall, path-based load
balancing, and session affinity.
**Non-HTTP(S):** These load-balancing services are either Layer 4 TCP or UDP services, or
DNS-based load balancing.

The following table summarizes the Azure load-balancing services.

**Service**
**Global/Regional**
**Recommended traffic**

Azure Front Door
Global
HTTP(S)

# **Load-balancing options**

7/7/25, 8:41 AM
Load-balancing options

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Farchitecture%2Fguide%2Ftechnology-choices%2Fload-balanci…
1/6

| Service
Azure Front Door | Global/Regional
Global | Recommended traffic
HTTP(S) |
| --- | --- | --- |

---
*Page 2*

**Service**
**Global/Regional**
**Recommended traffic**

Azure Traffic Manager
Global
Non-HTTP(S)

Azure Application Gateway
Regional
HTTP(S)

Azure Load Balancer
Regional or Global
Non-HTTP(S)

Note

Azure Traffic Manager and Azure Load Balancer have the capabilities to distribute any traffic,
including HTTP(S). However, these services do not have Layer 7 capabilities. Unlike Azure Load
Balancer, Azure Traffic Manager doesn't handle the traffic directly; Traffic Manager manipulates DNS
to direct clients to the appropriate endpoints.

# **Azure load-balancing services**

Here are the main load-balancing services currently available in Azure:

Azure Front Door is an application delivery network that provides global load balancing
and site acceleration service for web applications. It offers Layer 7 capabilities for your
application like SSL offload, path-based routing, fast failover, and caching to improve
performance and high availability of your applications.

Traffic Manager is a DNS-based traffic load balancer that enables you to distribute traffic
optimally to services across global Azure regions, while providing high availability and
responsiveness. Because Traffic Manager is a DNS-based load-balancing service, it load
balances only at the domain level. For that reason, it can't fail over as quickly as Azure
Front Door, because of common challenges around DNS caching and systems not honoring
DNS TTLs.

Application Gateway provides application delivery controller as a service, offering various
Layer 7 load-balancing capabilities and web application firewall functionality. Use it to
transition from public network space into your web servers hosted in private network space
within a region.

Load Balancer is a high-performance, ultra-low-latency Layer 4 load-balancing service
(inbound and outbound) for all UDP and TCP protocols. It's built to handle millions of
requests per second while ensuring your solution is highly available. Load Balancer is zone
redundant, ensuring high availability across availability zones. It supports both a regional
deployment topology and a cross-region topology.

Note

Clustering technology, such as Azure Container Apps or Azure Kubernetes Service contains load
balancing constructs that operate mostly within the scope of their own cluster boundary, routing traffic
to available application instances based on readiness and health probes. Those load balancing options
are not covered in this article.

7/7/25, 8:41 AM
Load-balancing options

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Farchitecture%2Fguide%2Ftechnology-choices%2Fload-balanci…
2/6

| Service | Global/Regional | Recommended traffic |
| --- | --- | --- |
| Azure Traffic Manager | Global | Non-HTTP(S) |
| Azure Application Gateway | Regional | HTTP(S) |
| Azure Load Balancer | Regional or Global | Non-HTTP(S) |

---
*Page 3*

# **Decision tree for load balancing in Azure**

Consider these factors such as these when you select a load balancing solution:

**Traffic type:** Is it a web HTTP(S) application? Is it public facing or a private application?
**Global vs. regional:** Do you need to load balance VMs or containers within a single virtual
network, or load balance scale unit/deployments across regions, or both?
**Availability:** What's the service-level agreement?
**Cost:** For more information, see Azure pricing. In addition to the cost of the service itself,
consider the operations cost for managing a solution built on that service.
**Features and limits:** What capabilities are supported on each service and what are the
Service limits of each service?

Tip

The Azure portal offers a questionnaire-based guide similar to the following flowchart. In the Azure
portal, search for '**Load balancing - help me choose**'. By answering the questions, you can narrow
down your load balancing options.

The following flowchart helps you to choose a load-balancing solution for your application. The
flowchart guides you through a set of key decision criteria to reach a recommendation.

Treat this flowchart as a starting point. Every application has unique requirements, so use the
recommendation as a starting point. Then perform a more detailed evaluation.

When your workload involves several services that require load balancing, it's important to assess each
service individually. In many cases, an effective setup uses more than one type of load-balancing
solution. You might incorporate these solutions at different places in your workload's architecture, each
serving a unique function or role.

7/7/25, 8:41 AM
Load-balancing options

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Farchitecture%2Fguide%2Ftechnology-choices%2Fload-balanci…
3/6

---
*Page 4*

## **Definitions**

**Web application (HTTP/HTTPS):** This refers to needing the capability to make a routing
decision for Layer 7 data such as URL path, support the inspection of the communication
payload (such as an HTTP request body), or handle TLS functionality.

**Internet facing application:** Applications that are publicly accessible from the internet. As
a best practice, application owners apply restrictive access policies or protect the application
by setting up offerings like web application firewall and DDoS protection.

**Global / Deployed in multiple regions:** If this load balancer should have a single, highly
available control plane that is responsible for routing traffic to public endpoints on your
globally distributed application. This can be to support either active-active or active-passive
topologies across regions.

7/7/25, 8:41 AM
Load-balancing options

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Farchitecture%2Fguide%2Ftechnology-choices%2Fload-balanci…
4/6

![Image](images/image_page4_0.png)

---
*Page 5*

Note

It is possible to use a regional service, such as Application Gateway, to load balance across
backends spanning multiple regions and control routing through a single control plane. That
architecture is made possible using cross-region Private Link, global virtual network
peering, or even public IPs of services in other regions.

This scenario isn't the primary point of this decision, however.

Using a regional resource as a router for globally distributed backends introduces a regional
single point of failure and incurs additional latency as traffic is forced through one region
before going to another and then back again.

**Platform as a service (PaaS):** Provides a managed hosting environment, where you can
deploy your application without needing to manage VMs or networking resources. In this
case, PaaS refers to services that provide integrated load balancing within a region. For
more information, see Choose a compute service – Scalability.

**Azure Kubernetes Service (AKS):** Enables you to deploy and manage containerized
applications. AKS provides serverless Kubernetes, an integrated continuous integration and
continuous delivery experience, and enterprise-grade security and governance. For more
information about AKS architectural resources, see Azure Kubernetes Service architecture
design.

**Infrastructure as a service (IaaS):** A computing option where you provision the virtual
machines that you need, along with associated network and storage components. IaaS
applications require internal load balancing within a virtual network by using Load
Balancer.

**Application-layer processing:** Refers to special routing within a virtual network. Examples
include path-based routing across VMs or virtual machine scale sets. For more information,
see When should I deploy an Application Gateway behind Azure Front Door?

**Performance acceleration:** Refers to features that accelerate web access. Performance
acceleration can be achieved by using content delivery networks (CDNs) or optimized point
of presence ingress for accelerated client onboarding into the destination network. Azure
Front Door supports both CDNs and Anycast traffic acceleration. The benefits of both
features can be gained with or without Application Gateway in the architecture.

## **Additional considerations**

Each load balancing service also has capability support or implementation details that need also be
considered. Here are some examples that might be relevant for your load balancing scenario.

WebSockets support
Server-sent events support
HTTP/2 support (both receiving and continuing to backend nodes)
Sticky session support
Backend node health monitoring mechanism
Client experience or delay between unhealthy node detection and removal from routing
logic.

7/7/25, 8:41 AM
Load-balancing options

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Farchitecture%2Fguide%2Ftechnology-choices%2Fload-balanci…
5/6

---
*Page 6*

# **Examples**

The following table lists various articles based on the load-balancing services used as a solution.

**Services**
**Article**
**Description**

Load Balancer
Load balance virtual
machines (VMs)
across availability
zones

Load balance VMs across availability zones to help
protect your apps and data from an unlikely failure or
loss of an entire datacenter. With zone redundancy, one
or more availability zones can fail and the data path
survives as long as one zone in the region remains
healthy.

Traffic
Manager

Multitier web
application built for
high availability and
disaster recovery

Deploy resilient multitier applications built for high
availability and disaster recovery. If the primary region
becomes unavailable, Traffic Manager fails over to the
secondary region.

Azure Front
Door +
Application
Gateway

Multitenant SaaS on
Azure

Use a multitenant solution that includes a combination
of Azure Front Door and Application Gateway. Azure
Front Door helps load balance traffic across regions.
Application Gateway routes and load-balances traffic
internally in the application to the various services that
satisfy client business needs.

Traffic
Manager +
Application
Gateway

Multiregion load
balancing with
Traffic Manager and
Application Gateway

Learn how to serve web workloads and deploy resilient
multitier applications in multiple Azure regions to
achieve high availability and a robust disaster recovery
infrastructure.

# **Next steps**

7/7/25, 8:41 AM
Load-balancing options

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Farchitecture%2Fguide%2Ftechnology-choices%2Fload-balanci…
6/6

| Services
Load Balancer | Article
Load balance virtual
machines (VMs)
across availability
zones | Description
Load balance VMs across availability zones to help
protect your apps and data from an unlikely failure or
loss of an entire datacenter. With zone redundancy, one
or more availability zones can fail and the data path
survives as long as one zone in the region remains
healthy. |
| --- | --- | --- |
| Traffic
Manager | Multitier web
application built for
high availability and
disaster recovery | Deploy resilient multitier applications built for high
availability and disaster recovery. If the primary region
becomes unavailable, Traffic Manager fails over to the
secondary region. |
| Azure Front
Door +
Application
Gateway | Multitenant SaaS on
Azure | Use a multitenant solution that includes a combination
of Azure Front Door and Application Gateway. Azure
Front Door helps load balance traffic across regions.
Application Gateway routes and load-balances traffic
internally in the application to the various services that
satisfy client business needs. |
| Traffic
Manager +
Application
Gateway | Multiregion load
balancing with
Traffic Manager and
Application Gateway | Learn how to serve web workloads and deploy resilient
multitier applications in multiple Azure regions to
achieve high availability and a robust disaster recovery
infrastructure. |
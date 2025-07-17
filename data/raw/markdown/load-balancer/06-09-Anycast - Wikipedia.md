### **Anycast**

Communication protocol

Visualization of anycast routing.

**Purpose**
To route traffic to the closest server.

**Developer(s)** Craig Partridge, Trevor Mendez, Walter

Milliken at BBN

**Introduction** 1989

**RFC(s)**
1546 (https://www.rfc-editor.org/rfc/rfc154
6), 2526 (https://www.rfc-editor.org/rfc/rfc
2526), 4291 (https://www.rfc-editor.org/rf
c/rfc4291), 4786 (https://www.rfc-editor.or

g/rfc/rfc4786)...

# **Anycast**

**Anycast** is a network addressing and routing
methodology in which a single IP address is
shared by devices (generally servers) in multiple
locations. Routers direct packets addressed to
this destination to the location nearest the
sender, using their normal decision-making
algorithms, typically the lowest number of BGP
network hops. Anycast routing is widely used by
content delivery networks such as web and
name servers, to bring their content closer to
end users.

The first documented use of anycast routing for
topological
load-balancing
of
Internet-
connected services was in 1989;[1][2] the
technique was first formally documented in the
IETF four years later.[3] It was first applied to
critical
infrastructure
in
2001
with
the
anycasting of the I-root nameserver.[2]

Early objections to the deployment of anycast routing centered on the perceived conflict between long-
lived TCP connections and the volatility of the Internet's routed topology. In concept, a long-lived
connection, such as an FTP file transfer (which can take hours to complete for large files) might be re-
routed to a different anycast instance in mid-connection due to changes in network topology or
routing, with the result that the server changes mid-connection, and the new server is not aware of the
connection and does not possess the TCP connection state of the previous anycast instance.

In practice, such problems were not observed, and these objections dissipated by the early 2000s.
Many initial anycast deployments consisted of DNS servers, using principally UDP transport.[4][2]

Measurements of long-term anycast flows revealed very few failures due to mid-connection instance
switches, far fewer (less than 0.017%[5] or "less than one flow per ten thousand per hour of
duration"[1] according to various sources) than were attributed to other causes of failure. Numerous
mechanisms were developed to efficiently share state between anycast instances.[6] And some TCP-

# **History**

### **Early objections**

7/7/25, 8:32 AM
Anycast - Wikipedia

https://en.wikipedia.org/wiki/Anycast
1/6

![Image](images/image_page1_0.png)

![Image](images/image_page1_1.png)

---
*Page 2*

based protocols, notably HTTP, incorporated "redirect" mechanisms, whereby anycast service
addresses could be used to locate the nearest instance of a service, whereupon a user would be
redirected to that specific instance prior to the initiation of any long-lived stateful transaction.[1][7]

Anycast can be implemented via Border Gateway Protocol (BGP). Multiple hosts (usually in different
geographic areas) are given the same unicast IP address and different routes to the address are
announced through BGP. Routers consider these to be alternative routes to the same destination, even
though they are actually routes to different destinations with the same address. As usual, routers
select a route by whatever distance metric is in use (the least cost, least congested, shortest). Selecting
a route in this setup amounts to selecting a destination.

Anycast is supported explicitly in the IPv6 addressing architecture.[8] The lowest address within an
IPv6 subnet (interface identifier 0) is reserved as the "Subnet Router" anycast address. In addition,
the highest 128 interface identifiers within a subnet are also reserved as anycast addresses.[9]

Reserved Anycast address's

**Subnet Prefix**
***interface identifier***
**CIDR notation**

**Subnet router**
any
::
::0/124

**Anycast**
any
ffff:ffff:ffff:ff80 to ffff:ffff:ffff:ffff
::ffff:ffff:ffff:ff80/121

**Mobility Support**
any
ffff:ffff:ffff:fffe
::ffff:ffff:ffff:fffe/124

Most IPv6 routers on the path of an anycast packet through the network will not distinguish it from a
unicast packet, but special handling is required from the routers near the destination (that is, within
the scope of the anycast address) as they are required to route an anycast packet to the "nearest"
interface within that scope which has the proper anycast address, according to whatever measure of
distance (hops, cost, etc.) is being used.

The method used in IPv4 of advertising multiple routes in BGP to multiply-assigned unicast addresses
also still works in IPv6, and can be used to route packets to the nearest of several geographically
dispersed hosts with the same address. This approach, which does not depend on anycast-aware
routers, has the same use cases together with the same problems and limitations as in IPv4.

With the growth of the Internet, network services increasingly have high-availability requirements. As
a result, operation of anycast services has grown in popularity among network operators.[10]

# **Internet Protocol version 4**

# **Internet Protocol version 6**

# **Applications**

7/7/25, 8:32 AM
Anycast - Wikipedia

https://en.wikipedia.org/wiki/Anycast
2/6

|  | Subnet Prefxi | interface identifeir | CIDR notation |
| --- | --- | --- | --- |
| Subnet router | any | :: | ::0/124 |
| Anycast | any | ffff:ffff:ffff:ff80 to ffff:ffff:ffff:ffff | ::ffff:ffff:ffff:ff80/121 |
| Mobility Support | any | ffff:ffff:ffff:fffe | ::ffff:ffff:ffff:fffe/124 |

---
*Page 3*

All Internet root nameservers are implemented as clusters of hosts using anycast addressing.[11] All 13
root servers A–M exist in multiple locations, with 11 on multiple continents. (Root servers B and H
exist in two U.S. locations.)[12][13][14] The servers use anycast address announcements to provide a
decentralized service. This has accelerated the deployment of physical (rather than logical) root
servers outside the United States. Many commercial DNS providers have switched to an IP anycast
environment to increase query performance and redundancy, and to implement load balancing.[2]

In IPv4 to IPv6 transitioning, anycast addressing may be deployed to provide IPv6 compatibility to
IPv4 hosts. This method, 6to4, uses a default gateway with the IP address *192.88.99.1*.[15] This allows
multiple providers to implement 6to4 gateways without hosts having to know each individual
provider's gateway addresses. 6to4 has been deprecated[16] in response to native IPv6 becoming more
prevalent.

Content delivery networks may use anycast for actual HTTP connections to their distribution centers,
or for DNS. Because most HTTP connections to such networks request static content such as images
and style sheets, they are generally short-lived and stateless across subsequent TCP sessions. The
general stability of routes and statelessness of connections makes anycast suitable for this application,
even though it uses TCP.[5][1]

Anycast rendezvous point can be used in Multicast Source Discovery Protocol (MSDP) and its
advantageous application as Anycast RP is an intra-domain feature that provides redundancy and
load-sharing capabilities. If the multiple anycast rendezvous point is used, IP routing automatically
will select the topologically closest rendezvous point for each source and receiver. It would provide a
multicast network with the fault tolerance requirements.[17]

Anycast allows any operator whose routing information is accepted by an intermediate router to hijack
any packets intended for the anycast address. While this at first sight appears insecure, it is no
different from the routing of ordinary IP packets, and no more or less secure. As with conventional IP
routing, careful filtering of who is and is not allowed to propagate route announcements is crucial to
prevent man-in-the-middle or blackhole attacks. The former can also be prevented by encrypting and
authenticating messages, such as using Transport Layer Security, while the latter can be frustrated by
onion routing.

### **Domain Name System**

### **IPv6 transition**

### **Content delivery networks**

### **Connectivity between Anycast and Multicast network**

# **Security**

7/7/25, 8:32 AM
Anycast - Wikipedia

https://en.wikipedia.org/wiki/Anycast
3/6

---
*Page 4*

***Internet portal***

Anycast is normally highly reliable, as it can provide automatic failover without adding complexity or
new potential points of failure. Anycast applications typically feature external "heartbeat" monitoring
of the server's function, and withdraw the route announcement if the server fails. In some cases this is
done by the actual servers announcing the anycast prefix to the router over OSPF or another IGP. If
the servers die, the router will automatically withdraw the announcement. "Heartbeat" functionality is
important because, if the announcement continues for a failed server, the server will act as a "black
hole" for nearby clients; this is the most serious mode of failure for an anycast system. Even in this
event, this kind of failure will only cause a total failure for clients that are closer to this server than any
other, and will not cause a global failure. However, even the automation necessary to implement
"heartbeat" routing withdrawal can itself add a potential point of failure, as seen in the 2021 Facebook
outage.

In denial-of-service attacks, a rogue network host may advertise itself as an anycast server for a vital
network service, to provide false information or simply block service.

Anycast methodologies on the Internet may be exploited to distribute DDoS attacks and reduce their
effectiveness: As traffic is routed to the closest node, a process over which the attacker has no control,
the DDoS traffic flow will be distributed amongst the closest nodes. Thus, not all nodes might be
affected. This may be a reason to deploy anycast addressing.[18] The effectiveness of this technique
depends upon maintaining the secrecy of any unicast addresses associated with anycast service nodes,
however, since an attacker in possession of the unicast addresses of individual nodes can attack them
from any location, bypassing anycast addressing methods.[19]

Some anycast deployments on the Internet distinguish between local and global nodes to benefit the
local community, by addressing local nodes preferentially. An example is the Domain Name System.
Local nodes are often announced with the no-export BGP community to prevent hosts from
announcing them to their peers, i.e. the announcement is kept in the local area. Where both local and
global nodes are deployed, the announcements from global nodes are often AS prepended (i.e. the AS
is added a few more times) to make the path longer so that a local node announcement is preferred
over a global node announcement.[20]

Multihoming
Line hunting, for an equivalent system for telephones

# **Reliability**

# **Mitigation of denial-of-service attacks**

# **Local and global nodes**

# **See also**

7/7/25, 8:32 AM
Anycast - Wikipedia

https://en.wikipedia.org/wiki/Anycast
4/6

![Image](images/image_page4_0.png)

---
*Page 5*

1. Woodcock, Bill (June 1996). "Best Practices in Anycast Routing" (https://www.pch.net/resources/T

utorials/anycast/Anycast-v06.pdf) (PDF). Packet Clearing House.
2. Hernandez, Gael (October 10, 2017). "Building and Operating a Global Anycast Network" (https://

www.enog.org/wp-content/uploads/presentations/enog-14/20-Anycast-DNS-network-ENOG14.pdf)
(PDF). Eurasia Network Operators Group.
3. C. Partridge; T. Mendez; W. Milliken (November 1993). *Host Anycasting Service* (https://datatracke

r.ietf.org/doc/html/rfc1546). Network Working Group. doi:10.17487/RFC1546 (https://doi.org/10.17
487%2FRFC1546). RFC 1546 (https://datatracker.ietf.org/doc/html/rfc1546). *Informational.*
4. Woodcock, Bill (November 14, 2019). "TCP and Anycast" (https://www.mail-archive.com/nanog@n

anog.org/msg103547.html). *NANOG mailing list archive*. North American Network Operators
Group.
5. Levine, Matt; Lyon, Barrett; Underwood, Todd (June 2006). "TCP Anycast: Don't Believe the FUD -

Operational experience with TCP and Anycast" (https://archive.nanog.org/meetings/nanog37/pres
entations/matt.levine.pdf) (PDF). North American Network Operators Group.
6. Herrin, William. "Anycast TCP Architecture" (https://bill.herrin.us/network/anycasttcp.html).

Retrieved October 11, 2021.
7. Katz-Bassett, Ethan; Gao, Ryan (July 2019). "Impact of TCP Loss on Regional Application

Performance" (https://www.microsoft.com/en-us/research/uploads/prod/2019/07/regionalloss.pdf)
(PDF). Microsoft. "Azure Frontdoor uses anycast redirection to direct users to a nearby edge."
8. R. Hinden; S. Deering (February 2006). *IP Version 6 Addressing Architecture* (https://datatracker.ie

tf.org/doc/html/rfc4291). Network Working Group. doi:10.17487/RFC4291 (https://doi.org/10.1748
7%2FRFC4291). RFC 4291 (https://datatracker.ietf.org/doc/html/rfc4291). *Draft Standard.*
Obsoletes RFC 3513 (https://www.rfc-editor.org/rfc/rfc3513). Updated by RFC 5952 (https://www.rf
c-editor.org/rfc/rfc5952), 6052 (https://www.rfc-editor.org/rfc/rfc6052), 7136 (https://www.rfc-editor.
org/rfc/rfc7136), 7346 (https://www.rfc-editor.org/rfc/rfc7346), 7371 (https://www.rfc-editor.org/rfc/rf
c7371) and 8064 (https://www.rfc-editor.org/rfc/rfc8064).
9. D. Johnson; S. Deering (March 1999). *Reserved IPv6 Subnet Anycast Addresses* (https://datatrac

ker.ietf.org/doc/html/rfc2526). Network Working Group. doi:10.17487/RFC2526 (https://doi.org/10.
17487%2FRFC2526). RFC 2526 (https://datatracker.ietf.org/doc/html/rfc2526). *Proposed*
*Standard.*
10. J. Abley; K. Lindqvist (December 2006). *Operation of Anycast Services* (https://datatracker.ietf.org/

doc/html/rfc4786). IETF Network Working Group. doi:10.17487/RFC4786 (https://doi.org/10.1748
7%2FRFC4786). BCP 126. RFC 4786 (https://datatracker.ietf.org/doc/html/rfc4786). *Best Current*
*Practice 126.*
11. T. Hardie (April 2002). *Distributing Authoritative Name Servers via Shared Unicast Addresses* (http

s://datatracker.ietf.org/doc/html/rfc3258). Network Working Group. doi:10.17487/RFC3258 (https://
doi.org/10.17487%2FRFC3258). RFC 3258 (https://datatracker.ietf.org/doc/html/rfc3258).
*Informational.*
12. Home-page B-root DNS server (http://www.isi.edu/b-root/), visited 8 Feb. 2015
13. "Report on Root Nameserver Locations" (http://pch.net/root-servers). Packet Clearing House.

Retrieved February 21, 2011.
14. "Root Server Technical Operations Assn" (http://www.root-servers.org/). root-servers.org.

Retrieved February 16, 2013.
15. C. Huitema (June 2001). *An Anycast Prefix for 6to4 Relay Routers* (https://datatracker.ietf.org/doc/

html/rfc3068). Network Working Group. doi:10.17487/RFC3068 (https://doi.org/10.17487%2FRFC
3068). RFC 3068 (https://datatracker.ietf.org/doc/html/rfc3068). *Informational.* Obsoleted by
RFC 7526 (https://www.rfc-editor.org/rfc/rfc7526).

# **References**

7/7/25, 8:32 AM
Anycast - Wikipedia

https://en.wikipedia.org/wiki/Anycast
5/6

---
*Page 6*

16. O. Troan (May 2015). B. Carpenter (ed.). *Deprecating the Anycast Prefix for 6to4 Relay Routers* (h

ttps://datatracker.ietf.org/doc/html/rfc7526). Internet Engineering Task Force.
doi:10.17487/RFC7526 (https://doi.org/10.17487%2FRFC7526). BCP 196. RFC 7526 (https://data
tracker.ietf.org/doc/html/rfc7526). *Best Current Practice 196.* Obsoletes RFC 3068 (https://www.rfc
-editor.org/rfc/rfc3068) and 6732 (https://www.rfc-editor.org/rfc/rfc6732).
17. "Anycast Rendezvous Point" (https://www.cisco.com/c/en/us/td/docs/ios/solutions_docs/ip_multica

st/White_papers/anycast.html). Cisco Systems. June 1, 2001.
18. "ICANN Factsheet on root server attack on 6 February 2007" (http://www.icann.org/announcement

s/factsheet-dns-attack-08mar07_v1.1.pdf) (PDF). *Factsheet*. The Internet Corporation for
Assigned Names and Numbers (ICANN). March 1, 2007. Retrieved February 21, 2011.
19. Metz, C. (2002). "IP Anycast: Point-to-(Any) Point Communication (sign-in required)". *IEEE*

*Internet Computing*. **6** (2). IEEE: 94–98. doi:10.1109/4236.991450 (https://doi.org/10.1109%2F423
6.991450).
20. Oki, Eiji; Rojas-Cessa, Roberto; Tatipamula, Mallikarjun; Vogt, Christian (April 24, 2012).

*Advanced Internet Protocols, Services, and Applications* (https://books.google.com/books?id=Tyte
75MFbHkC&q=anycast+local+and+global+nodes&pg=PA102). John Wiley & Sons. pp. 102 & 103.
ISBN 978-0-470-49903-0. Archived (https://web.archive.org/web/20200105061928/https://books.g
oogle.ca/books?id=Tyte75MFbHkC&lpg=PA103&ots=p3K484ueyF&dq=anycast%20local%20an
d%20global%20nodes&pg=PA102%23v=onepage&q=anycast%20local%20and%20global%20no
des&f=false) from the original on January 5, 2020.

Best Practices in IPv4 Anycast Routing (http://www.pch.net/resources/papers/ipv4-anycast/ipv4-an
ycast.pdf) Tutorial on anycast routing configuration.

Retrieved from "https://en.wikipedia.org/w/index.php?title=Anycast&oldid=1297796835"

# **External links**

7/7/25, 8:32 AM
Anycast - Wikipedia

https://en.wikipedia.org/wiki/Anycast
6/6
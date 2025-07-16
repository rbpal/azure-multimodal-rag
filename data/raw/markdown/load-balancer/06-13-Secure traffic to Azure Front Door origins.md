Front Door's features work best when traffic only flows through Front Door. You should configure your
origin to block traffic that hasn't been sent through Front Door. Otherwise, traffic might bypass Front
Door's web application firewall, DDoS protection, and other security features.

Note

*Origin* and *origin group* in this article refers to the backend and backend pool of the Azure Front Door
(classic) configuration.

Front Door provides several approaches that you can use to restrict your origin traffic.

# **Private Link origins**

When you use the premium SKU of Front Door, you can use Private Link to send traffic to your origin.
Learn more about Private Link origins.

You should configure your origin to disallow traffic that doesn't come through Private Link. The way
that you restrict traffic depends on the type of Private Link origin you use:

Azure App Service and Azure Functions automatically disable access through public
internet endpoints when you use Private Link. For more information, see Using Private
Endpoints for Azure Web App.
Azure Storage provides a firewall, which you can use to deny traffic from the internet. For
more information, see Configure Azure Storage firewalls and virtual networks.
Internal load balancers with Azure Private Link service aren't publicly routable. You can
also configure network security groups to ensure that you disallow access to your virtual
network from the internet.

# **Managed Identities**

Managed identities provided by Microsoft Entra ID enables your Front Door instance to securely
access other Microsoft Entra protected resources, such as Azure Blob Storage, without the need to
manage credentials. After you enable managed identity for Front Door and granting the managed
identity necessary permissions to your origin, Front Door will use the managed identity to obtain an
access token from Microsoft Entra ID for accessing the specified resource. After successfully obtaining
the token, Front Door will set the value of the token in the Authorization header using the Bearer
scheme and then forward the request to the origin. Front Door caches the token until it expires. For
more information, see use managed identities to authenticate to origins (preview).

# **Public IP address-based origins**

When you use public IP address-based origins, there are two approaches you should use together to
ensure that traffic flows through your Front Door instance:

# **Secure traffic to Azure Front Door origins**

7/7/25, 8:42 AM
Secure traffic to Azure Front Door origins

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Ffrontdoor%2Forigin-security%3Ftabs%3Dapp-service-function…
1/3

---
*Page 2*

Configure IP address filtering to ensure that requests to your origin are only accepted from
the Front Door IP address ranges.
Configure your application to verify the X-Azure-FDID header value, which Front Door
attaches to all requests to the origin, and ensure that its value matches your Front Door's
identifier.

## **IP address filtering**

Configure IP address filtering for your origins to accept traffic from Azure Front Door's backend IP
address space and Azure's infrastructure services only.

The *AzureFrontDoor.Backend* service tag provides a list of the IP addresses that Front Door uses to
connect to your origins. You can use this service tag within your network security group rules. You can
also download the Azure IP Ranges and Service Tags data set, which is updated regularly with the
latest IP addresses.

You should also allow traffic from Azure's basic infrastructure services through the virtualized host IP
addresses 168.63.129.16 and 169.254.169.254.

Warning

Front Door's IP address space changes regularly. Ensure that you use the *AzureFrontDoor.Backend*
service tag instead of hard-coding IP addresses.

## **Front Door identifier**

IP address filtering alone isn't sufficient to secure traffic to your origin, because other Azure customers
use the same IP addresses. You should also configure your origin to ensure that traffic has originated
from *your* Front Door profile.

Azure generates a unique identifier for each Front Door profile. You can find the identifier in the Azure
portal, by looking for the *Front Door ID* value in the Overview page of your profile.

When Front Door makes a request to your origin, it adds the X-Azure-FDID request header. Your origin
should inspect the header on incoming requests, and reject requests where the value doesn't match your
Front Door profile's identifier.

## **Example configuration**

The following examples show how you can secure different types of origins.

App Service and Functions
Application Gateway
Application Gateway for Containers
IIS
AKS NGINX controller

You can use App Service access restrictions to perform IP address filtering as well as header filtering.
The capability is provided by the platform, and you don't need to change your application or host.

7/7/25, 8:42 AM
Secure traffic to Azure Front Door origins

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Ffrontdoor%2Forigin-security%3Ftabs%3Dapp-service-function…
2/3

---
*Page 3*

# **Next steps**

Learn how to configure a WAF profile on Front Door.
Learn how to create a Front Door.
Learn how Front Door works.

7/7/25, 8:42 AM
Secure traffic to Azure Front Door origins

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Ffrontdoor%2Forigin-security%3Ftabs%3Dapp-service-function…
3/3
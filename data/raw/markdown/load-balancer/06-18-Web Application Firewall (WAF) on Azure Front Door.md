Azure Web Application Firewall (WAF) on Azure Front Door offers centralized protection for your
web applications. It safeguards against common exploits and vulnerabilities, ensuring high availability
and compliance. This article outlines the features of Azure Web Application Firewall on Azure Front
Door. For more information, see WAF on Azure Front Door.

# **Policy settings**

A Web Application Firewall (WAF) policy allows you to control access to your web applications using
custom and managed rules. You can adjust the policy state or configure its mode. Depending on the
settings, you can inspect incoming requests, monitor them, or take actions against requests that match a
rule. You can also set the WAF to detect threats without blocking them, which is useful when first
enabling the WAF. After evaluating its impact, you can reconfigure the WAF to prevention mode. For
more information, see WAF policy settings.

# **Web Application Firewall (WAF) on Azure**
# **Front Door**

7/7/25, 9:06 AM
Web Application Firewall (WAF) on Azure Front Door

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Ffrontdoor%2Fweb-application-firewall
1/3

![Image](images/image_page1_0.png)

---
*Page 2*

# **Managed rules**

Azure Front Door WAF protects web applications from common vulnerabilities and exploits. Azure-
managed rule sets offer easy deployment against common security threats. Azure updates these rules to
protect against new attack signatures. The default rule set includes Microsoft Threat Intelligence
Collection rules, providing increased coverage, specific vulnerability patches, and better false positive
reduction. For more information, see WAF managed rules.

Note

Managed rules are supported only by Azure Front Door Premium and Azure Front Door
(classic).
Azure Front Door (classic) supports only DRS 1.1 or below.

# **Custom rules**

Azure Web Application Firewall (WAF) with Front Door allows you to control access to your web
applications based on defined conditions. A custom WAF rule includes a priority number, rule type,
match conditions, and an action. There are two types of custom rules: match rules and rate limit rules.
Match rules control access based on specific conditions, while rate limit rules control access based on
conditions and the rate of incoming requests. For more information, see WAF custom rules.

# **Exclusion lists**

Azure Web Application Firewall (WAF) can sometimes block requests that you want to allow. WAF
exclusion lists let you omit certain request attributes from WAF evaluation, allowing the rest of the
request to be processed normally. For more information, see WAF exclusion lists.

# **Geo-filtering**

By default, Azure Front Door responds to all user requests regardless of their location. Geo-filtering
allows you to restrict access to your web application by countries/regions. For more information, see
WAF geo-filtering.

# **Bot Protection**

Azure Web Application Firewall (WAF) for Front Door includes bot protection rules to identify and
allow good bots while blocking bad bots. For more information, see configure bot protection.

# **IP restriction**

IP restriction rules in Azure WAF allow you to control access to your web applications by specifying
allowed or blocked IP addresses or IP address ranges. For more information, see configure IP
restriction.

7/7/25, 9:06 AM
Web Application Firewall (WAF) on Azure Front Door

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Ffrontdoor%2Fweb-application-firewall
2/3

---
*Page 3*

# **Rate limiting**

Rate limiting rules in Azure WAF control access based on matching conditions and the rate of
incoming requests. For more information, see What is rate limiting for Azure Front Door Service?.

# **Tuning**

Azure WAF's Default Rule Set is based on the OWASP Core Rule Set (CRS) and includes Microsoft
Threat Intelligence Collection rules. You can tune WAF rules to meet your application's specific needs
by defining rule exclusions, creating custom rules, and disabling rules. For more information, see WAF
Tuning.

# **Monitoring and logging**

Azure WAF provides monitoring and logging through integration with Azure Monitor and Azure
Monitor logs. For more information, see Azure Web Application Firewall (WAF) logging and
monitoring.

# **Next steps**

Learn how to create and apply Web Application Firewall policy to your Azure Front Door.
For more information, see Web Application Firewall (WAF) FAQ.

7/7/25, 9:06 AM
Web Application Firewall (WAF) on Azure Front Door

read://https_learn.microsoft.com/?url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Fazure%2Ffrontdoor%2Fweb-application-firewall
3/3
---
description: 'Build for message transforming between CS:GO servers and QQ groups'
---

# message-channel

## APIs

{% api-method method="post" host="https://message-channel.csgowiki.top" path="/api/register" %}
{% api-method-summary %}
Register
{% endapi-method-summary %}

{% api-method-description %}
Register new CS:GO server to QQ group
{% endapi-method-description %}

{% api-method-spec %}
{% api-method-request %}
{% api-method-form-data-parameters %}
{% api-method-parameter name="qq\_group" type="string" required=true %}
QQ group id
{% endapi-method-parameter %}

{% api-method-parameter name="sv\_port" type="string" required=true %}
origin CS:GO server's port opened for message-channel
{% endapi-method-parameter %}

{% api-method-parameter name="sv\_remark" type="string" required=true %}
origin CS:GO server's remark, shown in QQ group.
{% endapi-method-parameter %}

{% api-method-parameter name="sv\_host" type="string" required=true %}
origin CS:GO server's host\(IP or domain\)
{% endapi-method-parameter %}
{% endapi-method-form-data-parameters %}
{% endapi-method-request %}

{% api-method-response %}
{% api-method-response-example httpCode=200 %}
{% api-method-response-example-description %}

{% endapi-method-response-example-description %}

```
{
    "status": "ok",
    "message": "server on registed, need qq group admins to verify",
    "token": "xxx"
}
```
{% endapi-method-response-example %}
{% endapi-method-response %}
{% endapi-method-spec %}
{% endapi-method %}

{% hint style="info" %}
 Super-powers are granted randomly so please submit an issue if you're not happy with yours.
{% endhint %}

Once you're strong enough, save the world:

{% code title="hello.sh" %}
```bash
# Ain't no code for that yet, sorry
echo 'You got to trust me on this, I saved the world'
```
{% endcode %}




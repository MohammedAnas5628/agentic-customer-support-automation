---
document_id: EM-KB-ACCOUNT-SECURITY-001
effective_date: 2026-09-10
owner: ElectroMart Trust and Support Operations
status: active
version: 1
---

# ElectroMart Account and Security Policy

## Overview

This policy defines account-management, authentication, password,
profile, privacy, and security-support rules.

Customer account information is sensitive. Customer-specific account
access must always be controlled through authentication and
authorization checks.

## Account Access

Customers may access their ElectroMart account using the authentication
methods supported by the platform.

A customer must not share account credentials with another person.

ElectroMart support does not require a customer's password, OTP, UPI
PIN, CVV, or full card credentials.

## Password Reset

If a customer forgets their password, they should use the authorized
password-reset process.

Support may guide the customer through the process but must not ask for
or obtain the customer's existing password.

Password-reset links or verification codes must be used only by the
authorized account holder.

## OTP Security

OTP codes are authentication credentials.

ElectroMart support must never ask a customer to disclose an OTP.

Customers should not share OTPs with support agents, delivery personnel,
callers, or other third parties claiming to represent ElectroMart.

If a customer receives an unexpected OTP, the customer should not share
it and should report suspicious activity when appropriate.

## Profile Information

Customers may be able to update supported profile fields through their
account settings.

Some changes may require additional verification.

Examples include:

-   Name.
-   Phone number.
-   Email address.
-   Saved addresses.

The exact fields and verification requirements are controlled by the
account system.

## Delivery Address vs Account Address

A saved account address and an order's delivery address are not
necessarily the same.

Changing a saved address does not automatically change the delivery
address of an existing order.

Existing-order address changes remain subject to the rules in
`shipping_and_delivery.md`.

## Unauthorized Account Access

If a customer believes someone accessed their account without
permission:

1.  Do not request the customer's password or OTP.
2.  Advise the customer to use the authorized
    account-security/password-reset process.
3.  Review available account-security signals through authorized tools.
4.  Escalate the incident according to `escalation_rules.md` when
    unauthorized access is suspected or confirmed.

Support must not disclose security information that could help an
unauthorized person access the account.

## Suspicious Payment Activity

If a customer reports an unauthorized payment:

-   Verify the account and transaction through authorized systems.
-   Do not request full card credentials, CVV, OTP, UPI PIN, or banking
    password.
-   Escalate according to the payment and security escalation rules.
-   Advise the customer to contact their bank or payment provider where
    appropriate.

See `payments.md`.

## Customer Authentication and Authorization

Authentication confirms who the customer is.

Authorization determines what information or actions that customer is
allowed to access.

Both are required for customer-specific operations.

For example, knowing an order ID does not by itself authorize a person
to access the order details.

## Sensitive Information Handling

Support must minimize exposure of sensitive information.

Do not disclose:

-   Full payment-card numbers.
-   CVVs.
-   Passwords.
-   OTPs.
-   UPI PINs.
-   Authentication secrets.
-   Another customer's personal information.

When displaying account information, support should use the minimum
information necessary to resolve the request.

## Privacy Requests

Customers may ask about how their account information is used or request
support with privacy-related matters.

The AI agent should provide only the information covered by
ElectroMart's approved privacy/account policy and escalate requests
requiring formal privacy review.

The agent should not invent a data-retention period or legal right that
is not documented.

## Account Lockout

An account may be temporarily restricted after repeated unsuccessful
authentication attempts or security-risk detection.

The customer should use the authorized recovery process.

Support should not bypass security controls merely because a customer
requests immediate access.

## Account Changes and Existing Orders

Changing account information does not automatically modify historical
order records.

For example:

-   Changing a profile email does not rewrite a past invoice.
-   Changing a saved address does not change a shipped order.
-   Changing a phone number does not automatically change a courier's
    existing shipment contact record.

Order-specific changes must use the applicable order workflow.

## Security Edge Cases

### Customer asks support to tell them their OTP

The request must be refused. OTPs are private authentication
credentials.

### Customer says a delivery agent asked for an OTP

The case should be assessed carefully. Customers should never share an
OTP merely because someone claims to represent ElectroMart.

### Customer knows an order ID but is not the account holder

The order ID alone does not establish authorization.

### Customer wants support to disable security verification

Support must not bypass required authentication or security controls
without an authorized security workflow.

## Related Policies

-   `customer_support.md` for support handling.
-   `escalation_rules.md` for security escalation.
-   `payments.md` for payment security.
-   `shipping_and_delivery.md` for order-address changes.

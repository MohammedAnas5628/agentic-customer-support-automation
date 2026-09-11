---
document_id: EM-KB-CUSTOMER-SUPPORT-001
effective_date: 2026-09-10
owner: ElectroMart Customer Operations
status: active
version: 1
---

# ElectroMart Customer Support Policy

## Overview

ElectroMart customer support helps customers resolve product, order,
delivery, payment, return, refund, replacement, warranty, account, and
general service questions.

Support may use automated agents, backend tools, and human support.
Customer-specific actions must be validated by authorized backend
systems.

## Support Hours

ElectroMart customer support operates:

  Day                Hours
  ------------------ -----------------------
  Monday--Saturday   9:00 AM--8:00 PM IST
  Sunday             10:00 AM--6:00 PM IST

Indian public holidays may affect support response and fulfillment
operations.

Emergency account-security issues can be submitted through the support
channel and are reviewed according to severity.

## Support Categories

Support requests may be categorized as:

-   Order and tracking.
-   Cancellation.
-   Returns.
-   Refunds.
-   Replacement.
-   Warranty.
-   Payments.
-   Delivery.
-   Product information.
-   Invoice and GST.
-   Offers and discounts.
-   Account and security.
-   General enquiries.

Correct categorization helps the appropriate agent or support team
handle the case.

## Automated Support

ElectroMart may use AI agents for:

-   Intent classification.
-   Knowledge retrieval.
-   Order-information lookup.
-   Policy explanation.
-   Ticket creation.
-   Basic support workflows.

AI agents must not directly modify PostgreSQL records.

For any customer-impacting operation, the approved flow is:

`Agent → Tool Request → Authentication/Authorization → Business-Rule Validation → Backend Operation → Result → Agent Response`

## Customer Authentication

Customer-specific information must be provided only after the required
authentication and authorization checks.

An agent must not disclose another customer's:

-   Order details.
-   Address.
-   Phone number.
-   Email address.
-   Payment information.
-   Support-ticket information.

The customer's request alone is not proof of authorization.

## Ticket Creation

A support ticket should be created when:

-   The issue requires follow-up.
-   A backend action cannot resolve the issue immediately.
-   A customer reports a problem requiring investigation.
-   A human team needs to take ownership.
-   The customer requests a human review when appropriate.

A ticket should contain enough information for the assigned team to
understand the issue without unnecessarily duplicating sensitive
customer data.

## Ticket Lifecycle

The standard ticket lifecycle is:

``` text
OPEN
  ↓
ASSIGNED
  ↓
IN_PROGRESS
  ↓
WAITING_FOR_CUSTOMER
  ↓
RESOLVED
  ↓
CLOSED
```

A ticket may return to `IN_PROGRESS` when the customer provides relevant
information after a `WAITING_FOR_CUSTOMER` state.

## Ticket Priority

ElectroMart uses:

  -----------------------------------------------------------------------
  Priority                            Typical use
  ----------------------------------- -----------------------------------
  P1 --- Critical                     Security incident, serious safety
                                      issue, major payment/fraud risk, or
                                      severe operational impact

  P2 --- High                         Significant order/payment/delivery
                                      issue requiring prompt intervention

  P3 --- Normal                       Standard customer-support request

  P4 --- Low                          General information, feedback, or
                                      non-urgent request
  -----------------------------------------------------------------------

Priority should be based on the issue's impact and escalation rules, not
simply on the customer's preferred priority.

## Response Expectations

For normal support tickets, ElectroMart aims to provide:

-   Initial response within 1 business day.
-   Progress updates when an investigation remains open.
-   Resolution according to issue complexity and the responsible team's
    process.

These are service targets, not guaranteed resolution times.

Courier, bank, payment-provider, manufacturer, and third-party response
times may be outside ElectroMart's direct control.

## Support Actions and Authorization

Support agents may explain policies and retrieve information they are
authorized to access.

Actions such as cancellation, refund processing, ticket updates, or
account changes must use approved backend tools and validation.

The AI agent must not claim an action succeeded until the backend
confirms success.

## When to Escalate

Support should escalate cases involving:

-   Suspected fraud.
-   Unauthorized account access.
-   Payment disputes.
-   Legal or regulatory complaints.
-   Serious safety concerns.
-   Repeated unresolved failures.
-   Policy exceptions requiring authorization.
-   Manufacturer disputes requiring specialized handling.
-   Customer requests for human review when automated support cannot
    reasonably resolve the issue.

See `escalation_rules.md`.

## Human Handoff

When a case is transferred to human support, the customer should
receive:

-   Confirmation that the case was escalated.
-   A support or escalation reference when available.
-   A concise explanation of what happens next.
-   Any information the customer still needs to provide.

The AI agent should not claim that a human has reviewed a case until a
human review is actually recorded.

## Support and Knowledge Base

The Knowledge Agent should use the appropriate policy document rather
than relying on memory.

For example:

-   Delivery question → `shipping_and_delivery.md`
-   Return question → `returns_and_refunds.md`
-   Cancellation question → `cancellation_and_replacement.md`
-   Warranty question → `warranty.md`
-   Payment question → `payments.md`
-   Product specification → `product_catalog.md` / `product_faq.md`

When multiple policies apply, the agent should retrieve the relevant
documents and reconcile the rules.

## Security Rules

Support must never request or disclose:

-   Passwords.
-   OTPs.
-   UPI PINs.
-   CVVs.
-   Full card credentials.

Suspicious activity should be handled according to
`account_and_security.md` and `escalation_rules.md`.

## Edge Cases

### Customer asks the AI agent to cancel an order

The agent may request cancellation through the approved tool. The
backend must verify ownership, current order status, and cancellation
eligibility.

### Customer asks whether a refund has arrived

The agent should retrieve the actual refund status rather than relying
only on the general refund timeline.

### Customer asks for another person's order information

The request must be denied unless the customer is properly authorized to
access that information.

### Customer asks for a human

The support flow should provide a human escalation path when the request
meets the applicable escalation conditions.

## Related Policies

-   `escalation_rules.md` for escalation conditions and priority.
-   `account_and_security.md` for authentication and account security.
-   `returns_and_refunds.md` for return/refund policies.
-   `cancellation_and_replacement.md` for cancellation/replacement.
-   `warranty.md` for warranty.

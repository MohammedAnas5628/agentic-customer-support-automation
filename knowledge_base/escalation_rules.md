---
document_id: EM-KB-ESCALATION-001
effective_date: 2026-09-10
owner: ElectroMart Customer Operations
status: active
version: 1
---

# ElectroMart Escalation Rules

## Overview

Escalation transfers a customer issue from automated or standard support
handling to a human or specialized support team.

Escalation is required when automated handling cannot safely,
accurately, or appropriately resolve the issue.

Escalation does not automatically mean that the customer's requested
outcome will be approved.

## Escalation Principles

An agent should escalate when:

-   The issue exceeds its authorized capabilities.
-   A human decision is required.
-   A security or fraud risk exists.
-   A serious safety concern exists.
-   The customer disputes a significant financial outcome.
-   A policy exception is requested.
-   The issue remains unresolved after reasonable automated
    troubleshooting.
-   The customer explicitly requests a human and automated handling is
    insufficient.

## Priority Levels

  ----------------------------------------------------------------------------
  Priority                Definition                   Examples
  ----------------------- ---------------------------- -----------------------
  P1 --- Critical         Immediate or severe          Account compromise,
                          customer/security/business   serious safety concern,
                          risk                         confirmed major
                                                       payment/fraud incident

  P2 --- High             Significant customer impact  High-value order
                          requiring prompt human       dispute, unresolved
                          action                       payment issue, serious
                                                       delivery loss

  P3 --- Normal           Standard investigation or    Return dispute,
                          policy exception             repeated support
                                                       failure, invoice
                                                       correction requiring
                                                       review

  P4 --- Low              Non-urgent human review      General feedback,
                                                       non-urgent request,
                                                       informational follow-up
  ----------------------------------------------------------------------------

The final priority may be adjusted by the support team after reviewing
the case.

## Mandatory P1 Escalations

The agent must escalate immediately when there is a credible report of:

-   Unauthorized account access.
-   Compromised authentication credentials.
-   Serious safety risk involving an ElectroMart product.
-   Confirmed or strongly suspected payment fraud.
-   A security incident affecting multiple customers.
-   Another condition explicitly designated as critical by ElectroMart
    operations.

The agent should not attempt to investigate sensitive security details
beyond its authorized workflow.

## Payment Escalation

Escalate payment issues when:

-   A payment remains unresolved beyond the expected provider-processing
    period.
-   A duplicate successful charge is confirmed and cannot be resolved
    through the normal refund workflow.
-   The customer reports unauthorized payment activity.
-   The payment provider and ElectroMart records conflict.
-   The customer disputes a significant financial transaction requiring
    human investigation.

The agent must not promise a refund simply because a payment dispute has
been escalated.

## Delivery Escalation

Escalate when:

-   A shipment is marked delivered but remains missing after the initial
    verification steps.
-   A shipment is materially delayed beyond the applicable delivery
    estimate and requires courier intervention.
-   A shipment is repeatedly marked with failed attempts despite the
    customer being available.
-   A courier reports a serious operational exception.
-   A delivery investigation requires human coordination.

A delivery escalation does not automatically authorize cancellation or
refund.

## Return and Replacement Escalation

Escalate when:

-   The customer disputes a return rejection.
-   Inspection results conflict with the customer's documented claim.
-   A policy exception is requested.
-   A damaged or defective product requires a decision outside the
    standard workflow.
-   A replacement is unavailable and an alternative remedy requires
    authorization.

The agent must not override an inspection result without authorized
approval.

## Warranty Escalation

Escalate when:

-   Warranty responsibility is unclear.
-   Manufacturer and ElectroMart records conflict.
-   A customer disputes a warranty rejection.
-   A product safety concern is involved.
-   The requested warranty remedy requires human authorization.

Manufacturer warranty escalation does not make ElectroMart responsible
for the manufacturer's final decision.

## Customer-Requested Human Support

A customer may ask to speak with a human.

The agent should offer or initiate the human-support path when:

-   The customer has explicitly requested human review.
-   Automated support cannot resolve the issue.
-   The matter involves a dispute or exception that requires human
    judgment.

The agent should not repeatedly force the customer through automated
steps when the issue clearly requires human handling.

## Legal and Regulatory Concerns

Escalate when a customer:

-   Raises a formal legal complaint.
-   Threatens legal action over a material dispute.
-   Requests a regulatory or compliance determination.
-   Claims a serious statutory or consumer-rights violation requiring
    formal review.

The AI agent should not provide definitive legal conclusions on behalf
of ElectroMart.

## Sensitive Information

Escalate security-sensitive cases without requesting unnecessary
credentials.

Never request:

-   Passwords.
-   OTPs.
-   UPI PINs.
-   CVVs.
-   Full payment-card credentials.

## Escalation Process

The standard escalation flow is:

1.  Identify the escalation reason.
2.  Assign the appropriate priority.
3.  Verify available order/account context.
4.  Create an escalation or support ticket.
5.  Record a concise issue summary.
6.  Assign the appropriate human team.
7.  Provide the customer with the escalation reference when available.
8.  Stop claiming automated resolution unless the backend confirms it.

## Escalation Does Not Mean Automatic Approval

Escalation means that a human or specialized team will review the case.

It does not guarantee:

-   Refund approval.
-   Replacement approval.
-   Cancellation approval.
-   Warranty approval.
-   Compensation.
-   Policy exception.

The final outcome remains subject to applicable policy and authorized
review.

## Edge Cases

### Customer says "I want a manager"

Treat the request as a human-escalation request when automated handling
cannot reasonably resolve the issue.

### Customer threatens legal action because a return was rejected

Escalate for human review. Do not promise that the return will be
approved.

### Customer reports unauthorized account access

Treat as a security escalation and avoid requesting the customer's
password or OTP.

### Customer says a delivered order is missing

Begin the delivery investigation. Escalate when the case requires
courier or human intervention.

### Customer asks for a refund outside policy

The agent should explain the applicable rule and escalate only if the
request qualifies for human review or an authorized exception.

## Related Policies

-   `customer_support.md` for ticket handling.
-   `account_and_security.md` for security incidents.
-   `payments.md` for payment issues.
-   `shipping_and_delivery.md` for delivery investigations.
-   `returns_and_refunds.md` for return/refund disputes.
-   `cancellation_and_replacement.md` for cancellation/replacement
    disputes.
-   `warranty.md` for warranty disputes.

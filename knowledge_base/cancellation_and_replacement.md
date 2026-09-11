---
document_id: EM-KB-CANCEL-REPLACE-001
effective_date: 2026-09-10
owner: ElectroMart Order Operations
status: active
version: 1
---

# ElectroMart Cancellation and Replacement Policy

## Overview

This policy defines when an order can be cancelled and when a delivered
product may qualify for replacement.

A **cancellation** stops an order before delivery.

A **replacement** is the authorized process of supplying another product
because the delivered product is damaged, defective, incorrect, or
otherwise qualifies under the replacement rules.

Cancellation and replacement are separate processes.

## Order Statuses Used for Cancellation

ElectroMart uses the following operational statuses for cancellation
decisions:

-   `PLACED`
-   `CONFIRMED`
-   `PROCESSING`
-   `PACKED`
-   `SHIPPED`
-   `OUT_FOR_DELIVERY`
-   `DELIVERED`
-   `CANCELLED`

The backend order system is the source of truth for the current status
of a specific order.

## Cancellation Eligibility

Customers can request cancellation while an order is in `PLACED`,
`CONFIRMED`, or `PROCESSING`, subject to backend verification.

Cancellation is not permitted after an order enters `PACKED`, `SHIPPED`,
`OUT_FOR_DELIVERY`, or `DELIVERED`.

  -----------------------------------------------------------------------
  Order status                             Standard customer cancellation
  ------------------------------ ----------------------------------------
  PLACED                                                          Allowed

  CONFIRMED                                                       Allowed

  PROCESSING                       Allowed if the cancellation request is
                                                  accepted before packing

  PACKED                                                      Not allowed

  SHIPPED                                                     Not allowed

  OUT_FOR_DELIVERY                                            Not allowed

  DELIVERED                                                   Not allowed

  CANCELLED                                                Not applicable
  -----------------------------------------------------------------------

Because `PROCESSING` can change quickly, the cancellation tool must
verify the live order status before performing the operation.

## Cancellation Process

The standard cancellation process is:

1.  Customer requests cancellation.
2.  The system authenticates the customer and verifies order ownership.
3.  The backend checks the current order status.
4.  The backend checks cancellation eligibility.
5.  If eligible, the cancellation operation is performed.
6.  If payment was already collected, the applicable refund process
    begins.
7.  Customer receives the cancellation result.

The LLM must not directly change an order status or database record.

## Cancellation After Shipment

A shipped order cannot normally be cancelled.

If a customer no longer wants a shipped product:

1.  The customer should wait for delivery.
2.  If the product is return-eligible, the customer may submit a return
    request within the applicable return window.
3.  The return and refund process then follows `returns_and_refunds.md`.

A customer must not be instructed to falsely refuse delivery solely to
bypass the normal return process.

## Cancellation Refunds

If a prepaid order is successfully cancelled before shipment, the
applicable refund is initiated according to `returns_and_refunds.md`.

The exact refund amount must come from the order/refund system because
discounts, shipping charges, taxes, or other order components may affect
the amount.

COD orders that are successfully cancelled before shipment normally do
not require a refund because no payment was collected.

## Replacement Eligibility

A delivered product may qualify for replacement when the product is:

-   Damaged on arrival.
-   Defective on arrival.
-   Incorrectly supplied.
-   Missing an essential component where the applicable product process
    provides replacement.

Replacement requests should normally be submitted within **7 calendar
days from delivery**.

Certain products may have a manufacturer-specific DOA or defect process.
The applicable product record and warranty information must be checked.

## Damaged Product

A customer who receives a visibly damaged product should report it as
soon as possible.

ElectroMart may request:

-   Photographs of the outer package.
-   Photographs of the product damage.
-   Photographs of the shipping label.
-   A short video or other evidence where appropriate.
-   Product serial-number information.

Evidence requirements are used to support verification and do not
guarantee approval.

A damaged-product case may result in replacement, return/refund, or
another approved remedy depending on inspection and product eligibility.

## Defective Product

A product that does not function as expected may qualify for replacement
when the issue occurs within the applicable replacement period and the
defect is verified.

Customers may be asked to perform basic troubleshooting before
replacement is approved.

Troubleshooting must not require the customer to perform unsafe actions
or unauthorized repairs.

If the defect is reported after the replacement period, the warranty
policy should be checked.

## Wrong Product Received

If the customer receives a different product from the one ordered, the
customer should report the issue promptly.

After verification, ElectroMart may arrange return and replacement of
the incorrect product.

The customer should not use, modify, activate, or dispose of the
incorrectly supplied product while the case is being reviewed.

## Missing Accessories or Components

If a required accessory or component is missing, support should first
verify the product's official package contents.

If the missing item is included in the documented package contents,
ElectroMart may arrange the appropriate remedy, which can include
shipment of the missing component, replacement, or return/refund
depending on the case.

## Replacement Inspection

A replacement request may require verification before approval.

Inspection can include:

-   Product identity and serial number.
-   Physical condition.
-   Functional defect.
-   Included components.
-   Signs of misuse.
-   Evidence of unauthorized repair or modification.

A replacement is not automatically approved merely because the customer
reports a problem.

## Replacement Availability

Replacement is subject to availability of the same product or an
approved replacement option.

If the same product is unavailable, ElectroMart may offer:

-   Refund through the applicable refund process.
-   An equivalent alternative where the customer and ElectroMart agree
    to the applicable terms.
-   Another authorized resolution.

Support must not promise a specific substitute product without checking
availability and authorization.

## Replacement After the Replacement Window

The standard replacement window is **7 calendar days from delivery**.

After that period, a replacement request based on a newly reported
functional fault is generally handled under the warranty process when
warranty coverage applies.

A warranty claim is different from a standard replacement request.

## Replacement vs Warranty

Use the replacement process when the product qualifies for replacement
within the applicable replacement period.

Use the warranty process when:

-   The replacement window has expired.
-   The product develops a covered fault during the warranty period.
-   The manufacturer is responsible for the applicable warranty claim.

ElectroMart may assist the customer with a manufacturer warranty claim,
but assistance does not mean ElectroMart becomes the manufacturer or
assumes manufacturer obligations.

## Exceptions

Replacement may be rejected when inspection establishes:

-   Customer misuse.
-   Accidental damage after delivery.
-   Liquid damage where excluded.
-   Unauthorized repair or modification.
-   Missing or altered serial number.
-   Fraudulent or materially inconsistent claim information.
-   Product condition that violates the applicable replacement
    requirements.

A rejection of standard replacement does not automatically mean the
customer has no warranty rights. Warranty eligibility must be assessed
separately.

## Examples and Edge Cases

### Example 1: Customer wants to cancel a shipped order

Cancellation is not permitted after shipment. If delivered and
return-eligible, the customer may use the return process.

### Example 2: Customer receives a damaged laptop

The customer should report the damage and follow the replacement
verification process. Approval depends on eligibility and inspection.

### Example 3: Customer wants replacement after 12 days

The standard 7-day replacement period has expired. If the product has
developed a functional fault, warranty eligibility should be checked
instead.

### Example 4: Customer receives the wrong product

The issue should be verified and handled through the incorrect-product
replacement/return workflow.

### Example 5: Replacement product is unavailable

Support should check live inventory and authorized alternatives. A
specific substitute or refund must not be promised without verification.

### Example 6: Customer damaged the product after delivery

Customer-caused damage is generally not eligible for ElectroMart's
standard replacement process and may also be excluded from warranty
coverage.

## Related Policies

-   `shipping_and_delivery.md` for shipment status and delivery issues.
-   `returns_and_refunds.md` for return inspection and refund
    processing.
-   `warranty.md` for faults reported after the replacement period.
-   `company_handbook.md` for general customer-support principles.

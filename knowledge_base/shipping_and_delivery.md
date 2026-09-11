---
document_id: EM-KB-SHIPPING-001
effective_date: 2026-09-10
owner: ElectroMart Fulfillment Operations
status: active
version: 1
---

# ElectroMart Shipping and Delivery Policy

## Overview

This policy defines ElectroMart's shipping, delivery, tracking,
delivery-delay, failed-delivery, and address-change rules for orders
shipped within India.

Delivery eligibility and customer-specific shipment status must be
verified using the order and shipment systems. This document defines the
general policy and does not contain customer or order data.

## Delivery Applicability

ElectroMart delivers to serviceable Indian pincodes.

Pincode serviceability can depend on:

-   Product type.
-   Product size or handling requirements.
-   Courier coverage.
-   Destination.
-   Temporary operational restrictions.

A city being generally serviceable does not guarantee service to every
pincode.

## Shipping Methods

ElectroMart uses the following standard shipping options when available:

  -------------------------------------------------------------------------
  Shipping method              Typical delivery time Availability
  --------------------- ---------------------------- ----------------------
  Standard Delivery               3--7 business days Most serviceable
                                                     locations

  Express Delivery                1--3 business days Selected products and
                                                     pincodes

  Extended-area                  7--12 business days Selected remote or
  Delivery                                           difficult-to-service
                                                     locations
  -------------------------------------------------------------------------

The delivery estimate begins after the order is confirmed for
fulfillment, not necessarily when the customer places the order.

Business days are Monday through Saturday, excluding applicable public
holidays and declared non-operational fulfillment days.

The checkout system is the source of truth for the delivery estimate
shown for a specific order.

## Shipping Charges

Standard shipping is free for orders with a merchandise value of ₹999 or
more when the destination and products qualify for the free-shipping
program.

For eligible orders below ₹999, a standard shipping charge of ₹79 may
apply.

Express Delivery, where offered, may carry an additional charge of ₹149.

Extended-area or special-handling charges may apply when shown at
checkout.

The amount displayed at checkout is authoritative for a specific order.
Promotional offers may waive or change shipping charges.

## Order Processing and Dispatch

After an order is placed:

1.  Payment or COD eligibility is validated.
2.  The order is confirmed.
3.  Inventory is allocated where applicable.
4.  The fulfillment center processes and packs the product.
5.  The shipment is handed to a courier.
6.  Tracking information becomes available after shipment creation.

An order can take up to 1 business day to move from confirmed to
processing.

Delivery estimates do not mean that the package will necessarily arrive
on the earliest stated day.

## Order Tracking

Customers can track a shipped order using the tracking information
associated with the order.

Common shipment statuses include:

  -----------------------------------------------------------------------
  Status                              Meaning
  ----------------------------------- -----------------------------------
  Shipment Created                    Shipment information has been
                                      generated; courier movement may not
                                      have started.

  Picked Up                           Courier has collected the package.

  In Transit                          Package is moving through the
                                      courier network.

  At Local Facility                   Package has reached a facility
                                      serving the destination.

  Out for Delivery                    Courier has assigned the package
                                      for delivery that day.

  Delivered                           Courier system records the package
                                      as delivered.

  Delivery Attempted                  A delivery attempt was made but
                                      delivery was not completed.

  Exception                           Shipment requires attention because
                                      of an operational or delivery
                                      issue.
  -----------------------------------------------------------------------

The customer-support agent must not invent a shipment location or
delivery date when live tracking information is unavailable.

## Delivery Delays

A shipment is considered delayed when it passes the latest delivery date
shown by the applicable delivery estimate and remains undelivered.

For a delayed shipment, support should:

1.  Check the latest shipment status.
2.  Check for courier exceptions.
3.  Provide the latest verified information.
4.  Create or escalate a support case when the delay requires
    operational intervention.

A delay does not automatically create a right to cancellation, refund,
or compensation.

If the customer wants to cancel because of a delay, the cancellation
rules in `cancellation_and_replacement.md` apply.

If the order is eventually delivered and the customer wants to return
it, the return rules in `returns_and_refunds.md` apply.

## Failed Delivery Attempts

A courier may make up to 3 delivery attempts unless the courier's
operational rules require fewer attempts.

A delivery attempt can fail because of:

-   Customer unavailable.
-   Incorrect or incomplete address.
-   Customer unreachable.
-   Access restrictions.
-   Customer-requested rescheduling.
-   Local courier constraints.

After repeated failed attempts, the shipment may be returned to
ElectroMart.

A failed delivery does not automatically count as a customer-requested
cancellation.

## Incorrect Delivery Address

Customers should verify the delivery address before order confirmation.

Address changes are permitted only when all of the following are true:

-   The order has not been shipped.
-   The requested address is serviceable.
-   The change can be completed through the authorized support/order
    workflow.
-   The change does not violate payment or fraud-prevention controls.

Once an order is shipped, the delivery address cannot normally be
changed by customer support.

For a shipped order, the customer may be able to coordinate directly
with the courier for permitted delivery instructions, but ElectroMart
cannot guarantee courier-side changes.

If an incorrect address causes a failed delivery or return-to-sender
event, the customer may need to place a new order or follow the
applicable support process.

## Product Marked Delivered but Not Received

If the courier status shows `Delivered` but the customer states that the
package was not received, support must not immediately declare the order
lost or issue an automatic refund.

The case should be verified through the delivery investigation process.

The customer should first check:

-   Household members.
-   Building reception/security.
-   Authorized neighbors where applicable.
-   Delivery location or proof-of-delivery information.

If the package remains missing, a delivery investigation should be
opened.

The investigation outcome determines the next action. Refund or
replacement is not guaranteed solely because the tracking status says
delivered or because the customer reports non-receipt.

## Damaged Package at Delivery

Customers should report visible package damage as soon as possible.

If a product is damaged after delivery, the product-damage handling
rules in `cancellation_and_replacement.md` and `returns_and_refunds.md`
apply.

A shipping claim does not automatically mean the customer is entitled to
a refund before inspection.

## Partial Shipments

For multi-item orders, products may be shipped separately.

Each shipment may have a different tracking number and delivery date.

A customer should not be told that the complete order is lost merely
because one item has not arrived with another item.

Support should check the individual shipment records.

## Delivery and Cancellation Relationship

Once an order is shipped, standard cancellation is not permitted.

If the customer no longer wants a shipped order, support should explain
that cancellation is unavailable and direct the customer to the
applicable return process after delivery, where the product is
return-eligible.

See `cancellation_and_replacement.md` for cancellation eligibility.

## Examples and Edge Cases

### Example 1: Customer wants to cancel a shipped order

The order cannot normally be cancelled after shipment. If delivered, the
customer may request a return if the product satisfies the return
policy.

### Example 2: Delivery is two days late

Support should verify the latest shipment status and investigate the
delay. A delay alone does not automatically authorize a refund or
cancellation.

### Example 3: Customer entered the wrong address before shipping

If the order has not shipped and the new address is serviceable, an
address change may be possible through the authorized workflow.

### Example 4: Customer entered the wrong address after shipping

The address cannot normally be changed by ElectroMart after shipment.
Courier-side options may exist, but they are not guaranteed.

### Example 5: Order says delivered but customer did not receive it

Open or escalate a delivery investigation. Do not promise an immediate
refund or replacement.

## Related Policies

-   `company_handbook.md` for general company and support information.
-   `cancellation_and_replacement.md` for order cancellation and product
    replacement.
-   `returns_and_refunds.md` for returns and refunds after delivery.
-   `warranty.md` for product faults that occur after the applicable
    return/replacement period.

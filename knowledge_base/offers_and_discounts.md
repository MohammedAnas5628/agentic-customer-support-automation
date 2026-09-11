---
document_id: EM-KB-OFFERS-001
effective_date: 2026-09-10
owner: ElectroMart Commercial Operations
status: active
version: 1
---

# ElectroMart Offers and Discounts Policy

## Overview

ElectroMart may provide promotional discounts, coupon codes, bank
offers, and customer-specific promotions.

Offers are subject to their stated eligibility conditions and validity
periods.

The checkout and promotion systems are the source of truth for whether a
particular customer, order, or product qualifies for an offer.

## General Offer Rules

Unless an offer explicitly states otherwise:

-   An offer applies only during its published validity period.
-   An offer cannot be transferred to another customer.
-   An offer cannot be exchanged for cash.
-   An expired offer cannot be restored by customer support.
-   An offer may have product, category, payment-method, customer, or
    minimum-order restrictions.
-   A promotion may not be combined with another promotion unless
    stacking is explicitly permitted.

## Representative Promotional Programs

The following fictional offers illustrate ElectroMart's promotion rules.

### NEWEMART10

-   Discount: 10% off.
-   Maximum discount: ₹1,500.
-   Minimum merchandise value: ₹5,000.
-   Eligibility: First completed order from an eligible new customer.
-   One use per eligible customer.
-   Cannot be combined with another coupon.

### FESTIVE1500

-   Discount: ₹1,500 off.
-   Minimum merchandise value: ₹20,000.
-   Eligible categories: Selected laptops and monitors.
-   One use per order.
-   Cannot be combined with another percentage-off coupon unless the
    campaign explicitly permits stacking.

### ACCESSORY500

-   Discount: ₹500 off.
-   Minimum accessory merchandise value: ₹3,000.
-   Eligible category: Selected accessories.
-   One use per eligible order.

These representative campaigns are policy examples, not guarantees of a
currently active promotion. Current promotional availability must be
checked through the promotion system.

## Coupon Eligibility

A coupon can fail even when the customer has entered the code correctly.

Common reasons include:

-   Minimum order value not met.
-   Product not eligible.
-   Coupon expired.
-   Customer has already used the coupon.
-   Payment method restriction.
-   Coupon not valid in the customer's promotion segment.
-   Another incompatible promotion is already applied.
-   Coupon usage limit has been reached.

## Minimum Order Value

Minimum order value is calculated according to the specific offer terms.

Unless the offer states otherwise, shipping charges are not counted
toward the minimum merchandise value.

Discounted merchandise value may be used differently depending on the
promotion definition. The promotion system is authoritative for the
final eligibility result.

## Offer Stacking

Customers cannot assume that multiple discounts can be combined.

Two coupons may be stacked only when the promotion terms explicitly
allow stacking.

A bank/card promotion and a coupon may also have separate restrictions.

The checkout system determines whether the combination is accepted.

## Bank and Payment Offers

Bank offers may require:

-   Eligible card type.
-   Minimum transaction value.
-   Specific bank or payment method.
-   Maximum discount.
-   Validity period.
-   Transaction-level eligibility.

If a customer pays through an unsupported method, the bank offer may not
apply.

## Failed Coupon Application

If a coupon does not apply:

1.  Verify the coupon validity.
2.  Verify the minimum order value.
3.  Verify product/category eligibility.
4.  Check customer eligibility.
5.  Check whether another promotion conflicts.
6.  Use the promotion system for the final result.

Support must not manually promise a discount that the promotion system
has rejected unless an authorized exception is approved.

## Discount and Refund Interaction

If an order containing a discount is partially returned or cancelled,
the refund amount may reflect the promotional terms and recalculated
order value.

Customers should not be promised a refund equal to the undiscounted
product price.

The order/refund system determines the exact amount.

## Offer Expiry

An expired promotion cannot normally be applied retroactively.

If the customer placed an eligible order while the offer was valid but
the discount was not applied due to a system issue, support may
investigate the transaction and apply an authorized correction where
permitted.

## Fraud and Abuse

ElectroMart may restrict promotions when there is evidence of:

-   Coupon misuse.
-   Multiple accounts created to bypass one-time-use restrictions.
-   Automated or fraudulent promotion activity.
-   Manipulation of referral or discount mechanisms.

Such cases may be escalated according to `escalation_rules.md`.

## Offer Edge Cases

### Customer wants to use two coupons

Do not promise stacking. Check the specific promotion rules and checkout
result.

### Customer's order is ₹4,900 and coupon requires ₹5,000

The minimum merchandise value is not met, so the coupon is not eligible
unless the promotion terms define another calculation.

### Customer's coupon expired yesterday

The expired coupon cannot normally be applied.

### Customer returned one item from a discounted multi-item order

The refund must be calculated from the actual order and promotion rules
rather than simply refunding the displayed standalone price.

## Related Policies

-   `payments.md` for payment-method restrictions.
-   `returns_and_refunds.md` for refunds after promotional orders.
-   `invoices_and_tax.md` for invoice treatment of discounts and taxes.
-   `escalation_rules.md` for suspected promotion abuse or authorized
    exceptions.

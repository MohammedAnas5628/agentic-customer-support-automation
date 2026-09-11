---
document_id: EM-KB-PAYMENTS-001
effective_date: 2026-09-10
owner: ElectroMart Payments Operations
status: active
version: 1
---

# ElectroMart Payments Policy

## Overview

This policy defines the payment methods supported by ElectroMart,
payment-status handling, common payment failures, duplicate charges,
Cash on Delivery (COD), and payment-related customer support.

Customer-specific payment status, transaction identifiers, collected
amounts, refund amounts, and payment-provider responses must be obtained
from the payment and order systems. This document defines general policy
only.

## Supported Payment Methods

ElectroMart supports the following payment methods where available at
checkout:

-   UPI.
-   Credit cards.
-   Debit cards.
-   Net banking.
-   Eligible digital wallets.
-   Cash on Delivery (COD) for eligible orders and pincodes.

The payment options displayed during checkout are the authoritative
options for a specific order.

## UPI Payments

Customers may pay through supported UPI applications.

ElectroMart does not require a customer to disclose:

-   UPI PIN.
-   OTP.
-   Full card credentials.
-   Banking password.

A customer should never share these credentials with customer support.

A UPI payment may remain pending even when the customer has initiated
the payment. Support should verify the payment gateway and order records
before treating the payment as successful or failed.

## Card Payments

ElectroMart accepts eligible credit and debit cards through its
supported payment gateway.

A card payment can have statuses such as:

-   `SUCCESS`
-   `FAILED`
-   `PENDING`
-   `REVERSED`

A successful payment must be confirmed by the payment system before an
order is treated as paid.

## Net Banking and Wallets

Net banking and supported digital wallets may be available depending on
the checkout configuration.

If a payment fails after the customer leaves the bank or wallet
interface, the customer should not immediately repeat the payment if the
original transaction may still be pending.

Support should first verify the transaction status.

## Cash on Delivery

COD is available only for eligible products, order values, and
serviceable pincodes.

ElectroMart may restrict COD because of:

-   Product category.
-   Order value.
-   Destination pincode.
-   Courier availability.
-   Previous delivery failures.
-   Risk or fraud controls.

COD eligibility is determined at checkout and may change based on the
order.

A COD order normally requires payment to the delivery agent according to
the available courier process.

## Payment Status Rules

  -----------------------------------------------------------------------
  Payment status          Meaning                 Customer action
  ----------------------- ----------------------- -----------------------
  SUCCESS                 Payment has been        No additional payment
                          confirmed               is required

  FAILED                  Payment was not         Verify before
                          confirmed               attempting another
                                                  payment

  PENDING                 Payment result has not  Wait for status
                          been confirmed          resolution or contact
                                                  support

  REVERSED                Payment was reversed    Check order/payment
                          after authorization     status before retrying
  -----------------------------------------------------------------------

The agent must not claim that a payment succeeded solely because the
customer received a bank notification.

## Payment Failed but Money Was Deducted

If a customer reports that payment failed but money was deducted:

1.  Verify the order and payment transaction.
2.  Check whether the payment is `SUCCESS`, `PENDING`, `FAILED`, or
    `REVERSED`.
3.  Do not ask the customer to make another payment until the first
    transaction has been checked.
4.  If the payment is reversed or the gateway confirms failure, the
    amount may be returned according to the payment provider's
    processing cycle.
5.  Escalate when the payment remains unresolved beyond the expected
    processing period.

A customer should not be told that a refund has been issued unless the
refund or reversal is confirmed in the payment system.

## Duplicate Payment

If a customer believes the same order was charged twice:

-   Support must verify the payment transactions.
-   A duplicate authorization or temporary bank hold must not
    automatically be treated as a confirmed duplicate charge.
-   If two successful payments were actually collected for one order,
    the excess amount should be handled through the authorized refund
    process.

Support must use transaction records rather than relying only on
screenshots or customer descriptions.

## Payment Pending

A payment marked `PENDING` should not be treated as successful or failed
until the payment system resolves the transaction.

If the order remains unpaid after the payment result is resolved, the
customer may need to place the order again.

The customer should not be charged twice because support incorrectly
assumes that a pending transaction failed.

## Payment Security

ElectroMart support must never request:

-   Passwords.
-   OTPs.
-   UPI PINs.
-   CVVs.
-   Full card numbers.
-   Banking login credentials.

If a customer reports unauthorized payment activity, the case should be
escalated according to `escalation_rules.md` and the customer should be
advised to contact the relevant bank/payment provider where appropriate.

## Payment and Refund Relationship

A payment problem and a refund are different events.

-   A payment may fail without a refund being created.
-   A successful order cancellation may create a refund.
-   An approved product return may create a refund.
-   A payment reversal may occur without a standard return process.

Refund methods and timelines are defined in `returns_and_refunds.md`.

## Payment and Order Cancellation

For a prepaid order that is successfully cancelled before shipment, the
applicable refund is initiated through the refund process.

For COD orders cancelled before shipment, there is normally no payment
to refund.

The exact refund amount must come from the order/refund system.

## Payment-Related Edge Cases

### Payment failed but bank account was debited

Verify the payment transaction before asking the customer to retry. Do
not promise an immediate refund without confirmed payment-system
information.

### Customer paid twice

Verify whether both transactions were actually successful. If duplicate
collection is confirmed, the excess amount follows the authorized refund
process.

### Customer receives a bank notification but order is unpaid

The notification alone is not sufficient. Verify the payment status in
ElectroMart's payment system.

### Customer asks support for an OTP

Support must never request or provide OTPs.

### Customer wants to change the payment method after successful payment

A successful payment method cannot normally be changed for the existing
transaction. The available order/cancellation options must be checked.

## Related Policies

-   `returns_and_refunds.md` for refund methods and timelines.
-   `cancellation_and_replacement.md` for cancellation and
    cancellation-related refunds.
-   `account_and_security.md` for account and payment-security concerns.
-   `escalation_rules.md` for unresolved payment disputes and suspected
    fraud.

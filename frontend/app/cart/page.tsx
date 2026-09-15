"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useQueryClient } from "@tanstack/react-query";
import { ArrowLeft, Minus, Plus, ShoppingBag, Trash2, ArrowRight, MapPin, CreditCard, Loader2 } from "lucide-react";
import { useCart } from "@/lib/cart-provider";
import { useAuth } from "@/lib/auth-provider";
import { ordersApi } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ProductImage } from "@/components/ui/product-image";
import { useFeedback } from "@/components/ui/feedback";

export default function CartPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const { user } = useAuth();
  const { items, removeItem, updateQuantity, clearCart, subtotal, totalItems } = useCart();
  const { show } = useFeedback();

  const [shippingAddress, setShippingAddress] = useState(
    "Flat 402, Lotus Residency, Road No. 36, Jubilee Hills, Hyderabad, Telangana 500033"
  );
  const [paymentMethod, setPaymentMethod] = useState("UPI");
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleCheckout = async () => {
    if (!user) {
      show({
        message: "Please sign in to complete your order.",
        tone: "error",
      });
      router.push("/login");
      return;
    }

    if (items.length === 0) {
      show({
        message: "Your cart is empty.",
        tone: "error",
      });
      return;
    }

    if (!shippingAddress.trim()) {
      show({
        message: "Please enter a valid shipping address.",
        tone: "error",
      });
      return;
    }

    try {
      setIsSubmitting(true);
      const payload = {
        items: items.map((item) => ({
          product_id: item.product.id,
          quantity: item.quantity,
        })),
        shipping_address: shippingAddress.trim(),
        payment_method: paymentMethod,
      };

      const newOrder = await ordersApi.create(payload);

      show({
        message: `Order #${newOrder.order_number} placed successfully!`,
        tone: "success",
      });

      // Clear the cart
      clearCart();

      // Refresh cached orders list
      queryClient.invalidateQueries({ queryKey: ["orders", user.id] });

      // Navigate to the user's order details or orders list
      router.push(`/orders/${newOrder.order_number}`);
    } catch (error) {
      show({
        message: error instanceof Error ? error.message : "Failed to complete order. Please try again.",
        tone: "error",
      });
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="shell py-10">
      <Link
        href="/products"
        className="focus-ring inline-flex items-center gap-2 rounded text-sm font-semibold text-slate-500 hover:text-ink"
      >
        <ArrowLeft size={16} /> Continue shopping
      </Link>

      <div className="mt-6 flex items-center justify-between">
        <div>
          <p className="eyebrow">Checkout</p>
          <h1 className="mt-1 text-4xl font-extrabold tracking-tight">Your Cart</h1>
        </div>
        {items.length > 0 && (
          <button
            onClick={clearCart}
            className="text-sm font-semibold text-rose-600 hover:text-rose-700"
          >
            Clear all
          </button>
        )}
      </div>

      {items.length === 0 ? (
        <section className="mt-12 text-center">
          <div className="surface mx-auto max-w-md p-10">
            <span className="mx-auto grid h-16 w-16 place-items-center rounded-2xl bg-indigo-50 text-electric">
              <ShoppingBag size={28} />
            </span>
            <h2 className="mt-5 text-2xl font-extrabold">Your bag is empty</h2>
            <p className="mt-2 text-sm text-slate-500">
              Looks like you haven&apos;t added any items to your cart yet.
            </p>
            <Button href="/products" className="mt-6">
              Browse products
            </Button>
          </div>
        </section>
      ) : (
        <div className="mt-10 grid gap-8 lg:grid-cols-[1.5fr_1fr]">
          {/* Items List & Delivery Form */}
          <div className="space-y-6">
            <div className="space-y-4">
              {items.map(({ product, quantity }) => (
                <div
                  key={product.id}
                  className="surface flex flex-col gap-4 p-5 sm:flex-row sm:items-center sm:justify-between"
                >
                  <div className="flex items-center gap-4">
                    <ProductImage
                      product={product}
                      className="h-20 w-20 flex-shrink-0 rounded-2xl object-cover"
                    />
                    <div>
                      <span className="text-xs font-semibold text-electric uppercase">
                        {product.brand}
                      </span>
                      <h3 className="font-bold text-ink">
                        <Link
                          href={`/products/${product.id}`}
                          className="hover:text-electric"
                        >
                          {product.name}
                        </Link>
                      </h3>
                      <p className="text-sm font-semibold text-slate-600">
                        {formatCurrency(product.price)}
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center justify-between sm:justify-end gap-6">
                    {/* Quantity Stepper */}
                    <div className="flex items-center rounded-full border border-slate-200 bg-white p-1">
                      <button
                        onClick={() => updateQuantity(product.id, quantity - 1)}
                        aria-label="Decrease quantity"
                        className="grid h-7 w-7 place-items-center rounded-full text-slate-500 hover:bg-slate-100 hover:text-ink"
                      >
                        <Minus size={14} />
                      </button>
                      <span className="w-8 text-center text-sm font-semibold">
                        {quantity}
                      </span>
                      <button
                        onClick={() => updateQuantity(product.id, quantity + 1)}
                        aria-label="Increase quantity"
                        className="grid h-7 w-7 place-items-center rounded-full text-slate-500 hover:bg-slate-100 hover:text-ink"
                      >
                        <Plus size={14} />
                      </button>
                    </div>

                    <p className="min-w-20 text-right font-bold text-ink">
                      {formatCurrency(product.price * quantity)}
                    </p>

                    <button
                      onClick={() => removeItem(product.id)}
                      aria-label="Remove item"
                      className="text-slate-400 hover:text-rose-600"
                    >
                      <Trash2 size={18} />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            {/* Delivery Address & Payment Method */}
            <div className="surface p-6 space-y-6">
              <div>
                <div className="flex items-center gap-2 font-bold text-ink mb-3">
                  <MapPin size={18} className="text-electric" />
                  <span>Delivery Address</span>
                </div>
                <textarea
                  value={shippingAddress}
                  onChange={(e) => setShippingAddress(e.target.value)}
                  rows={2}
                  className="w-full rounded-xl border border-slate-200 bg-white p-3 text-sm focus:border-electric focus:outline-none"
                  placeholder="Enter full shipping address..."
                />
              </div>

              <div>
                <div className="flex items-center gap-2 font-bold text-ink mb-3">
                  <CreditCard size={18} className="text-electric" />
                  <span>Payment Method</span>
                </div>
                <div className="grid grid-cols-3 gap-3">
                  {[
                    { id: "UPI", label: "UPI" },
                    { id: "Credit Card", label: "Card" },
                    { id: "Cash on Delivery", label: "Cash on Delivery" },
                  ].map((m) => (
                    <button
                      key={m.id}
                      type="button"
                      onClick={() => setPaymentMethod(m.id)}
                      className={`rounded-xl border p-3 text-center text-xs font-bold transition ${
                        paymentMethod === m.id
                          ? "border-electric bg-indigo-50/50 text-electric shadow-sm"
                          : "border-slate-200 bg-white text-slate-600 hover:bg-slate-50"
                      }`}
                    >
                      {m.label}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Order Summary */}
          <div>
            <div className="surface sticky top-28 p-6">
              <h2 className="text-xl font-extrabold text-ink">Order Summary</h2>

              <div className="mt-6 space-y-3 text-sm">
                <div className="flex justify-between text-slate-600">
                  <span>Subtotal ({totalItems} items)</span>
                  <span className="font-semibold text-ink">{formatCurrency(subtotal)}</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>Standard Shipping</span>
                  <span className="font-semibold text-emerald-600">FREE</span>
                </div>
                <div className="flex justify-between text-slate-600">
                  <span>Estimated Tax</span>
                  <span className="font-semibold text-ink">{formatCurrency(0)}</span>
                </div>

                <div className="border-t border-slate-200 pt-3">
                  <div className="flex justify-between text-base font-extrabold text-ink">
                    <span>Total</span>
                    <span className="text-xl text-electric">{formatCurrency(subtotal)}</span>
                  </div>
                </div>
              </div>

              <div className="mt-6 space-y-3">
                <Button
                  onClick={handleCheckout}
                  disabled={isSubmitting}
                  className="w-full"
                >
                  {isSubmitting ? (
                    <>
                      <Loader2 size={16} className="animate-spin" /> Placing Order...
                    </>
                  ) : (
                    <>
                      Complete Order <ArrowRight size={16} />
                    </>
                  )}
                </Button>
                <Button href="/support" variant="secondary" className="w-full">
                  Ask AI Support about order
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

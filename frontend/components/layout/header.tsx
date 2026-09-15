"use client";

import Link from "next/link";
import { Bell, Menu, Search, ShoppingBag, UserRound, X } from "lucide-react";
import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/auth-provider";
import { useCart } from "@/lib/cart-provider";

const links = [
  { href: "/products", label: "Shop" },
  { href: "/products?category=Laptops", label: "Laptops" },
  { href: "/products?category=Audio", label: "Audio" },
  { href: "/support", label: "Support" },
];

export function Header() {
  const [open, setOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  const { user, ready } = useAuth();
  const { totalItems } = useCart();

  useEffect(() => {
    setMounted(true);
  }, []);

  const accountHref = mounted && user ? "/account" : "/login";
  const accountLabel = mounted && user ? "My account" : "Sign in";

  return (
    <header className="sticky top-0 z-50 border-b border-slate-200/70 bg-cloud/80 backdrop-blur-xl">
      <div className="shell flex h-20 items-center gap-4">
        <Link href="/" className="focus-ring mr-3 flex items-center gap-2 rounded-lg">
          <span className="grid h-9 w-9 place-items-center rounded-xl bg-electric font-black text-white shadow-glow">
            E
          </span>
          <span className="text-lg font-extrabold tracking-tight">
            Electro<span className="text-electric">Mart</span>
          </span>
        </Link>

        <nav className="hidden items-center gap-6 lg:flex">
          {links.map((link) => (
            <Link
              key={link.href}
              className="focus-ring rounded text-sm font-medium text-slate-600 transition hover:text-ink"
              href={link.href}
            >
              {link.label}
            </Link>
          ))}
        </nav>

        <div className="ml-auto hidden max-w-sm flex-1 items-center rounded-full bg-white px-4 py-2 ring-1 ring-slate-200 md:flex">
          <Search size={18} className="text-slate-400" />
          <input
            suppressHydrationWarning
            aria-label="Search products"
            className="w-full bg-transparent px-2 text-sm outline-none placeholder:text-slate-400"
            placeholder="Search headphones, TVs, laptops..."
          />
        </div>

        <div className="hidden items-center gap-1 sm:flex">
          <button
            suppressHydrationWarning
            aria-label="Notifications"
            className="focus-ring rounded-full p-2.5 text-slate-600 hover:bg-white"
          >
            <Bell size={19} />
          </button>
          <Link
            aria-label="Account"
            href={accountHref}
            className="focus-ring rounded-full p-2.5 text-slate-600 hover:bg-white"
          >
            <UserRound size={19} />
          </Link>
          <Link
            aria-label="Cart"
            href="/cart"
            className="focus-ring relative rounded-full p-2.5 text-slate-600 hover:bg-white"
          >
            <ShoppingBag size={19} />
            {mounted && totalItems > 0 ? (
              <span className="absolute -right-1 -top-1 grid h-5 min-w-5 place-items-center rounded-full bg-electric px-1 text-[11px] font-extrabold text-white shadow-sm">
                {totalItems}
              </span>
            ) : (
              <span className="absolute right-1 top-1 h-2 w-2 rounded-full bg-slate-300" />
            )}
          </Link>
          {mounted && ready && !user && (
            <Button href="/login" variant="ghost" className="ml-1 px-3 py-2">
              Sign in
            </Button>
          )}
        </div>

        <button
          suppressHydrationWarning
          aria-label="Open navigation"
          onClick={() => setOpen(!open)}
          className="focus-ring ml-auto rounded-full p-2 lg:hidden"
        >
          {open ? <X /> : <Menu />}
        </button>
      </div>

      {open && (
        <div className="shell border-t border-slate-200 py-4 lg:hidden">
          <nav className="grid gap-1">
            {links.map((link) => (
              <Link
                onClick={() => setOpen(false)}
                key={link.href}
                href={link.href}
                className="rounded-xl px-3 py-3 font-medium hover:bg-white"
              >
                {link.label}
              </Link>
            ))}
            <Link
              onClick={() => setOpen(false)}
              href="/cart"
              className="rounded-xl px-3 py-3 font-medium hover:bg-white flex items-center justify-between"
            >
              <span>Cart</span>
              {totalItems > 0 && (
                <span className="rounded-full bg-electric px-2 py-0.5 text-xs font-bold text-white">
                  {totalItems}
                </span>
              )}
            </Link>
            <Link
              href={accountHref}
              className="rounded-xl px-3 py-3 font-medium hover:bg-white"
            >
              {accountLabel}
            </Link>
            <Button href="/products" className="mt-2">
              Browse collection
            </Button>
          </nav>
        </div>
      )}
    </header>
  );
}

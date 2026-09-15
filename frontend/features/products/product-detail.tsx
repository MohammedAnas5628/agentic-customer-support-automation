"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { ArrowLeft } from "lucide-react";
import { productsApi } from "@/lib/api";
import { formatCurrency } from "@/lib/utils";
import { Button } from "@/components/ui/button";
import { ProductImage } from "@/components/ui/product-image";
import { ProductCard } from "./product-card";
import { useCart } from "@/lib/cart-provider";
import { useFeedback } from "@/components/ui/feedback";

export function ProductDetail({ id }: { id: string }) {
	const { data: product, isPending, isError } = useQuery({ queryKey: ["product", id], queryFn: () => productsApi.detail(id) });
	const { data: products } = useQuery({ queryKey: ["products"], queryFn: productsApi.list });
	const { addItem } = useCart();
	const { show } = useFeedback();

	const handleAddToCart = () => {
		if (!product) return;
		addItem(product);
		show({
			message: `Added ${product.name} to cart!`,
			tone: "success",
		});
	};

	if (isPending) return <div className="shell grid gap-10 pt-12 md:grid-cols-2"><div className="aspect-square animate-pulse rounded-4xl bg-slate-200" /><div className="space-y-5"><div className="h-5 w-24 animate-pulse rounded bg-slate-200" /><div className="h-12 animate-pulse rounded bg-slate-200" /></div></div>;
	if (isError || !product) return <section className="shell pt-16 text-center"><div className="surface mx-auto max-w-lg p-10"><h1 className="text-2xl font-extrabold">That product is out of reach.</h1><p className="mt-3 text-slate-500">It may no longer be available, or the ElectroMart service is offline.</p><Button href="/products" className="mt-6">Back to shop</Button></div></section>;

	const relatedProducts = products?.filter((item) => item.is_active && item.category === product.category && item.id !== product.id).slice(0, 4) ?? [];

	return <>
		<section className="shell pt-8"><Link href="/products" className="focus-ring inline-flex items-center gap-2 rounded text-sm font-semibold text-slate-500 hover:text-ink"><ArrowLeft size={16} /> All products</Link><div className="mt-8 grid gap-10 lg:grid-cols-2 lg:gap-16"><ProductImage product={product} className="aspect-square rounded-4xl" /><div className="py-3"><p className="eyebrow">{product.brand} · {product.category}</p><h1 className="mt-3 text-4xl font-extrabold tracking-tight sm:text-5xl">{product.name}</h1><p className="mt-5 text-3xl font-extrabold">{formatCurrency(product.price)}</p>{product.description && <p className="mt-6 max-w-xl leading-7 text-slate-600">{product.description}</p>}<p className="mt-5 text-sm text-slate-500">SKU: {product.sku}</p><p className="mt-2 text-sm font-medium text-emerald-600">{product.stock_quantity > 0 ? `${product.stock_quantity} available` : "Currently unavailable"}</p><div className="mt-8 flex flex-wrap gap-3"><Button onClick={handleAddToCart} className="min-w-44">Add to cart</Button><Button href="/support" variant="secondary">Ask a specialist</Button></div></div></div></section>
		{relatedProducts.length > 0 && <section className="shell mt-20 pb-16"><p className="eyebrow">From the same category</p><h2 className="mt-2 text-3xl font-extrabold tracking-tight">You may also like</h2><div className="mt-8 grid grid-cols-2 gap-4 md:grid-cols-4">{relatedProducts.map((item) => <ProductCard key={item.id} product={item} />)}</div></section>}
	</>;
}

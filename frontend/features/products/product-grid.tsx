"use client";
import { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { productsApi } from "@/lib/api";
import { ProductCard } from "./product-card";
import { catalogCategories, getDisplayCategory, getDisplaySubcategory, matchesCategory } from "@/lib/catalog";

type SortOrder = "featured" | "price-low" | "price-high" | "name";

export function ProductGrid({ limit }: { limit?: number }) {
	const { data, isPending, isError } = useQuery({ queryKey: ["products"], queryFn: productsApi.list });
	const [category, setCategory] = useState("");
	const [subcategory, setSubcategory] = useState("");
	const [search, setSearch] = useState("");
	const [sort, setSort] = useState<SortOrder>("featured");

	useEffect(() => {
		const params = new URLSearchParams(window.location.search);
		const requested = params.get("category") ?? "";
		const parent = catalogCategories.find((item) => item.name === requested);
		const child = catalogCategories.find((item) => item.subcategories.includes(requested as never));
		setCategory(parent?.name ?? child?.name ?? "");
		setSubcategory(child ? requested : "");
	}, []);

	if (isPending) return <div className="grid grid-cols-2 gap-4 lg:grid-cols-4">{Array.from({ length: limit ?? 4 }).map((_, i) => <div key={i} className="aspect-[3/4] animate-pulse rounded-3xl bg-slate-200" />)}</div>;
	if (isError) return <div className="surface p-8 text-center"><p className="font-bold">Products are taking a moment.</p><p className="mt-2 text-sm text-slate-500">Check that the ElectroMart API is running, then refresh the page.</p></div>;

	const activeProducts = data?.filter((product) => product.is_active) ?? [];
	const visibleProducts = activeProducts
		.filter((product) => matchesCategory(product, category || null, subcategory || null))
		.filter((product) => `${product.brand} ${product.name} ${product.category} ${product.description ?? ""}`.toLowerCase().includes(search.toLowerCase()))
		.sort((a, b) => sort === "price-low" ? a.price - b.price : sort === "price-high" ? b.price - a.price : sort === "name" ? a.name.localeCompare(b.name) : a.id - b.id)
		.slice(0, limit);

	if (!visibleProducts.length) return <div className="surface p-8 text-center text-slate-500"><p>No products match this view.</p><p className="mt-2 text-sm">Try another category or clear the search.</p></div>;

	return <>
		{!limit && <div className="surface mb-8 grid gap-4 p-4 md:grid-cols-[1.4fr_1fr_1fr_1fr]">
			<label className="flex items-center gap-3 rounded-2xl bg-slate-50 px-4 py-3 text-sm"><span className="font-semibold text-slate-500">Search</span><input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Brand or product name" className="min-w-0 flex-1 bg-transparent outline-none placeholder:text-slate-400" /></label>
			<select value={category} onChange={(event) => { setCategory(event.target.value); setSubcategory(""); }} className="rounded-2xl bg-slate-50 px-4 py-3 text-sm font-semibold outline-none"><option value="">All categories</option>{catalogCategories.map((item) => <option key={item.name}>{item.name}</option>)}</select>
			<select value={subcategory} onChange={(event) => setSubcategory(event.target.value)} disabled={!category} className="rounded-2xl bg-slate-50 px-4 py-3 text-sm font-semibold outline-none disabled:opacity-50"><option value="">All subcategories</option>{catalogCategories.find((item) => item.name === category)?.subcategories.map((item) => <option key={item}>{item}</option>)}</select>
			<select value={sort} onChange={(event) => setSort(event.target.value as SortOrder)} className="rounded-2xl bg-slate-50 px-4 py-3 text-sm font-semibold outline-none"><option value="featured">Featured order</option><option value="price-low">Price: low to high</option><option value="price-high">Price: high to low</option><option value="name">Name: A to Z</option></select>
		</div>}
		{!limit && <p className="mb-5 text-sm text-slate-500">{visibleProducts.length} product{visibleProducts.length === 1 ? "" : "s"} shown{category ? ` in ${category}` : ""}{subcategory ? ` / ${subcategory}` : ""}.</p>}
		<div className="grid grid-cols-2 gap-4 md:grid-cols-3 lg:grid-cols-4">{visibleProducts.map((product) => <ProductCard key={product.id} product={product} />)}</div>
	</>;
}

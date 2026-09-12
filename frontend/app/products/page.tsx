import { ProductGrid } from "@/features/products/product-grid";
export const metadata = { title: "Shop | ElectroMart" };
export default function ProductsPage() { return <section className="shell pt-12"><p className="eyebrow">The collection</p><h1 className="mt-2 text-4xl font-extrabold tracking-tight sm:text-5xl">Find your next favorite.</h1><p className="mt-4 max-w-xl text-slate-500">Purposeful technology selected for how you work, create, and unwind.</p><div className="mt-10"><ProductGrid /></div></section> }

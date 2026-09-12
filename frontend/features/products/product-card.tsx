"use client";
import Link from "next/link";
import { ArrowUpRight } from "lucide-react";
import { motion } from "framer-motion";
import type { Product } from "@/types/product";
import { formatCurrency } from "@/lib/utils";
import { ProductImage } from "@/components/ui/product-image";
import { getDisplaySubcategory } from "@/lib/catalog";
export function ProductCard({ product }: { product: Product }) { return <motion.article whileHover={{ y: -6 }} transition={{ duration: .2 }} className="group surface overflow-hidden"><Link href={`/products/${product.id}`}><div className="relative aspect-[4/3]"><ProductImage product={product} className="absolute inset-0" /><span className="absolute left-4 top-4 rounded-full bg-white/90 px-3 py-1 text-[11px] font-bold text-slate-600 backdrop-blur">{getDisplaySubcategory(product)}</span></div><div className="p-5"><p className="text-xs font-semibold uppercase tracking-wider text-slate-400">{product.brand}</p><h3 className="mt-1 line-clamp-1 text-base font-bold">{product.name}</h3><p className="mt-2 line-clamp-2 min-h-10 text-sm leading-5 text-slate-500">{product.description}</p><div className="mt-4 flex items-center justify-between"><p className="text-lg font-extrabold">{formatCurrency(product.price)}</p><span className="grid h-9 w-9 place-items-center rounded-full bg-slate-100 text-slate-700 transition group-hover:bg-electric group-hover:text-white"><ArrowUpRight size={17} /></span></div></div></Link></motion.article> }

"use client";

import Image from "next/image";
import { Box } from "lucide-react";
import { useState } from "react";
import type { Product } from "@/types/product";
import { getProductImage } from "@/lib/catalog";

export function ProductImage({ product, className = "" }: { product: Product; className?: string }) {
  const [failed, setFailed] = useState(false);
  const source = getProductImage(product);

  return (
    <div className={`relative h-full w-full overflow-hidden bg-gradient-to-br from-slate-100 via-white to-indigo-100 ${className}`}>
      {source && !failed ? (
        <Image
          src={source}
          alt={`${product.brand} ${product.name}`}
          fill
          sizes="(max-width: 768px) 50vw, (max-width: 1280px) 33vw, 25vw"
          className="object-cover transition duration-500 group-hover:scale-105"
          onError={() => setFailed(true)}
        />
      ) : (
        <div className="absolute inset-0 grid place-items-center text-electric/60" aria-label="Product image unavailable">
          <Box className="h-16 w-16" strokeWidth={1.2} />
        </div>
      )}
    </div>
  );
}

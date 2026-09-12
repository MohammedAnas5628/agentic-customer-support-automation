import type { Product } from "@/types/product";

export const catalogCategories = [
  { name: "Computing", description: "Laptops, Desktops, Accessories", subcategories: ["Laptops", "Desktops", "Computer Accessories"] },
  { name: "Mobiles", description: "Smartphones, Tablets, Accessories", subcategories: ["Smartphones", "Tablets", "Mobile Accessories"] },
  { name: "Audio", description: "Headphones, Earbuds, Speakers", subcategories: ["Headphones", "Earbuds", "Speakers", "Soundbars"] },
  { name: "Home Entertainment", description: "Smart TVs, Projectors, Streaming Devices", subcategories: ["Smart TVs", "Projectors", "Streaming Devices"] },
  { name: "Cameras", description: "DSLR, Mirrorless, Action Cameras", subcategories: ["DSLR", "Mirrorless", "Action Cameras", "Camera Accessories"] },
  { name: "Wearables", description: "Smartwatches, Fitness Bands", subcategories: ["Smartwatches", "Fitness Bands"] },
  { name: "Home Appliances", description: "Kitchen, Cleaning, Climate Control", subcategories: ["Kitchen Appliances", "Cleaning Appliances", "Climate Control"] },
  { name: "Accessories", description: "Chargers, Cables, Cases, Power", subcategories: ["Chargers", "Cables", "Cases", "Power Accessories"] },
] as const;

export type DisplayCategory = (typeof catalogCategories)[number]["name"];

export function getDisplayCategory(product: Product): DisplayCategory | null {
  if (product.category === "Laptops" || (product.category === "Accessories" && /keyboard|mouse/i.test(product.name))) return "Computing";
  if (product.category === "Smartphones" || product.category === "Tablets") return "Mobiles";
  if (product.category === "Headphones") return "Audio";
  if (product.category === "Smartwatches") return "Wearables";
  if (product.category === "Electronics" || product.category === "Gaming") return "Home Entertainment";
  if (product.category === "Accessories") return "Accessories";
  return null;
}

export function getDisplaySubcategory(product: Product): string {
  if (product.category === "Headphones") return /earbuds|airpods/i.test(product.name) ? "Earbuds" : "Headphones";
  if (product.category === "Electronics") return "Smart TVs";
  if (product.category === "Gaming") return "Streaming Devices";
  if (product.category === "Accessories" && /keyboard|mouse/i.test(product.name)) return "Computer Accessories";
  if (product.category === "Accessories" && /charger/i.test(product.name)) return "Chargers";
  if (product.category === "Accessories" && /cable/i.test(product.name)) return "Cables";
  return product.category;
}

export function matchesCategory(product: Product, category: string | null, subcategory: string | null) {
  if (category && getDisplayCategory(product) !== category) return false;
  if (subcategory && getDisplaySubcategory(product) !== subcategory) return false;
  return true;
}

export const PRODUCT_IMAGE_MAP = {
  "EM-PH-001": "/products/EM-PH-001.jpg",
  "EM-PH-002": "/products/EM-PH-002.jpg",
  "EM-PH-003": "/products/EM-PH-003.jpg",
  "EM-LT-001": "/products/EM-LT-001.jpg",
  "EM-LT-002": "/products/EM-LT-002.jpg",
  "EM-LT-003": "/products/EM-LT-003.jpg",
  "EM-TB-001": "/products/EM-TB-001.jpg",
  "EM-TB-002": "/products/EM-TB-002.jpg",
  "EM-AU-001": "/products/EM-AU-001.jpg",
  "EM-AU-002": "/products/EM-AU-002.jpg",
  "EM-SW-001": "/products/EM-SW-001.jpg",
  "EM-SW-002": "/products/EM-SW-002.jpg",
  "EM-GM-001": "/products/EM-GM-001.jpg",
  "EM-GM-002": "/products/EM-GM-002.jpg",
  "EM-AC-001": "/products/EM-AC-001.jpg",
  "EM-AC-002": "/products/EM-AC-002.jpg",
  "EM-AC-003": "/products/EM-AC-003.jpg",
  "EM-AC-004": "/products/EM-AC-004.jpg",
  "EM-TV-001": "/products/EM-TV-001.jpg",
  "EM-TV-002": "/products/EM-TV-002.jpg",
} as const;

const categoryImages: Record<DisplayCategory, string> = {
  Computing: PRODUCT_IMAGE_MAP["EM-LT-002"],
  Mobiles: PRODUCT_IMAGE_MAP["EM-PH-002"],
  Audio: PRODUCT_IMAGE_MAP["EM-AU-002"],
  "Home Entertainment": PRODUCT_IMAGE_MAP["EM-TV-001"],
  Cameras: "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=1200&q=85",
  Wearables: PRODUCT_IMAGE_MAP["EM-SW-001"],
  "Home Appliances": "https://images.unsplash.com/photo-1556911220-e15b29be8c8f?auto=format&fit=crop&w=1200&q=85",
  Accessories: PRODUCT_IMAGE_MAP["EM-AC-002"],
};

export function getProductImage(product: Product) {
  return PRODUCT_IMAGE_MAP[product.sku as keyof typeof PRODUCT_IMAGE_MAP];
};

export function getCategoryImage(category: DisplayCategory) {
  return categoryImages[category];
}

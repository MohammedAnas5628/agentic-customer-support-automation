"use client";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState } from "react";
import { AuthProvider } from "@/lib/auth-provider";
import { CartProvider } from "@/lib/cart-provider";
import { FeedbackProvider } from "@/components/ui/feedback";
export function QueryProvider({ children }: { children: React.ReactNode }) { const [client] = useState(() => new QueryClient({ defaultOptions: { queries: { staleTime: 60_000, retry: 1 } } })); return <QueryClientProvider client={client}><AuthProvider><CartProvider><FeedbackProvider>{children}</FeedbackProvider></CartProvider></AuthProvider></QueryClientProvider>; }

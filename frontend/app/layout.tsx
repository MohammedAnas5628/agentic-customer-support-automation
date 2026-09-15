import type { Metadata } from "next";
import "./globals.css";
import { QueryProvider } from "@/lib/query-provider";
import { Header } from "@/components/layout/header";
import { Footer } from "@/components/layout/footer";
export const metadata: Metadata = { title: "ElectroMart | Technology, thoughtfully chosen", description: "Premium electronics and support, all in one place." };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body suppressHydrationWarning>
        <QueryProvider>
          <Header />
          <main>{children}</main>
          <Footer />
        </QueryProvider>
      </body>
    </html>
  );
}

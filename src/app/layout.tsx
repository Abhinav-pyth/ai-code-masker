import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import TrustBanner from "@/components/TrustBanner";
import Sidebar from "@/components/Sidebar";
import { Toaster } from "@/components/ui/sonner";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Code Masker | Mask Sensitive Data in Code",
  description: "Protect API keys, credentials, and secrets before sharing code. Mask sensitive data instantly.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} h-screen bg-black text-zinc-100 flex overflow-hidden`}>
        <Sidebar />
        <div className="flex-grow flex flex-col overflow-y-auto">
          <TrustBanner />
          <main className="flex-grow relative">
            {children}
          </main>
        </div>
        <Toaster position="bottom-center" theme="dark" />
      </body>
    </html>
  );
}

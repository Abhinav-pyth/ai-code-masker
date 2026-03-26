import { ShieldCheck, Github, Lock } from "lucide-react";
import Link from "next/link";

export default function TrustBanner() {
  return (
    <div className="w-full bg-zinc-950 border-b border-zinc-900 py-3 px-4 flex flex-col sm:flex-row items-center justify-center sm:justify-between text-sm text-zinc-400">
      <div className="flex items-center gap-2 mb-2 sm:mb-0">
        <ShieldCheck className="h-4 w-4 text-emerald-500" />
        <span className="font-medium text-emerald-100">Secure by Design: We do NOT store your code.</span>
        <span className="hidden md:inline text-zinc-500">Processing is done completely on the fly.</span>
      </div>
      <div className="flex items-center gap-4">
        <Link href="/privacy-policy" className="flex items-center gap-1.5 hover:text-zinc-200 transition-colors">
          <Lock className="h-3.5 w-3.5" /> Privacy Policy
        </Link>
        <a href="https://github.com/" target="_blank" rel="noreferrer" className="flex items-center gap-1.5 hover:text-zinc-200 transition-colors">
          <Github className="h-3.5 w-3.5" /> Open Source
        </a>
      </div>
    </div>
  );
}

import MaskingEditor from "@/components/MaskingEditor";
import { ShieldAlert, Code2, Cpu, Zap, Lock, FileCode, CheckCircle } from "lucide-react";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center w-full">
      {/* Hero Section */}
      <section className="w-full max-w-6xl px-6 pt-24 pb-12 text-center flex flex-col items-center">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-sm font-medium mb-6 border border-emerald-500/20">
          <ShieldAlert className="w-4 h-4" />
          <span>v1.0 is Live: production-grade masking</span>
        </div>
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-6 text-transparent bg-clip-text bg-gradient-to-r from-zinc-100 to-zinc-500 leading-[1.1]">
          Mask Sensitive Data in<br className="hidden md:block"/> Code Instantly
        </h1>
        <p className="text-lg md:text-xl text-zinc-400 max-w-2xl mb-10 leading-relaxed">
          Protect API keys, JWT tokens, emails, and secrets before sharing your code with AI tools, 
          colleagues, or across the web. Completely private and instant.
        </p>
      </section>

      {/* Interactive Editor Section */}
      <section className="w-full max-w-7xl px-4 md:px-6 mb-24">
        <MaskingEditor />
      </section>

      {/* Features Section */}
      <section className="w-full max-w-6xl px-6 mb-24 grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="bg-zinc-950 p-8 rounded-2xl border border-zinc-900 flex flex-col items-start shadow-sm">
          <div className="bg-emerald-500/10 p-3 rounded-lg border border-emerald-500/20 mb-5">
            <Zap className="w-6 h-6 text-emerald-400" />
          </div>
          <h3 className="text-xl font-bold mb-3 text-zinc-100">Smart Detection</h3>
          <p className="text-zinc-400 leading-relaxed">
            Automatically identifies API keys, JWTs, emails, phone numbers, and common credentials utilizing fast Regex combinations.
          </p>
        </div>
        <div className="bg-zinc-950 p-8 rounded-2xl border border-zinc-900 flex flex-col items-start shadow-sm">
          <div className="bg-blue-500/10 p-3 rounded-lg border border-blue-500/20 mb-5">
            <Cpu className="w-6 h-6 text-blue-400" />
          </div>
          <h3 className="text-xl font-bold mb-3 text-zinc-100">AI-Ready Output</h3>
          <p className="text-zinc-400 leading-relaxed">
            Obfuscates variables while preserving structural integrity so LLMs and colleagues can still read your logic perfectly.
          </p>
        </div>
        <div className="bg-zinc-950 p-8 rounded-2xl border border-zinc-900 flex flex-col items-start shadow-sm">
          <div className="bg-purple-500/10 p-3 rounded-lg border border-purple-500/20 mb-5">
            <Lock className="w-6 h-6 text-purple-400" />
          </div>
          <h3 className="text-xl font-bold mb-3 text-zinc-100">Total Privacy</h3>
          <p className="text-zinc-400 leading-relaxed">
            Code isn't stored in our databases. The masking happens temporarily in serverless functions or on the client edge.
          </p>
        </div>
      </section>

      {/* Use Cases */}
      <section className="w-full bg-zinc-950 border-t border-b border-zinc-900 py-24">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <h2 className="text-3xl font-bold mb-12 text-zinc-100">Engineered for Developers</h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
            {[
              { title: "Share on StackOverflow", icon: Code2, desc: "Paste debugging logs completely safely." },
              { title: "Send Logs Safely", icon: FileCode, desc: "Strip customer emails from traces." },
              { title: "Debug Production", icon: Zap, desc: "Remove live DB tokens instantly." },
              { title: "Share GitHub Snippets", icon: CheckCircle, desc: "Contribute to OSS without fear." }
            ].map((uc, i) => (
              <div key={i} className="flex flex-col items-center bg-black p-6 rounded-xl border border-zinc-800">
                <uc.icon className="w-8 h-8 text-zinc-500 mb-4" />
                <h4 className="font-semibold text-zinc-200 mb-2">{uc.title}</h4>
                <p className="text-sm text-zinc-500">{uc.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="w-full max-w-6xl px-6 py-12 flex flex-col md:flex-row justify-between items-center text-sm text-zinc-500">
        <div className="flex items-center gap-2 mb-4 md:mb-0">
          <ShieldAlert className="w-5 h-5 text-emerald-500" />
          <span className="font-medium text-zinc-300">AI Code Masker</span>
          <span>© {new Date().getFullYear()}</span>
        </div>
        <div className="flex gap-6">
          <a href="/mask-api-keys-online" className="hover:text-zinc-300">Mask API Keys</a>
          <a href="/remove-sensitive-data-from-code" className="hover:text-zinc-300">Remove Secrets</a>
          <a href="/json-masker" className="hover:text-zinc-300">JSON Masker</a>
          <a href="/privacy-policy" className="hover:text-zinc-300">Privacy Policy</a>
        </div>
      </footer>
    </div>
  );
}

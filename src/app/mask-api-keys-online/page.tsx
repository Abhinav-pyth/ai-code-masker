import MaskingEditor from "@/components/MaskingEditor";
import { KeyRound, ShieldAlert } from "lucide-react";

export default function MaskApiKeysOnline() {
  return (
    <div className="flex flex-col items-center justify-center w-full px-4 py-12">
      <div className="max-w-4xl w-full text-center mb-10">
        <h1 className="text-3xl md:text-5xl font-bold tracking-tight mb-4 flex justify-center items-center gap-4">
          <KeyRound className="w-10 h-10 text-emerald-500" />
          Mask API Keys Online
        </h1>
        <p className="text-zinc-400 text-lg">
          Paste your code containing leaked API keys (OpenAI, AWS, Stripe) below. They will be instantly masked completely privately inside your browser without hitting our database.
        </p>
      </div>

      <div className="w-full max-w-7xl">
        <MaskingEditor />
      </div>
      
      <div className="max-w-4xl mt-12 bg-zinc-950 p-6 rounded-lg border border-zinc-900 shadow-sm text-left">
        <h2 className="text-xl font-bold text-zinc-200 mb-2 flex items-center gap-2">
          <ShieldAlert className="w-5 h-5 text-amber-500" /> Why mask API keys?
        </h2>
        <p className="text-zinc-400 text-sm leading-relaxed mb-4">
          Accidentally pushing or sharing an API key can lead to serious security breaches, huge financial damages, and compromised data. Use our AI Code Masker to sanitize the content before you post it online to seek debugging help. 
        </p>
        <p className="text-zinc-400 text-sm leading-relaxed">
          The code is completely stateless. We do not log inputs or outputs.
        </p>
      </div>
    </div>
  );
}

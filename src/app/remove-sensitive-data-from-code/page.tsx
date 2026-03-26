import MaskingEditor from "@/components/MaskingEditor";
import { FileCode2, ShieldAlert } from "lucide-react";

export default function RemoveSensitiveData() {
  return (
    <div className="flex flex-col items-center justify-center w-full px-4 py-12">
      <div className="max-w-4xl w-full text-center mb-10">
        <h1 className="text-3xl md:text-5xl font-bold tracking-tight mb-4 flex justify-center items-center gap-4">
          <FileCode2 className="w-10 h-10 text-blue-500" />
          Remove Sensitive Data from Code
        </h1>
        <p className="text-zinc-400 text-lg">
          Sanitize source code by removing passwords, phone numbers, PII, API tokens, and JWTs automatically before pushing to Git or sharing via ChatGPT.
        </p>
      </div>

      <div className="w-full max-w-7xl">
        <MaskingEditor />
      </div>
    </div>
  );
}

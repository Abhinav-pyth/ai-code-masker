import MaskingEditor from "@/components/MaskingEditor";
import { Braces } from "lucide-react";

export default function JSONMasker() {
  return (
    <div className="flex flex-col items-center justify-center w-full px-4 py-12">
      <div className="max-w-4xl w-full text-center mb-10">
        <h1 className="text-3xl md:text-5xl font-bold tracking-tight mb-4 flex justify-center items-center gap-4">
          <Braces className="w-10 h-10 text-purple-500" />
          JSON Object Sensitive Data Masker
        </h1>
        <p className="text-zinc-400 text-lg">
          Paste large JSON dumps or Webhooks containing PII and keys. The parser will immediately obliterate private credentials while keeping the JSON schema and structure completely intact.
        </p>
      </div>

      <div className="w-full max-w-7xl">
        <MaskingEditor />
      </div>
    </div>
  );
}

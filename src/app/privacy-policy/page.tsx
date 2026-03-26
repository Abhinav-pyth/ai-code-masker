import { ShieldCheck } from "lucide-react";

export default function PrivacyPolicy() {
  return (
    <div className="max-w-3xl mx-auto py-16 px-6">
      <div className="mb-10 flex gap-4 items-center">
        <ShieldCheck className="w-12 h-12 text-emerald-500" />
        <h1 className="text-4xl font-bold text-zinc-100">Privacy Policy</h1>
      </div>
      
      <div className="space-y-8 text-zinc-400">
        <section>
          <h2 className="text-2xl font-bold text-zinc-200 mb-4">1. Information Collection</h2>
          <p>
            The fundamental premise of AI Code Masker is privacy. We <strong>do not store</strong>, collect, 
            or log any source code, logs, or plain-text inputs that you process using our tool. All masking logic operates ephemerally.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-zinc-200 mb-4">2. Processing Architecture</h2>
          <p>
            When utilizing the web interface, text is sent to a stateless API endpoint (or executed locally depending on updates) that applies Regex and AI heuristics to mask strings. Once the text is returned to your browser, it is immediately discarded from server memory.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-zinc-200 mb-4">3. Security</h2>
          <p>
            Our architecture is designed to prevent data leaks. However, we advise you not to submit the absolute most critical, highly destructive, unprotected credentials arbitrarily, as internet transmission (HTTPS) still occurs. Treat the tool as an obfuscator before public posting. 
          </p>
        </section>
        
        <section>
          <h2 className="text-2xl font-bold text-zinc-200 mb-4">4. Open Source Transparency</h2>
          <p>
            We are fully open-source. You can review the exact masking paths and the API endpoints directly on GitHub. Feel free to clone the repository and run the instance solely on your local loopback address if absolute local isolation is required.
          </p>
        </section>
      </div>
    </div>
  );
}

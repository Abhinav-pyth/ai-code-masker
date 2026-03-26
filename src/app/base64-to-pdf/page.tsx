"use client";

import { useState, useRef, useEffect } from "react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { FileDown, Eye } from "lucide-react";

export default function Base64ToPdfPage() {
  const [base64Input, setBase64Input] = useState("");
  const [blobUrl, setBlobUrl] = useState<string | null>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  // Cleanup object URL when unmounting or changing
  useEffect(() => {
    return () => {
      if (blobUrl) URL.revokeObjectURL(blobUrl);
    };
  }, [blobUrl]);

  const stripDataUriPrefix = (str: string) => {
    return str.replace(/^data:[^;]+;base64,/i, '').trim();
  };

  const getPdfBlob = (b64: string) => {
    const raw = stripDataUriPrefix(b64);
    const byteChars = atob(raw);
    const byteNumbers = new Array(byteChars.length);
    for (let i = 0; i < byteChars.length; i++) {
      byteNumbers[i] = byteChars.charCodeAt(i);
    }
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: "application/pdf" });
  };

  const handlePreview = () => {
    if (!base64Input.trim()) {
      toast.error("Please input a Base64 string");
      return;
    }
    try {
      if (blobUrl) URL.revokeObjectURL(blobUrl);
      const blob = getPdfBlob(base64Input);
      const url = URL.createObjectURL(blob);
      setBlobUrl(url);
      toast.success("PDF Generated for preview");
    } catch (e: any) {
      toast.error("Error generating PDF: " + e.message);
    }
  };

  const handleDownload = () => {
    if (!base64Input.trim()) {
      toast.error("Please input a Base64 string");
      return;
    }
    try {
      const blob = getPdfBlob(base64Input);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "document.pdf";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      toast.success("Download started");
    } catch (e: any) {
      toast.error("Error downloading PDF: " + e.message);
    }
  };

  return (
    <div className="flex flex-col h-full w-full p-4 lg:p-8">
      {/* Toolbar */}
      <div className="h-16 border-b border-zinc-800 flex items-center justify-between px-6 bg-zinc-950 rounded-t-2xl shadow-sm">
        <h1 className="text-sm font-bold tracking-[0.15em] text-indigo-200 uppercase">
          BASE64 TO PDF
        </h1>
        <div className="flex gap-3">
          <Button variant="secondary" size="sm" onClick={handlePreview} className="bg-indigo-600 hover:bg-indigo-700 text-white border-0">
            <Eye className="w-4 h-4 mr-2" />
            Preview PDF
          </Button>
          <Button variant="outline" size="sm" onClick={handleDownload} className="text-indigo-300 border-indigo-900 hover:bg-indigo-950">
            <FileDown className="w-4 h-4 mr-2" />
            Download PDF
          </Button>
        </div>
      </div>

      {/* Two-column layout */}
      <div className="flex-grow grid grid-cols-1 lg:grid-cols-2 gap-8 pt-4">
        
        {/* Left: Base64 Input */}
        <div className="flex flex-col border border-zinc-800 rounded-2xl overflow-hidden shadow-lg bg-zinc-950">
          <div className="bg-zinc-900 border-b border-zinc-800 px-4 py-3 text-[10px] font-black text-indigo-400 uppercase tracking-widest">
            Base64 Input
          </div>
          <textarea
            value={base64Input}
            onChange={(e) => setBase64Input(e.target.value)}
            placeholder="Paste base64-encoded PDF here (with or without data:application/pdf;base64, prefix)..."
            className="flex-grow p-6 bg-transparent text-slate-300 text-sm font-mono outline-none resize-none custom-scrollbar leading-relaxed"
          ></textarea>
        </div>

        {/* Right: PDF Preview */}
        <div className="flex flex-col border border-zinc-800 rounded-2xl overflow-hidden shadow-lg bg-zinc-950">
          <div className="bg-zinc-900 border-b border-zinc-800 px-4 py-3 text-[10px] font-black text-indigo-400 uppercase tracking-widest">
            PDF Preview
          </div>
          <div className="flex-grow flex items-center justify-center p-4">
            {!blobUrl ? (
              <div className="w-full h-full flex items-center justify-center border border-dashed border-indigo-500/20 rounded-xl text-slate-500 text-sm">
                Paste base64 and click "Preview PDF"
              </div>
            ) : (
              <iframe
                ref={iframeRef}
                src={blobUrl}
                title="PDF Preview"
                className="w-full h-full rounded-xl bg-zinc-900 border-none"
              ></iframe>
            )}
          </div>
        </div>

      </div>
    </div>
  );
}

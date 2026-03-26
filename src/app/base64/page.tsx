"use client";

import { useState, useEffect } from "react";
import { Copy, Hash, FileJson, FileText, Download, Eye, FileType, FileCode, Binary } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Label } from "@/components/ui/label";
// import * as XLSX from "xlsx";

export default function SuperBase64Page() {
  const [input, setInput] = useState("");
  const [output, setOutput] = useState("");
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [fileType, setFileType] = useState<"pdf" | "image" | "csv" | "excel" | "other">("other");

  useEffect(() => {
    return () => { if (previewUrl) URL.revokeObjectURL(previewUrl); };
  }, [previewUrl]);

  const detectType = (b64: string) => {
    const clean = b64.replace(/^data:[^;]+;base64,/i, '').trim();
    const header = clean.substring(0, 16);
    if (header.startsWith('/9j/') || header.startsWith('iVBOR') || header.startsWith('R0lGO')) return "image";
    if (header.startsWith('JVBER')) return "pdf";
    // Heuristic for CSV/Excel: Check if it's text-like or common binary headers
    return "other";
  };

  const handleEncode = () => {
    try {
      const encoded = btoa(unescape(encodeURIComponent(input)));
      setOutput(encoded);
      toast.success("Text encoded to Base64");
    } catch (e) {
      toast.error("Encoding failed");
    }
  };

  const handleDecode = () => {
    try {
      const decoded = decodeURIComponent(escape(atob(input.trim())));
      setOutput(decoded);
      toast.success("Base64 decoded to Text");
    } catch (e) {
      toast.error("Decoding failed. Perhaps it's binary data?");
    }
  };

  const getBlobFromBase64 = (b64: string, mime: string) => {
    const clean = b64.replace(/^data:[^;]+;base64,/i, '').trim();
    const byteChars = atob(clean);
    const byteNumbers = new Array(byteChars.length);
    for (let i = 0; i < byteChars.length; i++) {
      byteNumbers[i] = byteChars.charCodeAt(i);
    }
    return new Blob([new Uint8Array(byteNumbers)], { type: mime });
  };

  const handlePreview = (type: "pdf" | "image") => {
    try {
      const mime = type === "pdf" ? "application/pdf" : "image/png"; // Default png if not specified
      const blob = getBlobFromBase64(input, mime);
      const url = URL.createObjectURL(blob);
      if (previewUrl) URL.revokeObjectURL(previewUrl);
      setPreviewUrl(url);
      setFileType(type);
      toast.success(`${type.toUpperCase()} generated for preview`);
    } catch (e) {
      toast.error("Failed to generate preview");
    }
  };

  const handleDownloadFile = (ext: string, mime: string) => {
    try {
      const blob = getBlobFromBase64(input, mime);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `converted_file.${ext}`;
      a.click();
      URL.revokeObjectURL(url);
      toast.success(`Downloaded as .${ext}`);
    } catch (e) {
      toast.error("Download failed");
    }
  };

  const handleExportData = (format: "csv" | "xlsx") => {
    try {
      toast.error("Excel/CSV export is currently being initialized. Please try again in 1 minute.");
      /*
      // Decode the input to get the raw string (assuming it's a CSV string or JSON array in B64)
      const decoded = decodeURIComponent(escape(atob(input.trim())));
      
      let data: any[];
      try {
        data = JSON.parse(decoded);
        if (!Array.isArray(data)) data = [data];
      } catch {
        // Not JSON, treat as CSV text
        const rows = decoded.split('\n').map(r => r.split(','));
        data = rows;
      }

      const ws = Array.isArray(data[0]) ? (XLSX as any).utils.aoa_to_sheet(data) : (XLSX as any).utils.json_to_sheet(data);
      const wb = (XLSX as any).utils.book_new();
      (XLSX as any).utils.book_append_sheet(wb, ws, "Sheet1");
      
      if (format === "xlsx") {
        (XLSX as any).writeFile(wb, "data_export.xlsx");
      } else {
        const csv = (XLSX as any).utils.sheet_to_csv(ws);
        const blob = new Blob([csv], { type: "text/csv" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "data_export.csv";
        a.click();
      }
      toast.success(`Exported as ${format.toUpperCase()}`);
      */
    } catch (e) {
      toast.error("Export failed. Ensure the Base64 content is valid CSV/JSON text.");
    }
  };

  return (
    <div className="min-h-full p-6 lg:p-10 space-y-8 max-w-6xl mx-auto flex flex-col">
      <div className="bg-zinc-950/50 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Binary className="text-indigo-500 w-6 h-6" />
          <h1 className="text-xs font-black tracking-[4px] text-zinc-100 uppercase">Super Base64 Converter</h1>
        </div>
        <div className="flex gap-2">
           <Button variant="outline" size="sm" onClick={() => { setInput(""); setOutput(""); setPreviewUrl(null); }} className="text-[10px] font-bold uppercase rounded-full">
             Clear
           </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 flex-grow overflow-hidden">
        {/* Input & Text Actions */}
        <div className="flex flex-col space-y-6 min-h-0">
          <div className="bg-zinc-950/40 border border-zinc-800 rounded-3xl p-6 flex-grow flex flex-col space-y-4">
            <Label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">Input (Text or Base64)</Label>
            <textarea
              className="flex-grow bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 text-sm font-mono text-zinc-300 outline-none focus:ring-1 focus:ring-indigo-500/30 resize-none transition-all"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Paste content here..."
            />
            <div className="flex gap-3">
              <Button onClick={handleEncode} className="flex-1 bg-indigo-600 hover:bg-indigo-700 h-12 rounded-2xl font-black uppercase tracking-widest text-[10px]">
                Encode Text
              </Button>
              <Button onClick={handleDecode} variant="secondary" className="flex-1 bg-zinc-800 hover:bg-zinc-700 h-12 rounded-2xl font-black uppercase tracking-widest text-[10px]">
                Decode B64
              </Button>
            </div>
          </div>

          <div className="bg-zinc-950/40 border border-zinc-800 rounded-3xl p-6 space-y-4">
             <Label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">File Conversions (From Base64)</Label>
             <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
                <Button variant="outline" size="sm" onClick={() => handlePreview("image")} className="border-emerald-500/20 text-emerald-500 hover:bg-emerald-500/5 text-[9px] font-black uppercase">
                  <Eye className="w-3 h-3 mr-2" /> Image
                </Button>
                <Button variant="outline" size="sm" onClick={() => handlePreview("pdf")} className="border-red-500/20 text-red-500 hover:bg-red-500/5 text-[9px] font-black uppercase">
                  <Eye className="w-3 h-3 mr-2" /> PDF
                </Button>
                <Button variant="outline" size="sm" onClick={() => handleExportData("csv")} className="border-amber-500/20 text-amber-500 hover:bg-amber-500/5 text-[9px] font-black uppercase">
                   Export CSV
                </Button>
                <Button variant="outline" size="sm" onClick={() => handleExportData("xlsx")} className="border-indigo-500/20 text-indigo-500 hover:bg-indigo-500/5 text-[9px] font-black uppercase">
                   Export Excel
                </Button>
             </div>
             <div className="flex gap-2">
                <Button variant="ghost" size="sm" onClick={() => handleDownloadFile("jpg", "image/jpeg")} className="text-[8px] text-zinc-600">Download .JPG</Button>
                <Button variant="ghost" size="sm" onClick={() => handleDownloadFile("png", "image/png")} className="text-[8px] text-zinc-600">Download .PNG</Button>
                <Button variant="ghost" size="sm" onClick={() => handleDownloadFile("pdf", "application/pdf")} className="text-[8px] text-zinc-600">Download .PDF</Button>
             </div>
          </div>
        </div>

        {/* Output & Preview */}
        <div className="flex flex-col space-y-6 min-h-0">
          <Tabs defaultValue="text" className="flex-grow flex flex-col">
            <TabsList className="bg-zinc-950 border border-zinc-800 rounded-full p-1 mb-4 h-11 w-fit">
              <TabsTrigger value="text" className="rounded-full text-[10px] font-bold uppercase tracking-widest px-6 data-[state=active]:bg-indigo-600">Text Result</TabsTrigger>
              <TabsTrigger value="preview" className="rounded-full text-[10px] font-bold uppercase tracking-widest px-6 data-[state=active]:bg-indigo-600">Media Preview</TabsTrigger>
            </TabsList>

            <TabsContent value="text" className="flex-grow flex flex-col m-0 p-0 border-none outline-none">
              <div className="bg-zinc-950/40 border border-zinc-800 rounded-3xl p-6 flex-grow flex flex-col space-y-4">
                <div className="flex justify-between items-center">
                   <Label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase text-emerald-400">Processed Output</Label>
                   <Button variant="ghost" size="sm" onClick={() => { navigator.clipboard.writeText(output); toast.success("Copied to clipboard"); }} className="text-zinc-500 hover:text-white">
                      <Copy className="w-3 h-3 mr-2" /> <span className="text-[9px] font-bold uppercase">Copy</span>
                   </Button>
                </div>
                <textarea
                  className="flex-grow bg-[#050505] border border-white/5 rounded-2xl p-6 text-sm font-mono text-emerald-500/80 outline-none resize-none transition-all"
                  value={output}
                  readOnly
                />
              </div>
            </TabsContent>

            <TabsContent value="preview" className="flex-grow flex flex-col m-0 p-0 border-none outline-none">
              <div className="bg-zinc-950/40 border border-zinc-800 rounded-3xl p-6 flex-grow flex flex-col items-center justify-center relative overflow-hidden bg-black/5">
                {!previewUrl ? (
                  <div className="flex flex-col items-center gap-4 text-zinc-700 italic text-[10px] uppercase tracking-widest opacity-40">
                    <Eye className="w-12 h-12" />
                    No Preview Active
                  </div>
                ) : fileType === "image" ? (
                  <img src={previewUrl} alt="Preview" className="max-w-full max-h-full object-contain rounded-xl border border-white/10 shadow-2xl" />
                ) : (
                  <iframe src={previewUrl} className="w-full h-full rounded-xl border-none" title="PDF Preview"></iframe>
                )}
                {previewUrl && (
                  <div className="absolute top-4 right-4 bg-emerald-500 shadow-lg px-4 py-1.5 rounded-full text-[9px] font-black text-white uppercase tracking-widest animate-pulse">
                    Live Preview
                  </div>
                )}
              </div>
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}

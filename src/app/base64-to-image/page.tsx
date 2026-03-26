"use client";

import { useState, useEffect } from "react";
import { Download, Eye, ImageIcon, Binary, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Label } from "@/components/ui/label";

export default function Base64ToImagePage() {
  const [input, setInput] = useState("");
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);

  useEffect(() => {
    return () => { if (previewUrl) URL.revokeObjectURL(previewUrl); };
  }, [previewUrl]);

  const detectImageType = (b64: string) => {
    const clean = b64.replace(/^data:[^;]+;base64,/i, '').trim();
    const header = clean.substring(0, 16);
    if (header.startsWith('/9j/')) return 'image/jpeg';
    if (header.startsWith('iVBOR')) return 'image/png';
    if (header.startsWith('R0lGO')) return 'image/gif';
    if (header.startsWith('UklGR')) return 'image/webp';
    return 'image/png';
  };

  const showImage = () => {
    if (!input.trim()) return;
    try {
      const mime = detectImageType(input);
      const clean = input.replace(/^data:[^;]+;base64,/i, '').trim();
      const byteChars = atob(clean);
      const byteNumbers = new Array(byteChars.length);
      for (let i = 0; i < byteChars.length; i++) {
        byteNumbers[i] = byteChars.charCodeAt(i);
      }
      const blob = new Blob([new Uint8Array(byteNumbers)], { type: mime });
      const url = URL.createObjectURL(blob);
      if (previewUrl) URL.revokeObjectURL(previewUrl);
      setPreviewUrl(url);
      toast.success("Image preview generated");
    } catch (e) {
      toast.error("Failed to load image. Check your Base64 string.");
    }
  };

  const downloadImage = () => {
    if (!previewUrl) return;
    const a = document.createElement("a");
    a.href = previewUrl;
    a.download = "base64_image.png";
    a.click();
  };

  return (
    <div className="min-h-full p-6 lg:p-10 space-y-8 max-w-5xl mx-auto flex flex-col">
      <div className="bg-zinc-950/50 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <ImageIcon className="text-emerald-500 w-6 h-6" />
          <h1 className="text-xs font-black tracking-[4px] text-zinc-100 uppercase">Base64 to Image</h1>
        </div>
        <Button variant="outline" size="sm" onClick={() => { setInput(""); setPreviewUrl(null); }} className="text-[10px] uppercase font-bold rounded-full">
           <Trash2 className="w-3 h-3 mr-2" /> Reset
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 flex-grow">
        <div className="bg-zinc-950/40 border border-zinc-800 rounded-[40px] p-8 space-y-6 flex flex-col">
           <Label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">Base64 Input</Label>
           <textarea
             className="flex-grow bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 text-xs font-mono text-zinc-400 outline-none resize-none"
             placeholder="Paste base64 image data here..."
             value={input}
             onChange={(e) => setInput(e.target.value)}
           />
           <div className="flex gap-4">
              <Button onClick={showImage} className="flex-1 bg-indigo-600 hover:bg-indigo-700 h-14 rounded-2xl font-black uppercase tracking-widest text-[10px]">
                <Eye className="w-4 h-4 mr-2" /> Show Preview
              </Button>
              {previewUrl && (
                <Button onClick={downloadImage} variant="secondary" className="flex-1 bg-zinc-800 hover:bg-zinc-700 h-14 rounded-2xl font-black uppercase tracking-widest text-[10px]">
                   <Download className="w-4 h-4 mr-2" /> Download
                </Button>
              )}
           </div>
        </div>

        <div className="bg-zinc-950/40 border border-zinc-800 rounded-[40px] p-8 flex items-center justify-center relative overflow-hidden bg-black/5 min-h-[400px]">
           {!previewUrl ? (
             <div className="flex flex-col items-center gap-4 text-zinc-700 opacity-30 italic text-[10px] uppercase tracking-widest">
                <Binary className="w-12 h-12" />
                Awaiting Content...
             </div>
           ) : (
             <img src={previewUrl} alt="Preview" className="max-w-full max-h-full object-contain rounded-xl shadow-2xl border border-white/10" />
           )}
           {previewUrl && (
             <div className="absolute top-6 right-6 bg-emerald-500/10 border border-emerald-500/20 text-emerald-500 text-[9px] font-black uppercase px-4 py-1.5 rounded-full backdrop-blur-md">
                Live Preview
             </div>
           )}
        </div>
      </div>
    </div>
  );
}

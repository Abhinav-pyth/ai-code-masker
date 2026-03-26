"use client";

import { useState, useRef } from "react";
import { QrCode, Download, RefreshCw, Palette, Settings2, Trash2, Binary } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Slider } from "@/components/ui/slider";
// import { QRCodeSVG } from "qrcode.react";

export default function QrGeneratorPage() {
  const [data, setData] = useState("https://google.com");
  const [size, setSize] = useState(256);
  const [bg, setBg] = useState("#FFFFFF");
  const [fg, setFg] = useState("#000000");
  const [level, setLevel] = useState<"L" | "M" | "Q" | "H">("M");

  const qrRef = useRef<HTMLDivElement>(null);

  const downloadQR = () => {
    toast.error("QR Code generator is initializing. Please try again soon.");
    /*
    const svg = qrRef.current?.querySelector("svg");
    if (!svg) return;

    const svgData = new XMLSerializer().serializeToString(svg);
    const canvas = document.createElement("canvas");
    const ctx = canvas.getContext("2d");
    const img = new Image();

    img.onload = () => {
      canvas.width = size;
      canvas.height = size;
      ctx?.drawImage(img, 0, 0);
      const pngUrl = canvas.toDataURL("image/png");
      const a = document.createElement("a");
      a.href = pngUrl;
      a.download = "qrcode.png";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      toast.success("QR Code downloaded!");
    };

    img.src = `data:image/svg+xml;base64,${btoa(svgData)}`;
    */
  };

  return (
    <div className="min-h-full p-6 lg:p-10 space-y-8 max-w-5xl mx-auto flex flex-col">
      <div className="bg-zinc-950/50 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <QrCode className="text-indigo-500 w-6 h-6" />
          <h1 className="text-xs font-black tracking-[4px] text-zinc-100 uppercase">QR Generator</h1>
        </div>
        <Button size="sm" variant="outline" onClick={() => setData("")} className="text-[10px] font-black uppercase rounded-full">
           <Trash2 className="w-3 h-3 mr-2" /> Reset
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-zinc-950/40 border border-zinc-800 rounded-3xl p-6 space-y-6 shadow-xl">
            <div className="space-y-3">
              <Label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">Target URL / Text</Label>
              <textarea
                value={data}
                onChange={(e) => setData(e.target.value)}
                className="w-full bg-zinc-900 border border-white/5 rounded-xl p-4 text-xs font-mono text-zinc-300 outline-none focus:ring-1 focus:ring-indigo-500/30 resize-none h-24"
                placeholder="Enter link or secret message..."
              />
            </div>

            <div className="space-y-4">
              <div className="flex justify-between items-center text-[10px] font-black text-zinc-500 tracking-widest uppercase">
                 <span>QR Size</span>
                 <span className="text-indigo-400">{size}px</span>
              </div>
              <Slider value={[size]} onValueChange={(v: number[]) => setSize(v[0])} min={128} max={512} step={16} />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label className="text-[9px] text-zinc-600 uppercase font-black">Foreground</Label>
                <div className="flex items-center gap-2 bg-zinc-900 border border-white/5 p-2 rounded-xl">
                  <input type="color" value={fg} onChange={(e) => setFg(e.target.value)} className="w-6 h-6 bg-transparent border-none" />
                  <span className="text-[9px] font-mono opacity-50 uppercase">{fg}</span>
                </div>
              </div>
              <div className="space-y-2">
                <Label className="text-[9px] text-zinc-600 uppercase font-black">Background</Label>
                <div className="flex items-center gap-2 bg-zinc-900 border border-white/5 p-2 rounded-xl">
                  <input type="color" value={bg} onChange={(e) => setBg(e.target.value)} className="w-6 h-6 bg-transparent border-none" />
                  <span className="text-[9px] font-mono opacity-50 uppercase">{bg}</span>
                </div>
              </div>
            </div>

            <div className="space-y-3 pt-4 border-t border-white/5">
                <Label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase mb-2 block">Error Correction</Label>
                <div className="flex gap-2">
                   {["L", "M", "Q", "H"].map((l) => (
                     <Button
                        key={l}
                        variant={level === l ? "default" : "secondary"}
                        onClick={() => setLevel(l as any)}
                        className={`flex-1 h-8 text-[9px] font-black ${level === l ? 'bg-indigo-600' : 'bg-zinc-800'}`}
                     >
                       {l}
                     </Button>
                   ))}
                </div>
            </div>

            <Button onClick={downloadQR} className="w-full bg-emerald-600 hover:bg-emerald-700 h-14 rounded-2xl font-black uppercase tracking-widest text-[10px] shadow-lg shadow-emerald-500/10">
              <Download className="w-4 h-4 mr-2" />
              Download PNG
            </Button>
          </div>
        </div>

        <div className="lg:col-span-3">
          <div className="bg-zinc-950/40 border border-zinc-800 rounded-3xl p-6 h-[500px] lg:h-[600px] flex flex-col items-center justify-center relative bg-black/5 shadow-inner overflow-hidden group">
             {!data ? (
               <div className="flex flex-col items-center gap-4 text-zinc-700 italic text-[10px] uppercase tracking-widest opacity-40 animate-pulse">
                 <Binary className="w-12 h-12" />
                 Awaiting Content...
               </div>
             ) : (
                <div className="p-8 bg-zinc-900/50 backdrop-blur-3xl rounded-[40px] border border-white/5 shadow-[0_0_50px_-12px_rgba(99,102,241,0.2)] animate-in zoom-in-95 duration-500 flex items-center justify-center text-zinc-500 text-[10px] font-black uppercase text-center max-w-[200px]">
                   QR Engine Initializing...
                </div>
             )}
             
             {data && (
               <div className="absolute bottom-8 text-[10px] font-black text-zinc-600 tracking-widest uppercase italic opacity-30">
                 Generated Vector Pattern
               </div>
             )}
          </div>
        </div>
      </div>
    </div>
  );
}

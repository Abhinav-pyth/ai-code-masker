"use client";

import { useState, useRef } from "react";
import { Copy, ImageIcon, Download, Palette, RefreshCw, Layers } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function ImageConverterPage() {
  const [loadedImage, setLoadedImage] = useState<HTMLImageElement | null>(null);
  const [convertedDataUrl, setConvertedDataUrl] = useState<string | null>(null);
  const [targetFormat, setTargetFormat] = useState("image/png");
  const [quality, setQuality] = useState(0.9);
  const [metadata, setMetadata] = useState<{ width: number; height: number; originalFormat: string; sizeKb: number }>({
    width: 0,
    height: 0,
    originalFormat: "-",
    sizeKb: 0
  });

  const canvasRef = useRef<HTMLCanvasElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (ev) => {
      const img = new Image();
      img.onload = () => {
        setLoadedImage(img);
        setMetadata({
          width: img.width,
          height: img.height,
          originalFormat: file.type || "unknown",
          sizeKb: Math.round(file.size / 1024)
        });
        setConvertedDataUrl(null);
      };
      img.src = ev.target?.result as string;
    };
    reader.readAsDataURL(file);
  };

  const convertImage = () => {
    if (!loadedImage || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    canvas.width = loadedImage.width;
    canvas.height = loadedImage.height;

    // Background for JPEGs
    if (targetFormat === "image/jpeg") {
      ctx.fillStyle = "#ffffff";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
    }

    ctx.drawImage(loadedImage, 0, 0);
    const dataUrl = canvas.toDataURL(targetFormat, quality);
    setConvertedDataUrl(dataUrl);
    toast.success("Image converted!");
  };

  const downloadImage = () => {
    if (!convertedDataUrl) return;
    const ext = targetFormat.split("/")[1].replace("jpeg", "jpg");
    const a = document.createElement("a");
    a.href = convertedDataUrl;
    a.download = `converted_image.${ext}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="min-h-full p-6 lg:p-10 space-y-8 max-w-5xl mx-auto">
      <div className="bg-zinc-950/50 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <ImageIcon className="text-emerald-500 w-6 h-6" />
          <h1 className="text-xs font-black tracking-[4px] text-zinc-100 uppercase">Image Converter</h1>
        </div>
        {metadata.width > 0 && (
          <div className="text-[10px] font-mono font-bold text-zinc-500 uppercase tracking-widest bg-zinc-900 px-3 py-1 rounded-full">
            {metadata.width} × {metadata.height} PX
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        {/* Left Control Panel */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-zinc-950/40 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 space-y-6 shadow-sm">
            <div className="space-y-3">
              <Label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">Upload Source</Label>
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileUpload}
                accept="image/*"
                className="hidden"
              />
              <Button
                variant="outline"
                className="w-full h-16 border-dashed border-zinc-700 hover:border-emerald-500/50 hover:bg-emerald-500/5 transition-all rounded-2xl group"
                onClick={() => fileInputRef.current?.click()}
              >
                <div className="flex flex-col items-center">
                  <span className="text-sm font-semibold group-hover:text-emerald-400">Select Image</span>
                  <span className="text-[9px] text-zinc-600 uppercase mt-0.5">JPG, PNG, WebP, BMP</span>
                </div>
              </Button>
            </div>

            {loadedImage && (
              <div className="space-y-6 pt-4 border-t border-white/5 animate-in fade-in duration-500">
                <div className="space-y-3">
                  <Label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">Target Format</Label>
                  <Select value={targetFormat} onValueChange={setTargetFormat}>
                    <SelectTrigger className="bg-zinc-900 border-zinc-800 rounded-xl h-12 text-sm">
                      <SelectValue placeholder="Format" />
                    </SelectTrigger>
                    <SelectContent className="bg-zinc-900 border-zinc-800 text-zinc-300">
                      <SelectItem value="image/png">PNG</SelectItem>
                      <SelectItem value="image/jpeg">JPEG</SelectItem>
                      <SelectItem value="image/webp">WebP</SelectItem>
                      <SelectItem value="image/bmp">BMP</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {(targetFormat === "image/jpeg" || targetFormat === "image/webp") && (
                  <div className="space-y-4">
                    <div className="flex justify-between items-center text-[10px] font-black text-zinc-500 tracking-widest uppercase">
                      <span>Quality</span>
                      <span className="text-emerald-500">{Math.round(quality * 100)}%</span>
                    </div>
                    <Slider
                      value={[quality * 100]}
                      onValueChange={(val) => setQuality(val[0] / 100)}
                      min={10}
                      max={100}
                      step={1}
                      className="py-2"
                    />
                  </div>
                )}

                <div className="flex gap-3">
                  <Button onClick={convertImage} className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-xs font-black uppercase tracking-widest h-12 rounded-2xl shadow-lg shadow-emerald-500/10">
                    <RefreshCw className="w-4 h-4 mr-2" />
                    Convert
                  </Button>
                  {convertedDataUrl && (
                    <Button onClick={downloadImage} variant="secondary" className="bg-zinc-800 hover:bg-zinc-700 text-xs font-black uppercase tracking-widest h-12 rounded-2xl">
                      <Download className="w-4 h-4" />
                    </Button>
                  )}
                </div>
              </div>
            )}
          </div>

          {metadata.width > 0 && (
            <div className="bg-zinc-950/40 border border-zinc-800 rounded-3xl p-6 space-y-4">
               <Label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase block">Original Info</Label>
               <div className="grid grid-cols-2 gap-4">
                  <div className="bg-zinc-900/50 p-3 rounded-xl border border-white/5">
                    <div className="text-[8px] text-zinc-600 uppercase font-black tracking-widest mb-1">Format</div>
                    <div className="text-[10px] font-mono font-bold text-zinc-400 capitalize">{metadata.originalFormat.split("/")[1] || "-"}</div>
                  </div>
                  <div className="bg-zinc-900/50 p-3 rounded-xl border border-white/5">
                    <div className="text-[8px] text-zinc-600 uppercase font-black tracking-widest mb-1">Size</div>
                    <div className="text-[10px] font-mono font-bold text-zinc-400">{metadata.sizeKb} KB</div>
                  </div>
               </div>
            </div>
          )}
        </div>

        {/* Right Preview Panel */}
        <div className="lg:col-span-2 space-y-6">
          <div className="bg-zinc-950/40 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 h-[600px] flex flex-col items-center justify-center relative overflow-hidden group shadow-inner">
             {!loadedImage && !convertedDataUrl ? (
               <div className="flex flex-col items-center text-zinc-600 space-y-4 animate-in fade-in duration-1000">
                  <Layers className="w-12 h-12 opacity-20" />
                  <p className="text-xs font-medium tracking-widest uppercase italic bg-zinc-900/50 px-6 py-2 rounded-full border border-white/5">Awaiting Image...</p>
               </div>
             ) : (
               <div className="flex-grow w-full flex items-center justify-center p-4">
                  <img
                    src={convertedDataUrl || loadedImage?.src}
                    alt="Preview"
                    className="max-w-full max-h-full object-contain rounded-xl shadow-2xl border border-white/10"
                  />
               </div>
             )}
             
             {convertedDataUrl && (
               <div className="absolute top-6 right-6 flex items-center gap-2">
                 <div className="bg-emerald-500/10 backdrop-blur-md px-4 py-1.5 rounded-full border border-emerald-500/20 text-[9px] font-black text-emerald-400 uppercase tracking-widest animate-in slide-in-from-right duration-300">
                   Converted Preview
                 </div>
               </div>
             )}
          </div>
        </div>
      </div>
      <canvas ref={canvasRef} className="hidden" />
    </div>
  );
}

"use client";

import { useState, useRef, useEffect } from "react";
import { Move, Maximize, Save, Trash2, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Slider } from "@/components/ui/slider";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";

export default function ImageResizePage() {
  const [loadedImage, setLoadedImage] = useState<HTMLImageElement | null>(null);
  const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
  const [targetDims, setTargetDims] = useState({ width: 0, height: 0 });
  const [linkAspect, setLinkAspect] = useState(true);
  const [scale, setScale] = useState(1);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = (ev) => {
      const img = new Image();
      img.onload = () => {
        setLoadedImage(img);
        setDimensions({ width: img.width, height: img.height });
        setTargetDims({ width: img.width, height: img.height });
        setScale(1);
      };
      img.src = ev.target?.result as string;
    };
    reader.readAsDataURL(file);
  };

  const handleWidthChange = (val: string) => {
    const w = parseInt(val) || 0;
    const h = linkAspect ? Math.round(w * (dimensions.height / dimensions.width)) : targetDims.height;
    setTargetDims({ width: w, height: h });
    setScale(w / dimensions.width);
  };

  const handleHeightChange = (val: string) => {
    const h = parseInt(val) || 0;
    const w = linkAspect ? Math.round(h * (dimensions.width / dimensions.height)) : targetDims.width;
    setTargetDims({ width: w, height: h });
    setScale(h / dimensions.height);
  };

  const handleScaleChange = (val: number) => {
    const s = val / 100;
    setScale(s);
    setTargetDims({
      width: Math.round(dimensions.width * s),
      height: Math.round(dimensions.height * s)
    });
  };

  const resizeAndDownload = () => {
    if (!loadedImage || !canvasRef.current) return;
    const canvas = canvasRef.current;
    canvas.width = targetDims.width;
    canvas.height = targetDims.height;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    ctx.imageSmoothingEnabled = true;
    ctx.imageSmoothingQuality = "high";
    ctx.drawImage(loadedImage, 0, 0, targetDims.width, targetDims.height);

    const dataUrl = canvas.toDataURL("image/png");
    const a = document.createElement("a");
    a.href = dataUrl;
    a.download = `resized_${targetDims.width}x${targetDims.height}.png`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    toast.success("Image resized and downloaded!");
  };

  return (
    <div className="min-h-full p-6 lg:p-10 space-y-8 max-w-5xl mx-auto">
      <div className="bg-zinc-950/50 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Maximize className="text-indigo-500 w-6 h-6" />
          <h1 className="text-xs font-black tracking-[4px] text-zinc-100 uppercase">Image Resizer</h1>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 items-start">
        <div className="col-span-1 space-y-6">
          <div className="bg-zinc-950/40 border border-zinc-800 rounded-3xl p-6 space-y-6">
            <div className="space-y-3">
              <Label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">Input</Label>
              <input type="file" ref={fileInputRef} onChange={handleFileUpload} accept="image/*" className="hidden" />
              <Button
                variant="outline"
                className="w-full h-16 border-dashed border-zinc-700 hover:border-indigo-500/50 hover:bg-indigo-500/5 transition-all rounded-2xl"
                onClick={() => fileInputRef.current?.click()}
              >
                {loadedImage ? "Change Image" : "Upload Image"}
              </Button>
            </div>

            {loadedImage && (
              <div className="space-y-6 animate-in slide-in-from-top duration-500">
                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-2">
                    <Label className="text-[9px] text-zinc-600 uppercase font-black">Width (PX)</Label>
                    <Input
                      type="number"
                      value={targetDims.width}
                      onChange={(e) => handleWidthChange(e.target.value)}
                      className="bg-zinc-900 border-zinc-800 rounded-xl"
                    />
                  </div>
                  <div className="space-y-2">
                    <Label className="text-[9px] text-zinc-600 uppercase font-black">Height (PX)</Label>
                    <Input
                      type="number"
                      value={targetDims.height}
                      onChange={(e) => handleHeightChange(e.target.value)}
                      className="bg-zinc-900 border-zinc-800 rounded-xl"
                    />
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                     <Label className="text-[9px] text-zinc-600 uppercase font-black">Scaling %</Label>
                     <span className="text-xs font-mono text-indigo-400 font-bold">{Math.round(scale * 100)}%</span>
                  </div>
                  <Slider
                    value={[scale * 100]}
                    onValueChange={(val) => handleScaleChange(val[0])}
                    min={1}
                    max={300}
                    step={1}
                  />
                </div>

                <div className="flex items-center space-x-2 bg-zinc-900/50 p-3 rounded-xl border border-white/5">
                  <input
                    type="checkbox"
                    id="aspect"
                    checked={linkAspect}
                    onChange={(e) => setLinkAspect(e.target.checked)}
                    className="accent-indigo-500 w-4 h-4 rounded-sm"
                  />
                  <Label htmlFor="aspect" className="text-xs font-medium text-zinc-400">Lock Aspect Ratio</Label>
                </div>

                <Button onClick={resizeAndDownload} className="w-full bg-indigo-600 hover:bg-indigo-700 h-12 rounded-2xl font-black uppercase tracking-widest text-[10px]">
                  <Save className="w-4 h-4 mr-2" />
                  Save & Download
                </Button>
              </div>
            )}
          </div>
        </div>

        <div className="col-span-2 space-y-6">
           <div className="bg-zinc-950/40 border border-zinc-800 rounded-3xl p-6 h-[600px] flex flex-col items-center justify-center bg-black/5 relative shadow-inner overflow-hidden">
             {!loadedImage ? (
               <div className="text-zinc-600 italic text-xs uppercase tracking-widest opacity-30 flex flex-col items-center gap-4">
                 <Move className="w-12 h-12" />
                 Ready to Resize
               </div>
             ) : (
               <div className="w-full h-full p-4 flex items-center justify-center relative">
                  <div className="absolute top-4 left-4 z-10 bg-black/60 backdrop-blur-md px-3 py-1 rounded-full text-[9px] font-mono text-zinc-500 border border-white/10 uppercase">
                    {dimensions.width}×{dimensions.height}
                    <ArrowRight className="inline w-3 h-3 mx-1" />
                    <span className="text-emerald-400">{targetDims.width}×{targetDims.height}</span>
                  </div>
                  <img
                    src={loadedImage.src}
                    alt="Preview"
                    className="max-h-full max-w-full object-contain rounded-xl border border-white/10 shadow-2xl transition-all duration-300"
                    style={{ width: `${scale * 100}%` }}
                  />
               </div>
             )}
           </div>
        </div>
      </div>
      <canvas ref={canvasRef} className="hidden" />
    </div>
  );
}

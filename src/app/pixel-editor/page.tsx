"use client";

import { useState, useRef, useEffect } from "react";
import { Grid3X3, Eraser, Paintbrush, Download, Trash2, Palette, Square } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Slider } from "@/components/ui/slider";

const COLORS = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF", "#6366F1", "#10B981"];

export default function PixelEditorPage() {
  const [gridSize, setGridSize] = useState(16);
  const [color, setColor] = useState("#6366F1");
  const [isDrawing, setIsDrawing] = useState(false);
  const [pixels, setPixels] = useState<Record<string, string>>({});

  const containerRef = useRef<HTMLDivElement>(null);

  const clear = () => {
    setPixels({});
    toast.success("Canvas cleared");
  };

  const handlePixelAction = (x: number, y: number, erase = false) => {
    const key = `${x}-${y}`;
    if (erase) {
      const newPixels = { ...pixels };
      delete newPixels[key];
      setPixels(newPixels);
    } else {
      setPixels({ ...pixels, [key]: color });
    }
  };

  const downloadPixelArt = () => {
    const canvas = document.createElement("canvas");
    const outputSize = 512;
    const pxSize = outputSize / gridSize;
    canvas.width = outputSize;
    canvas.height = outputSize;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // Background transparancy mock
    ctx.clearRect(0, 0, outputSize, outputSize);

    Object.entries(pixels).forEach(([key, color]) => {
      const [x, y] = key.split("-").map(Number);
      ctx.fillStyle = color;
      ctx.fillRect(x * pxSize, y * pxSize, pxSize, pxSize);
    });

    const url = canvas.toDataURL("image/png");
    const a = document.createElement("a");
    a.href = url;
    a.download = "pixel-art.png";
    a.click();
    toast.success("Pixel art downloaded!");
  };

  return (
    <div className="min-h-full p-6 lg:p-10 space-y-8 max-w-5xl mx-auto flex flex-col">
      <div className="bg-zinc-950/50 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Grid3X3 className="text-indigo-500 w-6 h-6" />
          <h1 className="text-xs font-black tracking-[4px] text-zinc-100 uppercase">Pixel Editor</h1>
        </div>
        <div className="flex gap-2">
           <Button variant="outline" size="sm" onClick={clear} className="text-[10px] font-bold uppercase rounded-full">
             <Trash2 className="w-3 h-3 mr-2" /> Clear
           </Button>
           <Button onClick={downloadPixelArt} size="sm" className="bg-emerald-600 hover:bg-emerald-700 text-[10px] font-bold uppercase rounded-full">
             <Download className="w-3 h-3 mr-2" /> Export
           </Button>
        </div>
      </div>

      <div className="flex-grow grid grid-cols-1 lg:grid-cols-4 gap-8">
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-zinc-950/40 border border-zinc-800 rounded-3xl p-6 space-y-8 shadow-lg">
            <div className="space-y-4">
              <label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">Grid Density</label>
              <div className="flex justify-between items-center font-mono text-zinc-400 text-xs">
                 <span>{gridSize}×{gridSize}</span>
              </div>
              <Slider
                value={[gridSize]}
                onValueChange={(v) => { setGridSize(v[0]); setPixels({}); }}
                min={8}
                max={64}
                step={8}
              />
            </div>

            <div className="space-y-4">
              <label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">Palette</label>
              <div className="flex flex-wrap gap-2">
                {COLORS.map((c) => (
                  <button
                    key={c}
                    className={`w-7 h-7 rounded-sm border ${color === c ? 'border-white ring-2 ring-indigo-500/50 ring-offset-2 ring-offset-black' : 'border-white/5 opacity-80 hover:opacity-100 transition-all'}`}
                    style={{ backgroundColor: c }}
                    onClick={() => setColor(c)}
                  />
                ))}
              </div>
              <div className="flex items-center gap-3 pt-2">
                 <div className="w-10 h-10 rounded-lg border border-white/10 p-1 bg-zinc-900">
                    <input type="color" value={color} onChange={(e) => setColor(e.target.value)} className="w-full h-full bg-transparent cursor-crosshair border-none" />
                 </div>
                 <div className="text-[10px] font-mono font-bold text-zinc-500 uppercase">{color}</div>
              </div>
            </div>

            <div className="pt-4 space-y-2 border-t border-white/5">
               <div className="text-[8px] text-zinc-600 font-black uppercase mb-2">Instructions</div>
               <p className="text-[10px] text-zinc-500 leading-relaxed italic">
                 Click or drag to paint. <br/>
                 Right-click to erase.
               </p>
            </div>
          </div>
        </div>

        <div className="lg:col-span-3">
          <div 
            className="aspect-square w-full max-w-[600px] mx-auto bg-[#0a0a0a] border border-white/10 rounded-xl overflow-hidden shadow-2xl cursor-crosshair select-none"
            onMouseDown={() => setIsDrawing(true)}
            onMouseUp={() => setIsDrawing(false)}
            onMouseLeave={() => setIsDrawing(false)}
            onContextMenu={(e) => e.preventDefault()}
          >
            <div 
              className="grid h-full w-full" 
              style={{ gridTemplateColumns: `repeat(${gridSize}, 1fr)` }}
            >
              {Array.from({ length: gridSize * gridSize }).map((_, i) => {
                const x = i % gridSize;
                const y = Math.floor(i / gridSize);
                const key = `${x}-${y}`;
                const pxColor = pixels[key];
                
                return (
                  <div
                    key={i}
                    className={`border-[0.5px] border-zinc-900/40 relative group transition-colors duration-75`}
                    style={{ backgroundColor: pxColor || "transparent" }}
                    onMouseDown={(e) => handlePixelAction(x, y, e.button === 2)}
                    onMouseEnter={() => isDrawing && handlePixelAction(x, y)}
                  >
                     {!pxColor && <div className="absolute inset-0 bg-white/5 opacity-0 group-hover:opacity-100 transition-opacity" />}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

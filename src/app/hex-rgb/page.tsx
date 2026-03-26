"use client";

import { useState, useEffect } from "react";
import { Copy, Hash, Palette } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";

export default function HexRgbPage() {
  const [hex, setHex] = useState("6366F1");
  const [rgb, setRgb] = useState({ r: 99, g: 102, b: 241 });
  const [hsl, setHsl] = useState({ h: 239, s: 84, l: 67 });

  const clamp = (v: number) => Math.min(255, Math.max(0, v));

  const rgbToHsl = (r: number, g: number, b: number) => {
    r /= 255; g /= 255; b /= 255;
    const max = Math.max(r, g, b), min = Math.min(r, g, b);
    let h = 0, s, l = (max + min) / 2;
    if (max === min) {
      h = s = 0;
    } else {
      const d = max - min;
      s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
      switch (max) {
        case r: h = ((g - b) / d + (g < b ? 6 : 0)) / 6; break;
        case g: h = ((b - r) / d + 2) / 6; break;
        case b: h = ((r - g) / d + 4) / 6; break;
      }
    }
    return { h: Math.round(h * 360), s: Math.round(s * 100), l: Math.round(l * 100) };
  };

  const handleHexChange = (val: string) => {
    const cleanHex = val.replace(/[^0-9a-fA-F]/g, "").substring(0, 6);
    setHex(cleanHex.toUpperCase());
    if (cleanHex.length === 6) {
      const r = parseInt(cleanHex.substring(0, 2), 16);
      const g = parseInt(cleanHex.substring(2, 4), 16);
      const b = parseInt(cleanHex.substring(4, 6), 16);
      setRgb({ r, g, b });
      setHsl(rgbToHsl(r, g, b));
    }
  };

  const handleRgbChange = (part: keyof typeof rgb, val: string) => {
    const num = clamp(parseInt(val) || 0);
    const newRgb = { ...rgb, [part]: num };
    setRgb(newRgb);
    const newHex = [newRgb.r, newRgb.g, newRgb.b].map(v => v.toString(16).padStart(2, "0")).join("").toUpperCase();
    setHex(newHex);
    setHsl(rgbToHsl(newRgb.r, newRgb.g, newRgb.b));
  };

  const copy = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast.success(`${label} copied!`);
  };

  return (
    <div className="min-h-full p-4 lg:p-10 space-y-8 bg-black/10">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="bg-zinc-950/50 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 flex items-center gap-4">
          <Palette className="text-indigo-500 w-6 h-6" />
          <h1 className="text-xs font-black tracking-[4px] text-zinc-100 uppercase">Hex / RGB Converter</h1>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
          <div className="bg-zinc-950/40 backdrop-blur-xl border border-zinc-800 rounded-3xl p-8 space-y-8">
            <div className="space-y-3">
              <label className="text-[10px] font-black text-indigo-400 tracking-widest uppercase flex items-center gap-2">
                <Hash className="w-3 h-3" /> Hex Color
              </label>
              <div className="flex items-center gap-4">
                <span className="text-2xl font-mono text-indigo-500">#</span>
                <input
                  type="text"
                  value={hex}
                  onChange={(e) => handleHexChange(e.target.value)}
                  className="bg-transparent text-3xl font-mono font-bold text-white outline-none w-full tracking-widest"
                  placeholder="RRGGBB"
                />
              </div>
            </div>

            <div className="space-y-3">
              <label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">RGB Values</label>
              <div className="grid grid-cols-3 gap-4">
                {(["r", "g", "b"] as const).map((part) => (
                  <div key={part} className="space-y-2">
                    <span className="text-[8px] font-bold text-zinc-600 uppercase">{part}</span>
                    <input
                      type="number"
                      value={rgb[part]}
                      onChange={(e) => handleRgbChange(part, e.target.value)}
                      className="w-full bg-white/5 border border-white/5 rounded-xl px-4 py-3 text-lg font-mono text-center outline-none focus:border-indigo-500/50 transition-colors"
                      min={0}
                      max={255}
                    />
                  </div>
                ))}
              </div>
            </div>

            <div className="space-y-3 pt-4 border-t border-white/5">
              <label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">HSL Values</label>
              <div className="text-sm font-mono text-indigo-300 bg-indigo-500/5 px-4 py-3 rounded-xl border border-indigo-500/10">
                hsl({hsl.h}, {hsl.s}%, {hsl.l}%)
              </div>
            </div>

            <div className="space-y-3">
              <label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">CSS / Styling</label>
              <div className="text-xs font-mono text-zinc-400 space-y-1.5 bg-zinc-900/50 p-4 rounded-xl border border-white/5">
                <div className="flex justify-between hover:text-white transition-colors cursor-pointer" onClick={() => copy(`#${hex}`, "Hex")}>
                  <span>color: #{hex};</span>
                  <Copy className="w-3 h-3 opacity-30" />
                </div>
                <div className="flex justify-between hover:text-white transition-colors cursor-pointer" onClick={() => copy(`rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`, "RGB")}>
                  <span>color: rgb({rgb.r}, {rgb.g}, {rgb.b});</span>
                  <Copy className="w-3 h-3 opacity-30" />
                </div>
              </div>
            </div>

            <div className="flex gap-4 pt-2">
              <Button onClick={() => copy(`#${hex}`, "Hex")} className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-xs font-bold uppercase tracking-widest h-12 rounded-2xl">
                Copy Hex
              </Button>
              <Button variant="secondary" onClick={() => copy(`rgb(${rgb.r}, ${rgb.g}, ${rgb.b})`, "RGB")} className="flex-1 bg-white/5 hover:bg-white/10 text-xs font-bold uppercase tracking-widest h-12 rounded-2xl">
                Copy RGB
              </Button>
            </div>
          </div>

          <div className="flex flex-col space-y-4">
            <div
              className={`flex-grow rounded-3xl border border-white/10 shadow-2xl transition-all duration-500 overflow-hidden relative`}
              style={{ backgroundColor: `#${hex}` }}
            >
              <div className="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent pointer-events-none"></div>
              <div className="absolute bottom-10 left-0 right-0 text-center">
                <span className="bg-black/60 backdrop-blur-md px-6 py-2 rounded-full text-sm font-mono font-bold text-white/90 border border-white/10 tracking-widest">
                  #{hex}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

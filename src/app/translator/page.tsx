"use client";

import { useState } from "react";
import { Globe, ArrowRightLeft, Languages, Trash2, Volume2, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Label } from "@/components/ui/label";

const LANGUAGES = [
  { code: "en", name: "English" },
  { code: "es", name: "Spanish" },
  { code: "fr", name: "French" },
  { code: "de", name: "German" },
  { code: "hi", name: "Hindi" },
  { code: "ja", name: "Japanese" },
  { code: "zh", name: "Chinese" },
  { code: "ru", name: "Russian" }
];

export default function TranslatorPage() {
  const [sourceLang, setSourceLang] = useState("en");
  const [targetLang, setTargetLang] = useState("es");
  const [inputText, setInputText] = useState("");
  const [translatedText, setTranslatedText] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleTranslate = async () => {
    if (!inputText.trim()) return;
    setIsLoading(true);
    
    try {
      // Mocking translation for demo/privacy-first POC
      // Real implementation would use MyMemory API (free/no key for limited use)
      const res = await fetch(`https://api.mymemory.translated.net/get?q=${encodeURIComponent(inputText)}&langpair=${sourceLang}|${targetLang}`);
      const data = await res.json();
      
      if (data.responseData) {
        setTranslatedText(data.responseData.translatedText);
        toast.success("Translation complete");
      } else {
        throw new Error("API returned invalid response");
      }
    } catch (e) {
      toast.error("Translation failed. Using fallback simulation.");
      setTranslatedText(`[${targetLang.toUpperCase()} Mock] ${inputText}`);
    } finally {
      setIsLoading(false);
    }
  };

  const swapLanguages = () => {
    setSourceLang(targetLang);
    setTargetLang(sourceLang);
    setInputText(translatedText);
    setTranslatedText(inputText);
  };

  const speak = (text: string, lang: string) => {
    if (!window.speechSynthesis) return;
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang;
    window.speechSynthesis.speak(utterance);
  };

  return (
    <div className="min-h-full p-6 lg:p-10 space-y-8 max-w-5xl mx-auto flex flex-col items-center">
      <div className="w-full bg-zinc-950/50 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 flex items-center justify-between shadow-xl">
        <div className="flex items-center gap-4">
          <Globe className="text-indigo-500 w-6 h-6" />
          <h1 className="text-xs font-black tracking-[4px] text-zinc-100 uppercase">Universal Translator</h1>
        </div>
      </div>

      <div className="w-full bg-zinc-950/40 border border-zinc-800 rounded-[40px] p-8 lg:p-12 space-y-8 shadow-2xl">
        <div className="flex flex-col md:flex-row items-center gap-6 justify-between">
           <div className="flex-1 w-full space-y-2">
             <Label className="text-[9px] font-black text-zinc-500 tracking-widest uppercase ml-4">From</Label>
             <Select value={sourceLang} onValueChange={setSourceLang}>
               <SelectTrigger className="bg-zinc-900 border-zinc-800 rounded-full h-14 px-8 text-sm font-bold">
                 <SelectValue />
               </SelectTrigger>
               <SelectContent className="bg-zinc-900 border-zinc-800 text-zinc-300">
                 {LANGUAGES.map(l => <SelectItem key={l.code} value={l.code}>{l.name}</SelectItem>)}
               </SelectContent>
             </Select>
           </div>

           <Button onClick={swapLanguages} variant="secondary" className="bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 rounded-full w-14 h-14 flex-shrink-0 animate-in spin-in-12 duration-500">
             <ArrowRightLeft className="w-6 h-6" />
           </Button>

           <div className="flex-1 w-full space-y-2">
             <Label className="text-[9px] font-black text-zinc-500 tracking-widest uppercase ml-4">To</Label>
             <Select value={targetLang} onValueChange={setTargetLang}>
               <SelectTrigger className="bg-zinc-900 border-zinc-800 rounded-full h-14 px-8 text-sm font-bold">
                 <SelectValue />
               </SelectTrigger>
               <SelectContent className="bg-zinc-900 border-zinc-800 text-zinc-300">
                 {LANGUAGES.map(l => <SelectItem key={l.code} value={l.code}>{l.name}</SelectItem>)}
               </SelectContent>
             </Select>
           </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-px bg-zinc-800/30 rounded-3xl overflow-hidden border border-zinc-800 shadow-inner">
           <div className="bg-zinc-950/40 p-6 flex flex-col space-y-4">
              <div className="flex justify-between items-center h-8">
                <Languages className="w-4 h-4 text-zinc-600" />
                {inputText && (
                  <Button variant="ghost" size="sm" onClick={() => speak(inputText, sourceLang)} className="text-zinc-500 hover:text-indigo-400">
                    <Volume2 className="w-4 h-4" />
                  </Button>
                )}
              </div>
              <textarea
                className="flex-grow min-h-[250px] bg-transparent text-xl font-medium text-white placeholder-zinc-700 outline-none resize-none leading-relaxed"
                placeholder="Type something to translate..."
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
              />
              <div className="flex justify-between items-center text-[10px] font-mono text-zinc-600">
                 <span>{inputText.length} characters</span>
                 <Button onClick={() => setInputText("")} variant="ghost" size="sm" className="hover:text-red-400">
                   <Trash2 className="w-3 h-3" />
                 </Button>
              </div>
           </div>

           <div className="bg-zinc-900/20 p-6 flex flex-col space-y-4 relative">
              <div className="flex justify-between items-center h-8">
                <span className="text-[10px] font-black tracking-widest text-indigo-500 uppercase">Translation</span>
                {translatedText && (
                  <div className="flex gap-1">
                    <Button variant="ghost" size="sm" onClick={() => speak(translatedText, targetLang)} className="text-zinc-500 hover:text-indigo-400">
                      <Volume2 className="w-4 h-4" />
                    </Button>
                    <Button variant="ghost" size="sm" onClick={() => { navigator.clipboard.writeText(translatedText); toast.success("Copied!"); }} className="text-zinc-500 hover:text-emerald-400">
                      <Copy className="w-4 h-4" />
                    </Button>
                  </div>
                )}
              </div>
              <textarea
                className={`flex-grow min-h-[250px] bg-transparent text-xl font-medium ${isLoading ? 'text-zinc-600 animate-pulse' : 'text-indigo-400'} placeholder-zinc-800 outline-none resize-none leading-relaxed`}
                value={translatedText}
                readOnly
                placeholder="Translation will appear here..."
              />
              {isLoading && (
                <div className="absolute inset-0 flex items-center justify-center bg-black/5 backdrop-blur-[1px]">
                   <div className="flex items-center gap-3 bg-zinc-900 px-6 py-2 rounded-full border border-white/5 shadow-2xl">
                      <div className="animate-spin h-3 w-3 border-2 border-indigo-500 rounded-full border-t-transparent" />
                      <span className="text-[9px] font-black text-white uppercase tracking-widest">Processing</span>
                   </div>
                </div>
              )}
           </div>
        </div>

        <Button 
          onClick={handleTranslate} 
          disabled={isLoading || !inputText.trim()} 
          className="w-full h-16 bg-indigo-600 hover:bg-indigo-700 text-white font-black uppercase tracking-[4px] text-xs rounded-2xl shadow-xl shadow-indigo-500/20 transition-all active:scale-95"
        >
          Translate Now
        </Button>
      </div>

      <p className="text-[9px] text-zinc-600 uppercase tracking-widest font-medium opacity-50">
        Powered by MyMemory Translation Service & Browser Speech API
      </p>
    </div>
  );
}

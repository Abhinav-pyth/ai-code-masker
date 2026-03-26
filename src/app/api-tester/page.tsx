"use client";

import { useState } from "react";
import { Send, Globe, Trash2, Rocket, Cloud, ShieldCheck } from "lucide-react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";

export default function ApiTesterPage() {
  const [url, setUrl] = useState("https://jsonplaceholder.typicode.com/todos/1");
  const [method, setMethod] = useState("GET");
  const [headers, setHeaders] = useState([{ key: "Content-Type", value: "application/json" }]);
  const [body, setBody] = useState("");
  const [response, setResponse] = useState<any>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [respMeta, setRespMeta] = useState({ status: 0, time: 0, size: 0 });

  const sendRequest = async () => {
    setIsLoading(true);
    const start = performance.now();
    try {
      const headerObj: Record<string, string> = {};
      headers.filter(h => h.key).forEach(h => headerObj[h.key] = h.value);

      const res = await fetch(url, {
        method,
        headers: headerObj,
        body: method !== "GET" && method !== "HEAD" ? body : undefined
      });

      const data = await res.json().catch(() => null);
      const end = performance.now();

      setResponse(data);
      setRespMeta({
        status: res.status,
        time: Math.round(end - start),
        size: JSON.stringify(data).length
      });
      toast.success(`Request completed: ${res.status}`);
    } catch (e: any) {
      toast.error(`Request failed: ${e.message}`);
      setResponse({ error: e.message });
    } finally {
      setIsLoading(false);
    }
  };

  const addHeader = () => setHeaders([...headers, { key: "", value: "" }]);
  const removeHeader = (i: number) => setHeaders(headers.filter((_, idx) => idx !== i));
  const updateHeader = (i: number, k: string, v: string) => {
    const newHeaders = [...headers];
    newHeaders[i] = { key: k, value: v };
    setHeaders(newHeaders);
  };

  return (
    <div className="min-h-full p-6 lg:p-10 space-y-8 max-w-6xl mx-auto flex flex-col">
      <div className="bg-zinc-950/50 backdrop-blur-xl border border-zinc-800 rounded-3xl p-6 flex flex-col lg:flex-row items-center gap-4 shadow-xl">
        <div className="flex items-center gap-4 w-full lg:w-fit">
          <Rocket className="text-indigo-500 w-6 h-6" />
          <h1 className="text-xs font-black tracking-[4px] text-zinc-100 uppercase mr-4">API Tester</h1>
        </div>
        
        <div className="flex flex-grow w-full gap-2">
          <Select value={method} onValueChange={setMethod}>
            <SelectTrigger className="w-28 bg-zinc-900 border-zinc-800 rounded-xl h-12 text-xs font-black text-indigo-400">
              <SelectValue />
            </SelectTrigger>
            <SelectContent className="bg-zinc-900 border-zinc-800 text-zinc-300">
              <SelectItem value="GET">GET</SelectItem>
              <SelectItem value="POST">POST</SelectItem>
              <SelectItem value="PUT">PUT</SelectItem>
              <SelectItem value="DELETE">DELETE</SelectItem>
              <SelectItem value="PATCH">PATCH</SelectItem>
            </SelectContent>
          </Select>
          <Input
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="flex-grow bg-zinc-900 border-zinc-800 rounded-xl h-12 font-mono text-sm"
            placeholder="https://api.example.com/v1"
          />
          <Button onClick={sendRequest} disabled={isLoading} className="bg-indigo-600 hover:bg-indigo-700 h-12 rounded-xl px-8 font-black uppercase tracking-widest text-[10px]">
            {isLoading ? <div className="animate-spin h-3 w-3 border-2 border-white rounded-full border-t-transparent" /> : "Send"}
          </Button>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 flex-grow overflow-hidden">
        {/* Request Setup */}
        <div className="flex flex-col space-y-6 min-h-0 bg-zinc-950/40 border border-zinc-800 rounded-3xl p-6">
          <Tabs defaultValue="headers" className="flex-grow flex flex-col">
            <TabsList className="bg-zinc-900 border border-white/5 rounded-full p-1 mb-6 h-11 w-fit">
              <TabsTrigger value="headers" className="rounded-full text-[10px] font-bold uppercase tracking-widest px-6">Headers</TabsTrigger>
              <TabsTrigger value="body" className="rounded-full text-[10px] font-bold uppercase tracking-widest px-6">Body</TabsTrigger>
            </TabsList>

            <TabsContent value="headers" className="flex-grow flex flex-col overflow-y-auto custom-scrollbar">
               <div className="space-y-3">
                 {headers.map((h, i) => (
                   <div key={i} className="flex gap-2">
                     <Input
                        placeholder="Key"
                        value={h.key}
                        onChange={(e) => updateHeader(i, e.target.value, h.value)}
                        className="bg-zinc-900 border-zinc-800 h-10 text-xs font-mono"
                     />
                     <Input
                        placeholder="Value"
                        value={h.value}
                        onChange={(e) => updateHeader(i, h.key, e.target.value)}
                        className="bg-zinc-900 border-zinc-800 h-10 text-xs font-mono"
                     />
                     <Button variant="ghost" size="sm" onClick={() => removeHeader(i)} className="text-zinc-600 hover:text-red-400">
                        <Trash2 className="w-3 h-3" />
                     </Button>
                   </div>
                 ))}
                 <Button variant="outline" size="sm" onClick={addHeader} className="w-full border-dashed border-zinc-800 text-[9px] font-bold uppercase">+ Add Header</Button>
               </div>
            </TabsContent>

            <TabsContent value="body" className="flex-grow flex flex-col">
               <textarea
                 className="flex-grow bg-[#0a0a0a] border border-white/5 rounded-2xl p-6 text-sm font-mono text-zinc-300 outline-none resize-none transition-all"
                 placeholder='{ "key": "value" }'
                 value={body}
                 onChange={(e) => setBody(e.target.value)}
               />
            </TabsContent>
          </Tabs>
        </div>

        {/* Response Panel */}
        <div className="flex flex-col space-y-6 min-h-0 bg-zinc-950/40 border border-zinc-800 rounded-3xl p-6 overflow-hidden relative">
          <div className="flex justify-between items-center mb-2">
             <div className="flex items-center gap-4">
                <ShieldCheck className="w-4 h-4 text-emerald-500" />
                <Label className="text-[10px] font-black text-zinc-500 tracking-widest uppercase">Response</Label>
             </div>
             {response && (
               <div className="flex items-center gap-3 animate-in fade-in duration-500">
                  <span className={`text-[10px] font-black uppercase ${respMeta.status < 300 ? 'text-emerald-500' : 'text-red-500'}`}>
                    {respMeta.status}
                  </span>
                  <span className="text-[9px] font-mono text-zinc-600">{respMeta.time}ms</span>
                  <span className="text-[9px] font-mono text-zinc-600">{(respMeta.size / 1024).toFixed(1)} KB</span>
               </div>
             )}
          </div>

          <div className="flex-grow bg-[#050505] rounded-2xl overflow-hidden relative">
             <textarea
               className="w-full h-full bg-transparent p-6 text-sm font-mono text-emerald-500/80 outline-none resize-none"
               readOnly
               value={response ? JSON.stringify(response, null, 2) : "Ready for request..."}
             />
             {isLoading && (
               <div className="absolute inset-0 bg-black/40 backdrop-blur-[2px] flex items-center justify-center">
                  <div className="flex items-center gap-3 bg-zinc-900 border border-white/10 px-6 py-2 rounded-full shadow-2xl">
                     <div className="animate-spin h-3 w-3 border-2 border-indigo-500 rounded-full border-t-transparent" />
                     <span className="text-[9px] font-black text-indigo-400 uppercase tracking-widest">Awaiting API...</span>
                  </div>
               </div>
             )}
          </div>
        </div>
      </div>
    </div>
  );
}

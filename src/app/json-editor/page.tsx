"use client";

import { useState } from "react";
import Editor from "@monaco-editor/react";
import { Button } from "@/components/ui/button";
import { toast } from "sonner";
import { CheckCircle2, XCircle } from "lucide-react";

// Recursive structural Node renderer
const JsonNode = ({ label, data }: { label: string | null; data: any }) => {
  const [collapsed, setCollapsed] = useState(false);

  const isObject = typeof data === "object" && data !== null;
  const isArray = Array.isArray(data);

  if (!isObject) {
    let valueClass = "text-slate-400";
    if (typeof data === "string") valueClass = "text-emerald-400";
    if (typeof data === "number") valueClass = "text-amber-400";
    if (typeof data === "boolean") valueClass = "text-pink-400";

    return (
      <div className="pl-4 py-0.5 text-sm font-mono tracking-tight">
        {label !== null && <span className="text-indigo-400 font-medium mr-1">{label}:</span>}
        <span className={valueClass}>
          {typeof data === "string" ? `"${data}"` : String(data)}
        </span>
      </div>
    );
  }

  const keys = Object.keys(data);
  const openBracket = isArray ? "[" : "{";
  const closeBracket = isArray ? "]" : "}";

  return (
    <div className="pl-4 py-0.5 text-sm font-mono tracking-tight cursor-default">
      <div className="flex items-start">
        <span
          className="text-indigo-500 font-black mr-2 select-none cursor-pointer w-4 text-center mt-[1px]"
          onClick={(e) => {
            e.stopPropagation();
            setCollapsed(!collapsed);
          }}
        >
          {collapsed ? "▸" : "▾"}
        </span>
        <div>
          {label !== null && <span className="text-indigo-400 font-medium mr-1">{label}:</span>}
          <span className="text-slate-500">{openBracket}</span>
          {collapsed && <span className="text-slate-500 ml-1">... {closeBracket}</span>}
        </div>
      </div>
      {!collapsed && (
        <>
          <div className="border-l border-white/5 ml-1 my-1">
            {keys.map((k) => (
              <JsonNode key={k} label={isArray ? null : k} data={data[k as keyof typeof data]} />
            ))}
          </div>
          <div className="pl-5 text-slate-500">{closeBracket}</div>
        </>
      )}
    </div>
  );
};

export default function JsonEditorPage() {
  const [jsonInput, setJsonInput] = useState("");
  const [parsedData, setParsedData] = useState<any>(null);
  const [isValid, setIsValid] = useState(true);

  const handleJsonChange = (value: string | undefined) => {
    const val = value || "";
    setJsonInput(val);
    if (!val.trim()) {
      setParsedData(null);
      setIsValid(true);
      return;
    }
    try {
      const parsed = JSON.parse(val);
      setParsedData(parsed);
      setIsValid(true);
    } catch (e) {
      setIsValid(false);
    }
  };

  const prettify = () => {
    try {
      const parsed = JSON.parse(jsonInput);
      setJsonInput(JSON.stringify(parsed, null, 2));
      toast.success("JSON Prettified");
    } catch {
      toast.error("Cannot prettify invalid JSON");
    }
  };

  const minify = () => {
    try {
      const parsed = JSON.parse(jsonInput);
      setJsonInput(JSON.stringify(parsed));
      toast.success("JSON Minified");
    } catch {
      toast.error("Cannot minify invalid JSON");
    }
  };

  const copyRaw = () => {
    navigator.clipboard.writeText(jsonInput);
    toast.success("Raw JSON copied!");
  };

  const clear = () => {
    setJsonInput("");
    setParsedData(null);
    setIsValid(true);
  };

  return (
    <div className="flex flex-col h-full w-full p-4 lg:p-8">
      {/* Top Toolbar */}
      <div className="h-16 border-b border-zinc-800 flex items-center justify-between px-6 bg-zinc-950 rounded-t-2xl shadow-sm">
        <div className="flex items-center space-x-4">
          <h2 className="text-xs font-black text-white tracking-[4px] uppercase">JSON Core Utility</h2>
        </div>
        <div className="flex space-x-3">
          <Button variant="ghost" size="sm" onClick={copyRaw} className="text-[10px] font-bold text-slate-400 hover:text-indigo-400 tracking-widest uppercase">
            Copy
          </Button>
          <Button variant="secondary" size="sm" onClick={prettify} className="text-[10px] font-bold text-indigo-400 uppercase">
            Prettify
          </Button>
          <Button variant="secondary" size="sm" onClick={minify} className="text-[10px] font-bold text-slate-400 uppercase">
            Minify
          </Button>
          <Button variant="destructive" size="sm" onClick={clear} className="text-[10px] font-bold uppercase bg-red-900/40 text-red-400 hover:bg-red-900/60">
            Clear
          </Button>
        </div>
      </div>

      {/* Editor & Tree View */}
      <div className="flex-grow grid grid-cols-1 lg:grid-cols-2 gap-8 pt-4">
        {/* Left Pane */}
        <div className="flex flex-col h-[600px] lg:h-full min-h-[500px] border border-zinc-800 rounded-b-2xl rounded-t-none lg:rounded-2xl overflow-hidden shadow-lg bg-[#1e1e1e]">
          <div className="bg-zinc-900 border-b border-zinc-800 px-4 py-3 flex justify-between items-center text-[10px] font-black text-indigo-400 tracking-[3px] uppercase">
            <span>Source JSON</span>
          </div>
          <div className="flex-grow">
            <Editor
              height="100%"
              defaultLanguage="json"
              theme="vs-dark"
              value={jsonInput}
              onChange={handleJsonChange}
              options={{ minimap: { enabled: false }, fontSize: 14, padding: { top: 16 }, scrollBeyondLastLine: false }}
            />
          </div>
        </div>

        {/* Right Pane (Tree) */}
        <div className="flex flex-col h-[600px] lg:h-full min-h-[500px] border border-zinc-800 rounded-2xl overflow-hidden shadow-lg bg-[#0a0a0a]">
          <div className="bg-zinc-900 border-b border-zinc-800 px-4 py-3 flex justify-between items-center text-[10px] font-black text-slate-500 tracking-[3px] uppercase">
            <span>Structural Tree</span>
            {!jsonInput ? (
              <span className="text-slate-600 italic tracking-normal lowercase">empty</span>
            ) : isValid ? (
              <span className="flex items-center text-emerald-400 tracking-normal lowercase"><CheckCircle2 className="w-3 h-3 mr-1"/> synced</span>
            ) : (
              <span className="flex items-center text-red-500 tracking-normal lowercase"><XCircle className="w-3 h-3 mr-1"/> syntax error</span>
            )}
          </div>
          <div className="flex-grow overflow-auto p-4 custom-scrollbar">
            {!jsonInput ? (
              <div className="text-slate-600 italic text-sm mt-4 text-center">No structure to display yet...</div>
            ) : !isValid ? (
              <div className="text-red-500/70 italic text-sm mt-4 text-center">Fix JSON syntax errors to see the tree</div>
            ) : (
              <div className="pt-2">
                <JsonNode label="Root" data={parsedData} />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

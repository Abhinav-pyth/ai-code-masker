"use client";

import { useState, useEffect } from "react";
import Editor from "@monaco-editor/react";
import { Copy, Trash2, FileCode2, Play, CheckCircle2, RotateCcw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Switch } from "@/components/ui/switch";
import { Label } from "@/components/ui/label";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";

const DEFAULT_SAMPLE = `// Example with sensitive data
const API_KEY = "sk-1234567890abcdef1234567890abcdef";
const email = "user@gmail.com";
const userPassword = "MySuperSecretPassword123!";
const awsToken = "AKIA1234567890EXAMPLE";

class DatabaseConnection {
  private secretKey: string;

  constructor(key) {
    this.secretKey = key;
  }

  public connectToDatabase() {
    console.log("Connecting with", email, this.secretKey);
  }
}

const db = new DatabaseConnection(API_KEY);
db.connectToDatabase();`;

export default function MaskingEditor() {
  const [inputCode, setInputCode] = useState("");
  const [outputCode, setOutputCode] = useState("");
  const [detectedSecrets, setDetectedSecrets] = useState<string[]>([]);
  const [restorationMap, setRestorationMap] = useState<Record<string, string> | null>(null);
  const [isMasking, setIsMasking] = useState(false);
  const [partialMode, setPartialMode] = useState(false);
  const [autoMask, setAutoMask] = useState(true);
  const [obfuscateIds, setObfuscateIds] = useState(false);

  // Debounced auto-mask
  useEffect(() => {
    if (!autoMask || !inputCode) return;
    const timeout = setTimeout(() => {
      handleMask();
    }, 500);
    return () => clearTimeout(timeout);
  }, [inputCode, partialMode, autoMask, obfuscateIds]);

  const handleMask = async () => {
    if (!inputCode.trim()) {
      setOutputCode("");
      setDetectedSecrets([]);
      setRestorationMap(null);
      return;
    }
    
    setIsMasking(true);
    try {
      const res = await fetch("/api/mask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: inputCode,
          mode: partialMode ? "partial" : "full",
          obfuscate: obfuscateIds,
          language: "js" // In real cases, dynamically detect from Editor
        }),
      });

      const data = await res.json();
      if (res.ok) {
        setOutputCode(data.maskedCode);
        setDetectedSecrets(data.detectedSecrets);
        setRestorationMap(data.mapping || null);
      } else {
        toast.error("Failed to mask code.");
      }
    } catch (error) {
      toast.error("An error occurred during masking.");
    } finally {
      setIsMasking(false);
    }
  };

  const handleUnmask = async () => {
    if (!outputCode || !restorationMap) {
      toast.error("No valid mapping generated. Enable Obfuscate Identifiers first.");
      return;
    }
    setIsMasking(true);
    try {
      const res = await fetch("/api/mask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code: outputCode,
          action: "unmask",
          mapping: restorationMap,
          language: "js"
        }),
      });
      const data = await res.json();
      if (res.ok) {
        setOutputCode(data.unmaskedCode);
        toast.success("Identifiers restored successfully!");
      } else {
        toast.error("Failed to restore code.");
      }
    } catch (error) {
      toast.error("Error during restoration.");
    } finally {
      setIsMasking(false);
    }
  };

  const loadSample = () => {
    setInputCode(DEFAULT_SAMPLE);
    toast.success("Sample code loaded");
  };

  const copyOutput = () => {
    if (!outputCode) return;
    navigator.clipboard.writeText(outputCode);
    toast.success("Output code copied to clipboard!");
  };

  const clearAll = () => {
    setInputCode("");
    setOutputCode("");
    setDetectedSecrets([]);
    setRestorationMap(null);
  };

  return (
    <div className="w-full flex-col flex space-y-4">
      {/* Controls */}
      <div className="flex flex-col xl:flex-row items-start xl:items-center justify-between gap-4 bg-zinc-950 p-4 rounded-xl border border-zinc-800 shadow-sm">
        <div className="flex flex-wrap items-center gap-2">
          <Button variant="outline" size="sm" onClick={loadSample}>
            <FileCode2 className="w-4 h-4 mr-2" />
            Load Sample
          </Button>
          <Button variant="outline" size="sm" onClick={clearAll}>
            <Trash2 className="w-4 h-4 mr-2" />
            Clear
          </Button>
        </div>

        <div className="flex flex-wrap items-center gap-6">
          <div className="flex items-center space-x-2">
            <Switch
              id="auto-mask"
              checked={autoMask}
              onCheckedChange={setAutoMask}
            />
            <Label htmlFor="auto-mask" className="text-zinc-400 whitespace-nowrap">Auto-mask</Label>
          </div>
          <div className="flex items-center space-x-2">
            <Switch
              id="partial-mode"
              checked={partialMode}
              onCheckedChange={setPartialMode}
            />
            <Label htmlFor="partial-mode" className="text-zinc-400 whitespace-nowrap">Partial Secret Stars</Label>
          </div>
          <div className="flex items-center space-x-2">
            <Switch
              id="obfuscate-ids"
              checked={obfuscateIds}
              onCheckedChange={setObfuscateIds}
            />
            <Label htmlFor="obfuscate-ids" className="text-emerald-400 font-medium whitespace-nowrap">Obfuscate Identifiers</Label>
          </div>

          <div className="flex gap-2">
            {!autoMask && (
              <Button size="sm" onClick={handleMask} disabled={isMasking} className="bg-emerald-600 hover:bg-emerald-700 text-white border-0">
                <Play className="w-4 h-4 mr-2" />
                Mask Now
              </Button>
            )}
            
            <Button size="sm" variant="secondary" onClick={handleUnmask} disabled={!restorationMap || isMasking}>
              <RotateCcw className="w-4 h-4 mr-2" />
              Restore Original
            </Button>
            
            <Button size="sm" variant="default" onClick={copyOutput} disabled={!outputCode}>
              <Copy className="w-4 h-4 mr-2" />
              Copy Output
            </Button>
          </div>
        </div>
      </div>

      {detectedSecrets.length > 0 && (
        <div className="flex items-center gap-2 px-1 text-sm text-zinc-400 flex-wrap">
          <CheckCircle2 className="w-4 h-4 text-emerald-500" />
          <span>Protected Secrets:</span>
          {detectedSecrets.map((secret, i) => (
            <Badge key={i} variant="secondary" className="bg-zinc-800 text-zinc-300 border-zinc-700 hover:bg-zinc-700">
              {secret}
            </Badge>
          ))}
        </div>
      )}

      {/* Editor Split View */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 h-[500px] lg:h-[600px]">
        {/* Input Pane */}
        <div className="flex flex-col border border-zinc-800 rounded-xl overflow-hidden shadow-lg bg-[#1e1e1e]">
          <div className="bg-zinc-900 border-b border-zinc-800 px-4 py-2 text-xs font-semibold text-zinc-400 flex justify-between items-center uppercase tracking-wider">
            Original Code
          </div>
          <div className="flex-grow">
            <Editor
              height="100%"
              defaultLanguage="javascript"
              theme="vs-dark"
              value={inputCode}
              onChange={(val) => setInputCode(val || "")}
              options={{
                minimap: { enabled: false },
                fontSize: 14,
                padding: { top: 16 },
                scrollBeyondLastLine: false,
                lineNumbersMinChars: 3,
              }}
            />
          </div>
        </div>

        {/* Output Pane */}
        <div className="flex flex-col border border-zinc-800 rounded-xl overflow-hidden shadow-lg bg-[#1e1e1e] relative">
          <div className="bg-zinc-900 border-b border-zinc-800 px-4 py-2 text-xs font-semibold text-emerald-500 flex justify-between items-center uppercase tracking-wider">
            Masked Output
          </div>
          <div className="flex-grow">
            <Editor
              height="100%"
              defaultLanguage="javascript"
              theme="vs-dark"
              value={outputCode}
              options={{
                readOnly: true,
                minimap: { enabled: false },
                fontSize: 14,
                padding: { top: 16 },
                scrollBeyondLastLine: false,
                lineNumbersMinChars: 3,
                renderLineHighlight: "none",
              }}
            />
          </div>
          {isMasking && (
            <div className="absolute inset-0 bg-zinc-950/20 backdrop-blur-[1px] flex items-center justify-center">
              <div className="text-emerald-500 bg-zinc-900 px-4 py-2 rounded-full shadow-lg border border-zinc-800 text-sm font-medium animate-pulse">
                Processing...
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

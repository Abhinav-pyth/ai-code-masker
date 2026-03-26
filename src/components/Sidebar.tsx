"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

export default function Sidebar() {
  const pathname = usePathname();

  const links = [
    { href: "/", label: "Code Masker", group: "Core" },
    { href: "/json-editor", label: "JSON Editor", group: "Core" },
    { href: "/base64", label: "Base64", group: "Encoding" },
    { href: "/base64-to-pdf", label: "Base64 to PDF", group: "Encoding" },
    { href: "/base64-to-image", label: "Base64 to Image", group: "Encoding" },
    // ...other links can be mapped similarly, but keeping the requested ones explicit
    { href: "/image-resize", label: "Image Resize", group: "Image Tools" },
    { href: "/pixel-editor", label: "Pixel Editor", group: "Image Tools" },
    { href: "/image-converter", label: "Image Converter", group: "Image Tools" },
    { href: "/hex-rgb", label: "Hex/RGB", group: "Colors" },
    { href: "/translator", label: "Translator", group: "Text & Language" },
    { href: "/qr-generator", label: "QR Generator", group: "Generators" },
    { href: "/api-tester", label: "API Tester", group: "API Testing" }
  ];

  const groupedLinks = links.reduce((acc, link) => {
    acc[link.group] = acc[link.group] || [];
    acc[link.group].push(link);
    return acc;
  }, {} as Record<string, typeof links>);

  return (
    <aside className="w-64 bg-zinc-950/80 backdrop-blur-xl border-r border-white/5 flex flex-col h-full shrink-0 z-50">
      <div className="flex items-center px-6 py-6 space-x-3 cursor-pointer border-b border-white/5 mb-2 hover:bg-white/5 transition-colors" onClick={() => window.location.href='/'}>
        <div className="w-10 h-10 bg-indigo-600 rounded-xl flex items-center justify-center shadow-lg shadow-indigo-500/20">
          <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
          </svg>
        </div>
        <div>
          <h1 className="text-sm font-bold text-white tracking-widest uppercase">Dev Tools</h1>
          <p className="text-[9px] text-indigo-400 font-bold uppercase opacity-80">Workspace v3.0</p>
        </div>
      </div>

      <nav className="flex-grow flex flex-col px-3 overflow-y-auto space-y-1 pb-6 custom-scrollbar">
        {Object.entries(groupedLinks).map(([groupName, groupLinks]) => (
          <div key={groupName} className="mb-2">
            <div className="text-[9px] font-black tracking-widest uppercase text-slate-500 px-4 py-2 mt-2">
              {groupName}
            </div>
            {groupLinks.map((link) => {
              const isActive = pathname === link.href;
              return (
                <Link
                  key={link.href}
                  href={link.href}
                  className={`flex items-center space-x-3 px-4 py-2.5 rounded-xl text-sm transition-all ${
                    isActive
                      ? "bg-indigo-500/10 text-white font-semibold border border-indigo-500/30"
                      : "text-slate-400 hover:bg-white/5 hover:text-white"
                  }`}
                >
                  <span className="truncate">{link.label}</span>
                </Link>
              );
            })}
          </div>
        ))}
      </nav>
    </aside>
  );
}

# AI Code Masker — Eclipse Plugin

> 🔒 Privacy-first code masking directly inside Eclipse IDE.

Mask sensitive identifiers, API keys, and secrets **before** sharing code with AI tools — then restore them when you get the response back.

## Installation (Eclipse PDE)

### From Source (Eclipse Workspace)
1. Clone this repo and open Eclipse with PDE installed
2. `File → Import → General → Existing Projects into Workspace`
3. Select the `eclipse_plugin/` folder
4. Right-click the project → `Run As → Eclipse Application`

### Building a Distributable JAR
1. Right-click the project → `Export → Plug-in Development → Deployable plug-ins and fragments`
2. Export to a folder; copy the `.jar` to your Eclipse `dropins/` folder
3. Restart Eclipse

## Features

| Feature | Shortcut | How to Access |
|---------|----------|---------------|
| **Mask Selection** | `Ctrl+Shift+M` | Right-click → 🔒 AI Code Masker → Mask Selection |
| **Mask Entire File** | — | Right-click → 🔒 AI Code Masker → Mask Entire File |
| **Unmask Selection** | `Ctrl+Shift+U` | Right-click → 🔒 AI Code Masker → Unmask Selection |
| **Unmask Entire File** | — | Right-click → 🔒 AI Code Masker → Unmask Entire File |
| **Show Mapping View** | — | Window → Show View → AI Code Masker → Masker Mapping |

## How It Works

1. **Select** code (or use entire file)
2. **Press `Ctrl+Shift+M`** — identifiers become `var_1`, `method_2`, `Class_3`
3. **Paste** masked code into your AI tool & get the response
4. **Paste** AI response back; press `Ctrl+Shift+U` to restore

## Supported Languages
- Java (`.java`)
- Python (`.py`)
- JavaScript / TypeScript (`.js`, `.ts`, `.jsx`, `.tsx`)

## Requirements
- Eclipse 2023-06 or newer
- Java 11+
- Eclipse PDE (for building from source)

## Privacy
**Zero network calls.** All masking happens in-process, never leaves your machine.

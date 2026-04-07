# AI Code Masker — VS Code Extension

> 🔒 Privacy-first code masking for AI-assisted development.

Mask sensitive identifiers, API keys, secrets, and tokens **before** sharing code with ChatGPT, Copilot, Claude, or any AI tool — then restore them when you get the response back.

## Features

| Feature | Shortcut | Description |
|---------|----------|-------------|
| **Mask Selection** | `Ctrl+Shift+M` | Mask identifiers in highlighted text |
| **Mask Entire File** | `Ctrl+Shift+Alt+M` | Mask all identifiers, opens side-by-side |
| **Unmask Selection** | `Ctrl+Shift+U` | Restore masked text using stored mapping |
| **Unmask Entire File** | `Ctrl+Shift+Alt+U` | Restore full file from mapping |
| **Mask & Copy** | Right-click menu | Mask and copy to clipboard in one step |
| **Mapping Panel** | Status bar click | View, copy, download the mapping JSON |

## How It Works

1. **Select** code you want to protect
2. **Press `Ctrl+Shift+M`** — identifiers become `var_1`, `method_2`, `Class_3`
3. **Paste** the masked code into your AI tool
4. **Get the AI response**, paste it back
5. **Press `Ctrl+Shift+U`** — original names are restored

The mapping is stored per-file and persists across VS Code restarts.

## Supported Languages

- Python
- Java
- JavaScript / TypeScript / React / Vue / Svelte

## Sensitive Pattern Detection

Automatically detects and masks:
- 📧 Email addresses
- 🔑 AWS access keys (`AKIA...`)
- 🔐 Secret tokens (`token=`, `password=`, `api_key=`)
- 🌐 IP addresses

## Configuration

| Setting | Default | Description |
|---------|---------|-------------|
| `aiCodeMasker.detectSensitivePatterns` | `true` | Enable secret/email/IP detection |
| `aiCodeMasker.customRules` | `[]` | Custom identifiers to always mask |
| `aiCodeMasker.autoShowMapping` | `true` | Auto-show mapping panel after masking |

## Installation

### From VSIX (Local)
```bash
cd vscode_extension
npm install
npm run compile
npx vsce package
code --install-extension ai-code-masker-1.0.0.vsix
```

## Privacy

**Zero network calls.** All masking happens locally in your VS Code instance. No data is sent anywhere.

## License

MIT

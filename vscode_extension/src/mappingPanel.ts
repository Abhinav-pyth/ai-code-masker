/**
 * AI Code Masker — Mapping Panel (Webview)
 * Displays the current mapping as a styled, interactive panel.
 */

import * as vscode from 'vscode';
import { mappingStore } from './mappingStore';

export class MappingPanel {
    public static currentPanel: MappingPanel | undefined;
    private static readonly viewType = 'aiCodeMasker.mappingPanel';

    private readonly panel: vscode.WebviewPanel;
    private readonly disposables: vscode.Disposable[] = [];

    private constructor(panel: vscode.WebviewPanel) {
        this.panel = panel;

        // Listen for mapping changes
        this.disposables.push(
            mappingStore.onDidChange(() => this.update())
        );

        // Listen for active editor changes
        this.disposables.push(
            vscode.window.onDidChangeActiveTextEditor(() => this.update())
        );

        // Handle panel disposal
        this.panel.onDidDispose(() => this.dispose(), null, this.disposables);

        // Handle messages from the webview
        this.panel.webview.onDidReceiveMessage(
            async (message) => {
                switch (message.command) {
                    case 'copy':
                        await vscode.env.clipboard.writeText(message.text);
                        vscode.window.showInformationMessage('Mapping copied to clipboard!');
                        break;
                    case 'clear':
                        if (message.uri) {
                            mappingStore.clearMapping(message.uri);
                            vscode.window.showInformationMessage('Mapping cleared.');
                        }
                        break;
                    case 'download':
                        const uri = await vscode.window.showSaveDialog({
                            defaultUri: vscode.Uri.file('masker-mapping.json'),
                            filters: { 'JSON': ['json'] }
                        });
                        if (uri) {
                            await vscode.workspace.fs.writeFile(uri, Buffer.from(message.text, 'utf-8'));
                            vscode.window.showInformationMessage('Mapping saved!');
                        }
                        break;
                }
            },
            null,
            this.disposables
        );

        this.update();
    }

    /** Create or reveal the Mapping Panel */
    public static show(): void {
        const column = vscode.window.activeTextEditor
            ? vscode.ViewColumn.Beside
            : vscode.ViewColumn.One;

        if (MappingPanel.currentPanel) {
            MappingPanel.currentPanel.panel.reveal(column);
            return;
        }

        const panel = vscode.window.createWebviewPanel(
            MappingPanel.viewType,
            '🔒 AI Code Masker — Mapping',
            column,
            {
                enableScripts: true,
                retainContextWhenHidden: true
            }
        );

        MappingPanel.currentPanel = new MappingPanel(panel);
    }

    /** Force-update the panel content */
    public update(): void {
        const editor = vscode.window.activeTextEditor;
        const fileUri = editor?.document.uri.toString() || '';
        const fileName = editor?.document.fileName.split(/[/\\]/).pop() || 'No file open';
        const mapping = fileUri ? mappingStore.getMapping(fileUri) : undefined;

        this.panel.webview.html = this.getHtml(fileName, fileUri, mapping);
    }

    private getHtml(
        fileName: string,
        fileUri: string,
        mapping: Record<string, string> | undefined
    ): string {
        const entries = mapping ? Object.entries(mapping) : [];
        const jsonStr = mapping ? JSON.stringify(mapping, null, 2) : '{}';

        const tableRows = entries.length > 0
            ? entries.map(([original, masked], i) => `
                <tr>
                    <td class="idx">${i + 1}</td>
                    <td class="original">${escapeHtml(original)}</td>
                    <td class="arrow">→</td>
                    <td class="masked">${escapeHtml(masked)}</td>
                </tr>
            `).join('')
            : `<tr><td colspan="4" class="empty">No mappings yet. Mask some code to see the mapping here.</td></tr>`;

        return /* html */`<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Code Masker Mapping</title>
    <style>
        :root {
            --bg: #0d1117;
            --surface: #161b22;
            --border: #21262d;
            --text: #c9d1d9;
            --text-muted: #8b949e;
            --accent: #6366f1;
            --accent-glow: rgba(99, 102, 241, 0.15);
            --green: #10b981;
            --red: #f87171;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            background: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, sans-serif;
            padding: 20px;
            line-height: 1.6;
        }
        .header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }
        .header h1 {
            font-size: 14px;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: var(--accent);
        }
        .file-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--accent-glow);
            border: 1px solid rgba(99, 102, 241, 0.3);
            border-radius: 8px;
            padding: 4px 12px;
            font-size: 11px;
            color: var(--accent);
            font-weight: 600;
        }
        .stats {
            display: flex;
            gap: 12px;
            margin-bottom: 20px;
        }
        .stat-card {
            flex: 1;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
        }
        .stat-card .value {
            font-size: 28px;
            font-weight: 900;
            color: var(--accent);
        }
        .stat-card .label {
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-top: 4px;
        }
        .actions {
            display: flex;
            gap: 8px;
            margin-bottom: 20px;
        }
        .btn {
            padding: 8px 16px;
            border: 1px solid var(--border);
            border-radius: 8px;
            background: var(--surface);
            color: var(--text);
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            cursor: pointer;
            transition: all 0.15s ease;
        }
        .btn:hover {
            border-color: var(--accent);
            color: var(--accent);
            background: var(--accent-glow);
        }
        .btn.danger:hover {
            border-color: var(--red);
            color: var(--red);
            background: rgba(248, 113, 113, 0.1);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: var(--surface);
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid var(--border);
        }
        th {
            background: rgba(99, 102, 241, 0.08);
            padding: 10px 16px;
            text-align: left;
            font-size: 10px;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            color: var(--accent);
            font-weight: 800;
        }
        td {
            padding: 8px 16px;
            font-size: 13px;
            border-top: 1px solid var(--border);
            font-family: 'Fira Code', 'Cascadia Code', 'JetBrains Mono', monospace;
        }
        .idx { color: var(--text-muted); width: 40px; font-size: 11px; }
        .original { color: var(--red); font-weight: 600; }
        .arrow { color: var(--text-muted); width: 30px; text-align: center; }
        .masked { color: var(--green); font-weight: 600; }
        .empty {
            text-align: center;
            color: var(--text-muted);
            font-style: italic;
            padding: 40px 16px;
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        }
        .json-section {
            margin-top: 20px;
        }
        .json-section h3 {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--text-muted);
            margin-bottom: 8px;
        }
        .json-block {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            color: var(--green);
            white-space: pre-wrap;
            word-break: break-all;
            max-height: 200px;
            overflow: auto;
            opacity: 0.7;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 Mapping Panel</h1>
        <span class="file-badge">📄 ${escapeHtml(fileName)}</span>
    </div>

    <div class="stats">
        <div class="stat-card">
            <div class="value">${entries.length}</div>
            <div class="label">Identifiers Masked</div>
        </div>
        <div class="stat-card">
            <div class="value">${entries.filter(([,v]) => v.startsWith('SECRET_') || v.startsWith('EMAIL_') || v.startsWith('AWS_KEY_') || v.startsWith('IP_ADDRESS_')).length}</div>
            <div class="label">Secrets Detected</div>
        </div>
    </div>

    <div class="actions">
        <button class="btn" onclick="copyMapping()">📋 Copy JSON</button>
        <button class="btn" onclick="downloadMapping()">💾 Download</button>
        <button class="btn danger" onclick="clearMapping()">🗑 Clear</button>
    </div>

    <table>
        <thead>
            <tr>
                <th>#</th>
                <th>Original</th>
                <th></th>
                <th>Masked As</th>
            </tr>
        </thead>
        <tbody>
            ${tableRows}
        </tbody>
    </table>

    <div class="json-section">
        <h3>Raw JSON Map</h3>
        <div class="json-block">${escapeHtml(jsonStr)}</div>
    </div>

    <script>
        const vscode = acquireVsCodeApi();
        const fileUri = ${JSON.stringify(fileUri)};
        const jsonStr = ${JSON.stringify(jsonStr)};

        function copyMapping() {
            vscode.postMessage({ command: 'copy', text: jsonStr });
        }
        function downloadMapping() {
            vscode.postMessage({ command: 'download', text: jsonStr });
        }
        function clearMapping() {
            vscode.postMessage({ command: 'clear', uri: fileUri });
        }
    </script>
</body>
</html>`;
    }

    private dispose(): void {
        MappingPanel.currentPanel = undefined;
        this.panel.dispose();
        while (this.disposables.length) {
            const d = this.disposables.pop();
            if (d) { d.dispose(); }
        }
    }
}

function escapeHtml(text: string): string {
    return text
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

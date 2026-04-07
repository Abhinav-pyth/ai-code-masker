/**
 * AI Code Masker — VS Code Extension Entry Point
 * Registers all commands, status bar, and context menu integration.
 */

import * as vscode from 'vscode';
import { maskContent, unmaskContent, detectLanguage } from './maskerEngine';
import { mappingStore } from './mappingStore';
import { MappingPanel } from './mappingPanel';

let statusBarItem: vscode.StatusBarItem;

export function activate(context: vscode.ExtensionContext) {
    console.log('AI Code Masker extension activated');

    // Initialize persistent mapping store
    mappingStore.initialize(context);

    // ─── Status Bar ────────────────────────────────────────────
    statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'aiCodeMasker.showMapping';
    updateStatusBar();
    statusBarItem.show();
    context.subscriptions.push(statusBarItem);

    // Update status bar on editor change
    context.subscriptions.push(
        vscode.window.onDidChangeActiveTextEditor(() => updateStatusBar())
    );
    context.subscriptions.push(
        mappingStore.onDidChange(() => updateStatusBar())
    );

    // ─── Commands ──────────────────────────────────────────────

    // Mask Selection
    context.subscriptions.push(
        vscode.commands.registerCommand('aiCodeMasker.maskSelection', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor.');
                return;
            }

            const selection = editor.selection;
            if (selection.isEmpty) {
                vscode.window.showWarningMessage('No text selected. Select code to mask.');
                return;
            }

            const text = editor.document.getText(selection);
            const lang = detectLanguage(editor.document.languageId);
            const config = vscode.workspace.getConfiguration('aiCodeMasker');
            const customRules = config.get<string[]>('customRules', []);
            const detectSecrets = config.get<boolean>('detectSensitivePatterns', true);

            const result = maskContent(text, lang, customRules, detectSecrets);

            await editor.edit(editBuilder => {
                editBuilder.replace(selection, result.maskedCode);
            });

            // Store mapping
            const uri = editor.document.uri.toString();
            mappingStore.mergeMapping(uri, result.mapping);

            const count = Object.keys(result.mapping).length;
            vscode.window.showInformationMessage(
                `🔒 Masked ${count} identifier${count !== 1 ? 's' : ''}. Mapping stored.`
            );

            // Auto-show mapping panel
            if (config.get<boolean>('autoShowMapping', true)) {
                MappingPanel.show();
            }
        })
    );

    // Mask Entire File
    context.subscriptions.push(
        vscode.commands.registerCommand('aiCodeMasker.maskFile', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor.');
                return;
            }

            const text = editor.document.getText();
            const lang = detectLanguage(editor.document.languageId);
            const config = vscode.workspace.getConfiguration('aiCodeMasker');
            const customRules = config.get<string[]>('customRules', []);
            const detectSecrets = config.get<boolean>('detectSensitivePatterns', true);

            const result = maskContent(text, lang, customRules, detectSecrets);

            // Open masked content in a new untitled document beside the original
            const maskedDoc = await vscode.workspace.openTextDocument({
                content: result.maskedCode,
                language: editor.document.languageId
            });
            await vscode.window.showTextDocument(maskedDoc, vscode.ViewColumn.Beside);

            // Store mapping against the original file
            const uri = editor.document.uri.toString();
            mappingStore.setMapping(uri, result.mapping);

            const count = Object.keys(result.mapping).length;
            vscode.window.showInformationMessage(
                `🔒 Masked ${count} identifier${count !== 1 ? 's' : ''} across the file. Copy the masked version for AI use.`
            );

            if (config.get<boolean>('autoShowMapping', true)) {
                MappingPanel.show();
            }
        })
    );

    // Unmask Selection
    context.subscriptions.push(
        vscode.commands.registerCommand('aiCodeMasker.unmaskSelection', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor.');
                return;
            }

            const selection = editor.selection;
            if (selection.isEmpty) {
                vscode.window.showWarningMessage('No text selected. Select masked code to restore.');
                return;
            }

            // Try to find mapping for this file, or prompt user for a mapping
            const uri = editor.document.uri.toString();
            let mapping = mappingStore.getMapping(uri);

            if (!mapping) {
                // Try to get mapping from clipboard
                const clipText = await vscode.env.clipboard.readText();
                try {
                    mapping = JSON.parse(clipText);
                    if (typeof mapping !== 'object' || Array.isArray(mapping)) {
                        throw new Error('Invalid mapping format');
                    }
                } catch {
                    // Prompt user to paste mapping
                    const input = await vscode.window.showInputBox({
                        prompt: 'No stored mapping found. Paste the JSON mapping:',
                        placeHolder: '{"originalName": "var_1", ...}',
                        ignoreFocusOut: true
                    });
                    if (!input) { return; }
                    try {
                        mapping = JSON.parse(input);
                    } catch {
                        vscode.window.showErrorMessage('Invalid JSON mapping.');
                        return;
                    }
                }
            }

            if (!mapping) {
                vscode.window.showErrorMessage('No mapping available for unmasking.');
                return;
            }

            const text = editor.document.getText(selection);
            const lang = detectLanguage(editor.document.languageId);
            const restored = unmaskContent(text, mapping, lang);

            await editor.edit(editBuilder => {
                editBuilder.replace(selection, restored);
            });

            vscode.window.showInformationMessage('🔓 Code restored successfully!');
        })
    );

    // Unmask Entire File
    context.subscriptions.push(
        vscode.commands.registerCommand('aiCodeMasker.unmaskFile', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor.');
                return;
            }

            const uri = editor.document.uri.toString();
            let mapping = mappingStore.getMapping(uri);

            if (!mapping) {
                const input = await vscode.window.showInputBox({
                    prompt: 'No stored mapping. Paste the JSON mapping:',
                    placeHolder: '{"originalName": "var_1", ...}',
                    ignoreFocusOut: true
                });
                if (!input) { return; }
                try {
                    mapping = JSON.parse(input);
                } catch {
                    vscode.window.showErrorMessage('Invalid JSON mapping.');
                    return;
                }
            }

            if (!mapping) {
                vscode.window.showErrorMessage('No mapping available.');
                return;
            }

            const text = editor.document.getText();
            const lang = detectLanguage(editor.document.languageId);
            const restored = unmaskContent(text, mapping, lang);

            const restoredDoc = await vscode.workspace.openTextDocument({
                content: restored,
                language: editor.document.languageId
            });
            await vscode.window.showTextDocument(restoredDoc, vscode.ViewColumn.Beside);

            vscode.window.showInformationMessage('🔓 File restored! Review the output in the new tab.');
        })
    );

    // Mask & Copy to Clipboard
    context.subscriptions.push(
        vscode.commands.registerCommand('aiCodeMasker.copyMaskedToClipboard', async () => {
            const editor = vscode.window.activeTextEditor;
            if (!editor) {
                vscode.window.showWarningMessage('No active editor.');
                return;
            }

            const selection = editor.selection;
            const text = selection.isEmpty
                ? editor.document.getText()
                : editor.document.getText(selection);

            const lang = detectLanguage(editor.document.languageId);
            const config = vscode.workspace.getConfiguration('aiCodeMasker');
            const customRules = config.get<string[]>('customRules', []);
            const detectSecrets = config.get<boolean>('detectSensitivePatterns', true);

            const result = maskContent(text, lang, customRules, detectSecrets);

            await vscode.env.clipboard.writeText(result.maskedCode);

            const uri = editor.document.uri.toString();
            mappingStore.mergeMapping(uri, result.mapping);

            vscode.window.showInformationMessage(
                `🔒 Masked code copied to clipboard! ${Object.keys(result.mapping).length} identifiers protected.`
            );

            if (config.get<boolean>('autoShowMapping', true)) {
                MappingPanel.show();
            }
        })
    );

    // Show Mapping Panel
    context.subscriptions.push(
        vscode.commands.registerCommand('aiCodeMasker.showMapping', () => {
            MappingPanel.show();
        })
    );

    // Clear Mapping
    context.subscriptions.push(
        vscode.commands.registerCommand('aiCodeMasker.clearMapping', async () => {
            const editor = vscode.window.activeTextEditor;
            if (editor) {
                mappingStore.clearMapping(editor.document.uri.toString());
            } else {
                mappingStore.clearAll();
            }
            vscode.window.showInformationMessage('🗑 Mapping cleared.');
        })
    );
}

function updateStatusBar(): void {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        statusBarItem.text = '$(shield) AI Masker';
        statusBarItem.tooltip = 'AI Code Masker — No file open';
        return;
    }

    const uri = editor.document.uri.toString();
    const count = mappingStore.getMappingCount(uri);

    if (count > 0) {
        statusBarItem.text = `$(lock) Masked (${count})`;
        statusBarItem.tooltip = `AI Code Masker — ${count} identifiers masked in this file. Click to view mapping.`;
        statusBarItem.backgroundColor = new vscode.ThemeColor('statusBarItem.warningBackground');
    } else {
        statusBarItem.text = '$(unlock) AI Masker';
        statusBarItem.tooltip = 'AI Code Masker — Ready. Use Ctrl+Shift+M to mask selected code.';
        statusBarItem.backgroundColor = undefined;
    }
}

export function deactivate() {
    mappingStore.dispose();
}

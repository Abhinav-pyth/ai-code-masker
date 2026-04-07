/**
 * AI Code Masker — Mapping Store
 * Manages per-file mappings with workspace-level persistence.
 */

import * as vscode from 'vscode';

export class MappingStore {
    private memoryStore: Map<string, Record<string, string>> = new Map();
    private context: vscode.ExtensionContext | undefined;

    /** Bind to extension context for workspace-state persistence */
    initialize(context: vscode.ExtensionContext): void {
        this.context = context;

        // Restore persisted mappings from workspace state
        const persisted = context.workspaceState.get<Record<string, Record<string, string>>>('aiCodeMasker.mappings');
        if (persisted) {
            for (const [uri, mapping] of Object.entries(persisted)) {
                this.memoryStore.set(uri, mapping);
            }
        }
    }

    /** Get mapping for a file URI */
    getMapping(uri: string): Record<string, string> | undefined {
        return this.memoryStore.get(uri);
    }

    /** Store mapping for a file URI */
    setMapping(uri: string, mapping: Record<string, string>): void {
        this.memoryStore.set(uri, mapping);
        this.persist();
        this._onDidChange.fire(uri);
    }

    /** Merge new mapping entries into an existing mapping for a file */
    mergeMapping(uri: string, newEntries: Record<string, string>): void {
        const existing = this.memoryStore.get(uri) || {};
        const merged = { ...existing, ...newEntries };
        this.setMapping(uri, merged);
    }

    /** Clear mapping for a file URI */
    clearMapping(uri: string): void {
        this.memoryStore.delete(uri);
        this.persist();
        this._onDidChange.fire(uri);
    }

    /** Clear all mappings */
    clearAll(): void {
        this.memoryStore.clear();
        this.persist();
        this._onDidChange.fire('*');
    }

    /** Get all stored file URIs that have mappings */
    getAllUris(): string[] {
        return Array.from(this.memoryStore.keys());
    }

    /** Get the total count of mapped identifiers for a file */
    getMappingCount(uri: string): number {
        const mapping = this.memoryStore.get(uri);
        return mapping ? Object.keys(mapping).length : 0;
    }

    /** Export all mappings as a JSON string */
    exportAll(): string {
        const obj: Record<string, Record<string, string>> = {};
        for (const [uri, mapping] of this.memoryStore.entries()) {
            obj[uri] = mapping;
        }
        return JSON.stringify(obj, null, 2);
    }

    /** Event emitter for mapping changes */
    private _onDidChange = new vscode.EventEmitter<string>();
    readonly onDidChange = this._onDidChange.event;

    /** Persist current state to workspace storage */
    private persist(): void {
        if (!this.context) { return; }
        const obj: Record<string, Record<string, string>> = {};
        for (const [uri, mapping] of this.memoryStore.entries()) {
            obj[uri] = mapping;
        }
        this.context.workspaceState.update('aiCodeMasker.mappings', obj);
    }

    dispose(): void {
        this._onDidChange.dispose();
    }
}

/** Singleton instance */
export const mappingStore = new MappingStore();

package com.aimasker.eclipse.handlers;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.jface.dialogs.InputDialog;
import org.eclipse.jface.dialogs.MessageDialog;
import org.eclipse.jface.text.IDocument;
import org.eclipse.jface.text.ITextSelection;
import org.eclipse.jface.viewers.ISelection;
import org.eclipse.jface.window.Window;
import org.eclipse.ui.IEditorPart;
import org.eclipse.ui.handlers.HandlerUtil;
import org.eclipse.ui.texteditor.ITextEditor;

import com.aimasker.eclipse.MaskerEngine;
import com.aimasker.eclipse.MappingStore;
import com.aimasker.eclipse.views.MappingView;

import java.util.Map;
import java.util.HashMap;

/**
 * Unmasks identifiers in the currently selected text.
 * Keybinding: Ctrl+Shift+U
 */
public class UnmaskSelectionHandler extends AbstractHandler {

    @Override
    public Object execute(ExecutionEvent event) throws ExecutionException {
        IEditorPart editorPart = HandlerUtil.getActiveEditor(event);
        if (!(editorPart instanceof ITextEditor)) {
            MessageDialog.openWarning(
                HandlerUtil.getActiveShell(event),
                "AI Code Masker",
                "Please open a text file."
            );
            return null;
        }

        ITextEditor editor   = (ITextEditor) editorPart;
        String filePath      = MaskSelectionHandler.getFilePath(editor);
        String lang          = MaskerEngine.detectLanguage(filePath);

        ISelection selection = HandlerUtil.getCurrentSelection(event);
        if (!(selection instanceof ITextSelection)) {
            MessageDialog.openWarning(
                HandlerUtil.getActiveShell(event),
                "AI Code Masker",
                "Please select some masked code to restore."
            );
            return null;
        }

        ITextSelection textSel = (ITextSelection) selection;
        if (textSel.isEmpty()) {
            MessageDialog.openWarning(
                HandlerUtil.getActiveShell(event),
                "AI Code Masker",
                "Selection is empty. Please select the masked code to restore."
            );
            return null;
        }

        // Get mapping from store, or ask user to paste it
        Map<String, String> mapping = getOrPromptMapping(event, filePath);
        if (mapping == null || mapping.isEmpty()) return null;

        String restored = MaskerEngine.unmaskContent(textSel.getText(), mapping, lang);

        IDocument doc = editor.getDocumentProvider().getDocument(editor.getEditorInput());
        try {
            doc.replace(textSel.getOffset(), textSel.getLength(), restored);
        } catch (Exception e) {
            MessageDialog.openError(
                HandlerUtil.getActiveShell(event),
                "AI Code Masker — Error",
                "Failed to replace text: " + e.getMessage()
            );
            return null;
        }

        MappingView.refresh();
        MessageDialog.openInformation(
            HandlerUtil.getActiveShell(event),
            "AI Code Masker",
            "✅ Code restored successfully!"
        );

        return null;
    }

    @SuppressWarnings("unchecked")
    static Map<String, String> getOrPromptMapping(ExecutionEvent event, String filePath) {
        MappingStore store = MappingStore.getInstance();

        if (store.hasMapping(filePath)) {
            return store.getMapping(filePath);
        }

        // No stored mapping — prompt user to paste JSON
        InputDialog dialog = new InputDialog(
            HandlerUtil.getActiveShell(event),
            "AI Code Masker — Paste Mapping",
            "No stored mapping found for this file.\nPaste the JSON mapping below:",
            "{}",
            null
        );

        if (dialog.open() != Window.OK) return null;

        String jsonInput = dialog.getValue();
        try {
            // Simple JSON parse using Jackson-style or manual approach
            Map<String, String> mapping = parseSimpleJsonMap(jsonInput);
            if (!mapping.isEmpty()) {
                store.setMapping(filePath, mapping);
            }
            return mapping;
        } catch (Exception e) {
            MessageDialog.openError(
                HandlerUtil.getActiveShell(event),
                "AI Code Masker",
                "Invalid JSON mapping: " + e.getMessage()
            );
            return null;
        }
    }

    /**
     * Lightweight JSON object parser for flat string-to-string maps.
     * Avoids pulling in external JSON libraries.
     */
    static Map<String, String> parseSimpleJsonMap(String json) throws Exception {
        Map<String, String> result = new HashMap<>();
        if (json == null || json.isBlank()) return result;

        String trimmed = json.trim();
        if (!trimmed.startsWith("{") || !trimmed.endsWith("}")) {
            throw new IllegalArgumentException("Expected a JSON object");
        }

        // Strip outer braces
        String inner = trimmed.substring(1, trimmed.length() - 1).trim();
        if (inner.isEmpty()) return result;

        // Split on commas that are not inside strings (simplified — works for flat maps)
        String[] pairs = inner.split(",(?=(?:[^\"]*\"[^\"]*\")*[^\"]*$)");
        for (String pair : pairs) {
            String[] kv = pair.split(":\\s*", 2);
            if (kv.length != 2) continue;
            String key = kv[0].trim().replaceAll("^\"|\"$", "");
            String val = kv[1].trim().replaceAll("^\"|\"$", "");
            result.put(key, val);
        }
        return result;
    }
}

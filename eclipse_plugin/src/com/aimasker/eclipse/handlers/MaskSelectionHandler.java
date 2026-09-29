package com.aimasker.eclipse.handlers;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.jface.dialogs.MessageDialog;
import org.eclipse.jface.text.IDocument;
import org.eclipse.jface.text.ITextSelection;
import org.eclipse.jface.viewers.ISelection;
import org.eclipse.ui.IEditorPart;
import org.eclipse.ui.handlers.HandlerUtil;
import org.eclipse.ui.texteditor.ITextEditor;

import com.aimasker.eclipse.MaskerEngine;
import com.aimasker.eclipse.MaskResult;
import com.aimasker.eclipse.MappingStore;
import com.aimasker.eclipse.views.MappingView;

/**
 * Masks identifiers in the currently selected text.
 * Keybinding: Ctrl+Shift+M
 */
public class MaskSelectionHandler extends AbstractHandler {

    @Override
    public Object execute(ExecutionEvent event) throws ExecutionException {
        IEditorPart editorPart = HandlerUtil.getActiveEditor(event);
        if (!(editorPart instanceof ITextEditor)) {
            MessageDialog.openWarning(
                HandlerUtil.getActiveShell(event),
                "AI Code Masker",
                "Please open a text file to use AI Code Masker."
            );
            return null;
        }

        ITextEditor editor = (ITextEditor) editorPart;
        ISelection selection = HandlerUtil.getCurrentSelection(event);

        if (!(selection instanceof ITextSelection)) {
            MessageDialog.openWarning(
                HandlerUtil.getActiveShell(event),
                "AI Code Masker",
                "Please select some code to mask."
            );
            return null;
        }

        ITextSelection textSelection = (ITextSelection) selection;
        if (textSelection.isEmpty() || textSelection.getText().trim().isEmpty()) {
            MessageDialog.openWarning(
                HandlerUtil.getActiveShell(event),
                "AI Code Masker",
                "Selection is empty. Please select code to mask."
            );
            return null;
        }

        String selectedText = textSelection.getText();
        String filePath     = getFilePath(editor);
        String lang         = MaskerEngine.detectLanguage(filePath);

        MaskResult result = MaskerEngine.maskContent(selectedText, lang);

        // Replace selected text
        IDocument doc = editor.getDocumentProvider().getDocument(editor.getEditorInput());
        try {
            doc.replace(textSelection.getOffset(), textSelection.getLength(), result.maskedCode);
        } catch (Exception e) {
            MessageDialog.openError(
                HandlerUtil.getActiveShell(event),
                "AI Code Masker — Error",
                "Failed to replace text: " + e.getMessage()
            );
            return null;
        }

        // Merge mapping
        MappingStore.getInstance().mergeMapping(filePath, result.mapping);

        // Refresh mapping view
        MappingView.refresh();

        MessageDialog.openInformation(
            HandlerUtil.getActiveShell(event),
            "AI Code Masker",
            "✅ Masked " + result.getMappingCount() + " identifier(s).\n" +
            "Open the Mapping view (Window → Show View → AI Code Masker → Masker Mapping) to review."
        );

        return null;
    }

    static String getFilePath(ITextEditor editor) {
        try {
            org.eclipse.core.resources.IFile file =
                editor.getEditorInput().getAdapter(org.eclipse.core.resources.IFile.class);
            if (file != null) return file.getLocation().toOSString();
        } catch (Exception ignored) {}
        return editor.getEditorInput().getName();
    }
}

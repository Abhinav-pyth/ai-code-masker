package com.aimasker.eclipse.handlers;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.core.resources.IFile;
import org.eclipse.core.resources.IWorkspace;
import org.eclipse.core.resources.ResourcesPlugin;
import org.eclipse.core.runtime.Path;
import org.eclipse.jface.dialogs.MessageDialog;
import org.eclipse.jface.text.IDocument;
import org.eclipse.ui.IEditorPart;
import org.eclipse.ui.handlers.HandlerUtil;
import org.eclipse.ui.texteditor.ITextEditor;

import com.aimasker.eclipse.MaskerEngine;
import com.aimasker.eclipse.MaskResult;
import com.aimasker.eclipse.MappingStore;
import com.aimasker.eclipse.views.MappingView;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;

/**
 * Masks all identifiers in the entire active file.
 * Opens a new compare editor showing original vs. masked.
 */
public class MaskFileHandler extends AbstractHandler {

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

        ITextEditor editor = (ITextEditor) editorPart;
        IDocument doc = editor.getDocumentProvider().getDocument(editor.getEditorInput());
        String content  = doc.get();
        String filePath = MaskSelectionHandler.getFilePath(editor);
        String lang     = MaskerEngine.detectLanguage(filePath);

        MaskResult result = MaskerEngine.maskContent(content, lang);

        // Save masked content to a sibling file: <name>.masked.<ext>
        try {
            String maskedFileName = buildMaskedFileName(filePath);
            IWorkspace workspace = ResourcesPlugin.getWorkspace();
            IFile maskedFile = workspace.getRoot().getFileForLocation(new Path(maskedFileName));

            if (maskedFile == null) {
                // Fallback: save next to original using absolute path
                java.io.File outFile = new java.io.File(maskedFileName);
                java.nio.file.Files.writeString(outFile.toPath(), result.maskedCode, StandardCharsets.UTF_8);
            } else {
                byte[] bytes = result.maskedCode.getBytes(StandardCharsets.UTF_8);
                ByteArrayInputStream stream = new ByteArrayInputStream(bytes);
                if (maskedFile.exists()) {
                    maskedFile.setContents(stream, true, true, null);
                } else {
                    maskedFile.create(stream, true, null);
                }
                // Open the masked file in a new editor
                org.eclipse.ui.ide.IDE.openEditor(
                    HandlerUtil.getActivePart(event).getSite().getPage(),
                    maskedFile
                );
            }
        } catch (Exception e) {
            MessageDialog.openError(
                HandlerUtil.getActiveShell(event),
                "AI Code Masker — Error",
                "Failed to create masked file: " + e.getMessage()
            );
            return null;
        }

        // Store full mapping
        MappingStore.getInstance().setMapping(filePath, result.mapping);
        MappingView.refresh();

        MessageDialog.openInformation(
            HandlerUtil.getActiveShell(event),
            "AI Code Masker",
            "✅ File masked: " + result.getMappingCount() + " identifier(s) protected.\n" +
            "The masked file has been opened in a new editor.\n" +
            "Mapping stored — use Unmask File to restore later."
        );

        return null;
    }

    private String buildMaskedFileName(String originalPath) {
        int dot = originalPath.lastIndexOf('.');
        if (dot > 0) {
            return originalPath.substring(0, dot) + ".masked" + originalPath.substring(dot);
        }
        return originalPath + ".masked";
    }
}

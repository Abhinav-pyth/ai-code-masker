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
import com.aimasker.eclipse.MappingStore;
import com.aimasker.eclipse.views.MappingView;

import java.io.ByteArrayInputStream;
import java.nio.charset.StandardCharsets;
import java.util.Map;

/**
 * Unmasks all identifiers in the entire active file using the stored mapping.
 */
public class UnmaskFileHandler extends AbstractHandler {

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

        ITextEditor editor  = (ITextEditor) editorPart;
        IDocument doc       = editor.getDocumentProvider().getDocument(editor.getEditorInput());
        String content      = doc.get();
        String filePath     = MaskSelectionHandler.getFilePath(editor);
        String lang         = MaskerEngine.detectLanguage(filePath);

        // Get or prompt for mapping
        Map<String, String> mapping = UnmaskSelectionHandler.getOrPromptMapping(event, filePath);
        if (mapping == null || mapping.isEmpty()) return null;

        String restored = MaskerEngine.unmaskContent(content, mapping, lang);

        // Write restored content to a sibling file: <name>.restored.<ext>
        try {
            String restoredFileName = buildRestoredFileName(filePath);
            IWorkspace workspace    = ResourcesPlugin.getWorkspace();
            IFile restoredFile      = workspace.getRoot().getFileForLocation(new Path(restoredFileName));

            if (restoredFile == null) {
                java.io.File outFile = new java.io.File(restoredFileName);
                java.nio.file.Files.writeString(outFile.toPath(), restored, StandardCharsets.UTF_8);
            } else {
                byte[] bytes              = restored.getBytes(StandardCharsets.UTF_8);
                ByteArrayInputStream stream = new ByteArrayInputStream(bytes);
                if (restoredFile.exists()) {
                    restoredFile.setContents(stream, true, true, null);
                } else {
                    restoredFile.create(stream, true, null);
                }
                org.eclipse.ui.ide.IDE.openEditor(
                    HandlerUtil.getActivePart(event).getSite().getPage(),
                    restoredFile
                );
            }
        } catch (Exception e) {
            MessageDialog.openError(
                HandlerUtil.getActiveShell(event),
                "AI Code Masker — Error",
                "Failed to create restored file: " + e.getMessage()
            );
            return null;
        }

        MappingView.refresh();
        MessageDialog.openInformation(
            HandlerUtil.getActiveShell(event),
            "AI Code Masker",
            "✅ File restored! The restored version has been opened in a new editor tab."
        );

        return null;
    }

    private String buildRestoredFileName(String originalPath) {
        // If it's a .masked.<ext> file, strip the .masked part
        originalPath = originalPath.replace(".masked.", ".");
        int dot = originalPath.lastIndexOf('.');
        if (dot > 0) {
            return originalPath.substring(0, dot) + ".restored" + originalPath.substring(dot);
        }
        return originalPath + ".restored";
    }
}

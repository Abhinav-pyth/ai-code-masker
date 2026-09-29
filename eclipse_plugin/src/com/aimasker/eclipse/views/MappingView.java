package com.aimasker.eclipse.views;

import org.eclipse.swt.SWT;
import org.eclipse.swt.dnd.Clipboard;
import org.eclipse.swt.dnd.TextTransfer;
import org.eclipse.swt.dnd.Transfer;
import org.eclipse.swt.events.SelectionAdapter;
import org.eclipse.swt.events.SelectionEvent;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Composite;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Table;
import org.eclipse.swt.widgets.TableColumn;
import org.eclipse.swt.widgets.TableItem;
import org.eclipse.swt.widgets.Text;
import org.eclipse.ui.IEditorPart;
import org.eclipse.ui.IWorkbenchPage;
import org.eclipse.ui.PlatformUI;
import org.eclipse.ui.part.ViewPart;
import org.eclipse.ui.texteditor.ITextEditor;

import com.aimasker.eclipse.MappingStore;
import com.aimasker.eclipse.handlers.MaskSelectionHandler;

import java.util.Map;

/**
 * Eclipse ViewPart that displays the current file's identifier mapping
 * as a sortable table with copy and clear actions.
 */
public class MappingView extends ViewPart implements MappingStore.MappingChangeListener {

    public static final String VIEW_ID = "com.aimasker.eclipse.views.MappingView";

    /** Singleton reference for static refresh calls from handlers */
    private static MappingView instance;

    private Table table;
    private Text jsonText;
    private Label statsLabel;
    private Label fileLabel;

    @Override
    public void createPartControl(Composite parent) {
        instance = this;

        parent.setLayout(new GridLayout(1, false));

        // ─── Header ───────────────────────────────────────────────────────────
        Composite header = new Composite(parent, SWT.NONE);
        header.setLayout(new GridLayout(2, false));
        header.setLayoutData(new GridData(SWT.FILL, SWT.TOP, true, false));

        Label titleLabel = new Label(header, SWT.NONE);
        titleLabel.setText("🔒 AI Code Masker — Mapping");

        statsLabel = new Label(header, SWT.RIGHT);
        statsLabel.setText("0 identifiers");
        statsLabel.setLayoutData(new GridData(SWT.END, SWT.CENTER, true, false));

        fileLabel = new Label(parent, SWT.NONE);
        fileLabel.setText("File: (no file open)");
        fileLabel.setLayoutData(new GridData(SWT.FILL, SWT.TOP, true, false));

        // ─── Action Buttons ───────────────────────────────────────────────────
        Composite buttons = new Composite(parent, SWT.NONE);
        buttons.setLayout(new GridLayout(3, false));
        buttons.setLayoutData(new GridData(SWT.FILL, SWT.TOP, true, false));

        Button copyBtn = new Button(buttons, SWT.PUSH);
        copyBtn.setText("📋 Copy JSON");
        copyBtn.addSelectionListener(new SelectionAdapter() {
            @Override
            public void widgetSelected(SelectionEvent e) {
                copyJsonToClipboard();
            }
        });

        Button refreshBtn = new Button(buttons, SWT.PUSH);
        refreshBtn.setText("🔄 Refresh");
        refreshBtn.addSelectionListener(new SelectionAdapter() {
            @Override
            public void widgetSelected(SelectionEvent e) {
                refreshView();
            }
        });

        Button clearBtn = new Button(buttons, SWT.PUSH);
        clearBtn.setText("🗑 Clear");
        clearBtn.addSelectionListener(new SelectionAdapter() {
            @Override
            public void widgetSelected(SelectionEvent e) {
                clearCurrentMapping();
            }
        });

        // ─── Mapping Table ────────────────────────────────────────────────────
        table = new Table(parent, SWT.BORDER | SWT.FULL_SELECTION | SWT.V_SCROLL | SWT.H_SCROLL);
        table.setHeaderVisible(true);
        table.setLinesVisible(true);
        table.setLayoutData(new GridData(SWT.FILL, SWT.FILL, true, true));

        TableColumn idxCol = new TableColumn(table, SWT.NONE);
        idxCol.setText("#");
        idxCol.setWidth(40);

        TableColumn originalCol = new TableColumn(table, SWT.NONE);
        originalCol.setText("Original Identifier");
        originalCol.setWidth(200);

        TableColumn arrowCol = new TableColumn(table, SWT.CENTER);
        arrowCol.setText("→");
        arrowCol.setWidth(30);

        TableColumn maskedCol = new TableColumn(table, SWT.NONE);
        maskedCol.setText("Masked As");
        maskedCol.setWidth(150);

        // ─── JSON Output ──────────────────────────────────────────────────────
        Label jsonLabel = new Label(parent, SWT.NONE);
        jsonLabel.setText("Raw JSON Map:");
        jsonLabel.setLayoutData(new GridData(SWT.FILL, SWT.TOP, true, false));

        jsonText = new Text(parent, SWT.BORDER | SWT.MULTI | SWT.V_SCROLL | SWT.READ_ONLY);
        GridData jsonGd = new GridData(SWT.FILL, SWT.FILL, true, false);
        jsonGd.heightHint = 120;
        jsonText.setLayoutData(jsonGd);
        jsonText.setText("{}");

        // Register to mapping store changes
        MappingStore.getInstance().addListener(this);

        // Initial load
        refreshView();
    }

    // ─── MappingChangeListener ────────────────────────────────────────────────

    @Override
    public void onMappingChanged(String filePath) {
        Display.getDefault().asyncExec(this::refreshView);
    }

    // ─── Public Static Refresh ────────────────────────────────────────────────

    public static void refresh() {
        if (instance != null) {
            Display.getDefault().asyncExec(instance::refreshView);
        }
    }

    // ─── Internal Refresh ─────────────────────────────────────────────────────

    private void refreshView() {
        if (table == null || table.isDisposed()) return;

        String filePath = getCurrentFilePath();
        fileLabel.setText("File: " + (filePath != null ? filePath : "(none)"));

        Map<String, String> mapping = filePath != null
            ? MappingStore.getInstance().getMapping(filePath)
            : Map.of();

        // Populate table
        table.removeAll();
        int i = 1;
        for (Map.Entry<String, String> entry : mapping.entrySet()) {
            TableItem item = new TableItem(table, SWT.NONE);
            item.setText(0, String.valueOf(i++));
            item.setText(1, entry.getKey());
            item.setText(2, "→");
            item.setText(3, entry.getValue());
        }

        statsLabel.setText(mapping.size() + " identifier" + (mapping.size() != 1 ? "s" : "") + " masked");

        // Build JSON
        jsonText.setText(buildJson(mapping));

        // Resize columns
        for (TableColumn col : table.getColumns()) {
            col.pack();
        }
    }

    private void copyJsonToClipboard() {
        String json = jsonText.getText();
        Clipboard clipboard = new Clipboard(Display.getDefault());
        clipboard.setContents(
            new Object[]{ json },
            new Transfer[]{ TextTransfer.getInstance() }
        );
        clipboard.dispose();
        setPartName("🔒 Mapping (Copied!)");
        Display.getDefault().timerExec(1500, () -> setPartName("🔒 Masker Mapping"));
    }

    private void clearCurrentMapping() {
        String filePath = getCurrentFilePath();
        if (filePath != null) {
            MappingStore.getInstance().clearMapping(filePath);
        } else {
            MappingStore.getInstance().clearAll();
        }
        refreshView();
    }

    private String getCurrentFilePath() {
        try {
            IWorkbenchPage page = PlatformUI.getWorkbench()
                .getActiveWorkbenchWindow().getActivePage();
            if (page == null) return null;

            IEditorPart editor = page.getActiveEditor();
            if (!(editor instanceof ITextEditor)) return null;

            return MaskSelectionHandler.getFilePath((ITextEditor) editor);
        } catch (Exception e) {
            return null;
        }
    }

    private String buildJson(Map<String, String> mapping) {
        if (mapping.isEmpty()) return "{}";
        StringBuilder sb = new StringBuilder("{\n");
        int i = 0;
        for (Map.Entry<String, String> entry : mapping.entrySet()) {
            sb.append("  \"").append(escapeJson(entry.getKey()))
              .append("\": \"").append(escapeJson(entry.getValue())).append("\"");
            if (i++ < mapping.size() - 1) sb.append(",");
            sb.append("\n");
        }
        sb.append("}");
        return sb.toString();
    }

    private String escapeJson(String s) {
        return s.replace("\\", "\\\\").replace("\"", "\\\"");
    }

    @Override
    public void setFocus() {
        table.setFocus();
    }

    @Override
    public void dispose() {
        MappingStore.getInstance().removeListener(this);
        instance = null;
        super.dispose();
    }
}

package com.aimasker.eclipse.handlers;

import org.eclipse.core.commands.AbstractHandler;
import org.eclipse.core.commands.ExecutionEvent;
import org.eclipse.core.commands.ExecutionException;
import org.eclipse.ui.IWorkbenchPage;
import org.eclipse.ui.PartInitException;
import org.eclipse.ui.handlers.HandlerUtil;

import com.aimasker.eclipse.views.MappingView;

/**
 * Opens the Masker Mapping view panel.
 */
public class ShowMappingHandler extends AbstractHandler {

    @Override
    public Object execute(ExecutionEvent event) throws ExecutionException {
        IWorkbenchPage page = HandlerUtil.getActiveWorkbenchWindow(event).getActivePage();
        try {
            page.showView(MappingView.VIEW_ID);
        } catch (PartInitException e) {
            throw new ExecutionException("Failed to open Mapping view", e);
        }
        return null;
    }
}

package com.aimasker.eclipse;

import org.eclipse.ui.plugin.AbstractUIPlugin;
import org.osgi.framework.BundleContext;

/**
 * OSGi bundle activator for the AI Code Masker Eclipse plugin.
 */
public class Activator extends AbstractUIPlugin {

    public static final String PLUGIN_ID = "com.aimasker.eclipse";

    private static Activator plugin;

    @Override
    public void start(BundleContext context) throws Exception {
        super.start(context);
        plugin = this;
    }

    @Override
    public void stop(BundleContext context) throws Exception {
        plugin = null;
        MappingStore.getInstance().clearAll();
        super.stop(context);
    }

    public static Activator getDefault() {
        return plugin;
    }
}

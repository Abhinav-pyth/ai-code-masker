package com.aimasker.eclipse;

import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.ArrayList;
import java.util.List;

/**
 * Thread-safe singleton store for per-file identifier mappings.
 * Keyed by absolute file path.
 */
public class MappingStore {

    /** Listener interface for mapping change events */
    public interface MappingChangeListener {
        void onMappingChanged(String filePath);
    }

    // Singleton
    private static final MappingStore INSTANCE = new MappingStore();
    public static MappingStore getInstance() { return INSTANCE; }

    private final ConcurrentHashMap<String, Map<String, String>> store = new ConcurrentHashMap<>();
    private final List<MappingChangeListener> listeners = Collections.synchronizedList(new ArrayList<>());

    private MappingStore() {}

    // ─── Listener Management ──────────────────────────────────────────────────

    public void addListener(MappingChangeListener listener) {
        listeners.add(listener);
    }

    public void removeListener(MappingChangeListener listener) {
        listeners.remove(listener);
    }

    private void notifyListeners(String filePath) {
        for (MappingChangeListener l : listeners) {
            l.onMappingChanged(filePath);
        }
    }

    // ─── CRUD Operations ──────────────────────────────────────────────────────

    public Map<String, String> getMapping(String filePath) {
        return store.getOrDefault(filePath, Collections.emptyMap());
    }

    public boolean hasMapping(String filePath) {
        return store.containsKey(filePath) && !store.get(filePath).isEmpty();
    }

    public void setMapping(String filePath, Map<String, String> mapping) {
        store.put(filePath, new HashMap<>(mapping));
        notifyListeners(filePath);
    }

    /**
     * Merge new entries into an existing mapping for a file.
     * Existing entries are preserved; new entries are added.
     */
    public void mergeMapping(String filePath, Map<String, String> newEntries) {
        store.merge(filePath, new HashMap<>(newEntries), (existing, incoming) -> {
            Map<String, String> merged = new HashMap<>(existing);
            merged.putAll(incoming);
            return merged;
        });
        notifyListeners(filePath);
    }

    public void clearMapping(String filePath) {
        store.remove(filePath);
        notifyListeners(filePath);
    }

    public void clearAll() {
        store.clear();
        notifyListeners("*");
    }

    public int getMappingCount(String filePath) {
        Map<String, String> m = store.get(filePath);
        return m != null ? m.size() : 0;
    }

    public Map<String, Map<String, String>> getAllMappings() {
        return Collections.unmodifiableMap(store);
    }
}

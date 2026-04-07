package com.aimasker.eclipse;

import java.util.Map;

/**
 * Data class holding the result of a masking operation.
 */
public class MaskResult {

    /** The masked source code with identifiers replaced by placeholders */
    public final String maskedCode;

    /** Mapping from original identifier → masked placeholder */
    public final Map<String, String> mapping;

    public MaskResult(String maskedCode, Map<String, String> mapping) {
        this.maskedCode = maskedCode;
        this.mapping    = mapping;
    }

    /** Count of masked identifiers */
    public int getMappingCount() {
        return mapping.size();
    }
}

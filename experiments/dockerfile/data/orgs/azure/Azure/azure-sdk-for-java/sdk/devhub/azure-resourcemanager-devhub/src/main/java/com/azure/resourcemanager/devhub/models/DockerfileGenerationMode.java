// Copyright (c) Microsoft Corporation. All rights reserved.
// Licensed under the MIT License.
// Code generated by Microsoft (R) AutoRest Code Generator.

package com.azure.resourcemanager.devhub.models;

import com.azure.core.util.ExpandableStringEnum;
import com.fasterxml.jackson.annotation.JsonCreator;
import java.util.Collection;

/** The mode of generation to be used for generating Dockerfiles. */
public final class DockerfileGenerationMode extends ExpandableStringEnum<DockerfileGenerationMode> {
    /** Static value enabled for DockerfileGenerationMode. */
    public static final DockerfileGenerationMode ENABLED = fromString("enabled");

    /** Static value disabled for DockerfileGenerationMode. */
    public static final DockerfileGenerationMode DISABLED = fromString("disabled");

    /**
     * Creates a new instance of DockerfileGenerationMode value.
     *
     * @deprecated Use the {@link #fromString(String)} factory method.
     */
    @Deprecated
    public DockerfileGenerationMode() {
    }

    /**
     * Creates or finds a DockerfileGenerationMode from its string representation.
     *
     * @param name a name to look for.
     * @return the corresponding DockerfileGenerationMode.
     */
    @JsonCreator
    public static DockerfileGenerationMode fromString(String name) {
        return fromString(name, DockerfileGenerationMode.class);
    }

    /**
     * Gets known DockerfileGenerationMode values.
     *
     * @return known DockerfileGenerationMode values.
     */
    public static Collection<DockerfileGenerationMode> values() {
        return values(DockerfileGenerationMode.class);
    }
}
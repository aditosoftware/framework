/*
 * Copyright 2000-2014 Vaadin Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not
 * use this file except in compliance with the License. You may obtain a copy of
 * the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
 * WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
 * License for the specific language governing permissions and limitations under
 * the License.
 */
package com.vaadin.util;

import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.net.URLConnection;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * Provides various helper methods for resource handling. Meant for internal
 * use.
 *
 * @since
 * @author Vaadin Ltd
 */
public final class ResourceHelper {

    /**
     * Get the timestamp for theme at given resourceUrl
     *
     * @param resourceUrl
     *            Theme resource url
     * @return Theme timestamp or -1 if not found.
     */
    public static long getThemeResourceTimestamp(URL resourceUrl) {
        if (resourceUrl == null) {
            return -1;
        }

        // Find the modification timestamp
        URLConnection connection = null;
        try {
            connection = resourceUrl.openConnection();
            return connection.getLastModified();
        } catch (Exception e) {
            getLogger().log(Level.FINEST,
                    "Failed to find out last modified timestamp. Continuing without it.",
                    e);
        } finally {
            try {
                // Explicitly close the input stream to prevent it
                // from remaining hanging
                // http://bugs.sun.com/bugdatabase/view_bug.do?bug_id=4257700
                InputStream is = connection.getInputStream();
                if (is != null) {
                    is.close();
                }
            } catch (FileNotFoundException e) {
                // Not logging when the file does not exist.
            } catch (IOException e) {
                getLogger().log(Level.INFO,
                        "Error closing URLConnection input stream", e);
            }
        }
        return -1;
    }

    private static final Logger getLogger() {
        return Logger.getLogger(ResourceHelper.class.getName());
    }
}

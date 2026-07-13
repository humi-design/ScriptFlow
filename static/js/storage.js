/**
 * ScriptFlow - Storage Module
 * Handles localStorage, session storage, and offline data management
 */

const Storage = {
    PREFIX: 'sf_',

    /**
     * Get item from localStorage
     */
    get(key, defaultValue = null) {
        try {
            const item = localStorage.getItem(this.PREFIX + key);
            if (item === null) return defaultValue;
            return JSON.parse(item);
        } catch (e) {
            console.error('Storage.get error:', e);
            return defaultValue;
        }
    },

    /**
     * Set item in localStorage
     */
    set(key, value) {
        try {
            localStorage.setItem(this.PREFIX + key, JSON.stringify(value));
            return true;
        } catch (e) {
            console.error('Storage.set error:', e);
            // Handle quota exceeded
            if (e.name === 'QuotaExceededError') {
                this.cleanup();
                try {
                    localStorage.setItem(this.PREFIX + key, JSON.stringify(value));
                    return true;
                } catch (e2) {
                    return false;
                }
            }
            return false;
        }
    },

    /**
     * Remove item from localStorage
     */
    remove(key) {
        try {
            localStorage.removeItem(this.PREFIX + key);
            return true;
        } catch (e) {
            return false;
        }
    },

    /**
     * Clear all app data from localStorage
     */
    clear() {
        try {
            const keysToRemove = [];
            for (let i = 0; i < localStorage.length; i++) {
                const key = localStorage.key(i);
                if (key && key.startsWith(this.PREFIX)) {
                    keysToRemove.push(key);
                }
            }
            keysToRemove.forEach(key => localStorage.removeItem(key));
            return true;
        } catch (e) {
            return false;
        }
    },

    /**
     * Cleanup old/unused data
     */
    cleanup() {
        // Remove old drafts
        const drafts = this.get('drafts', {});
        const cleanedDrafts = {};
        const oneWeekAgo = Date.now() - (7 * 24 * 60 * 60 * 1000);
        
        Object.entries(drafts).forEach(([id, draft]) => {
            if (draft.timestamp && draft.timestamp > oneWeekAgo) {
                cleanedDrafts[id] = draft;
            }
        });
        
        this.set('drafts', cleanedDrafts);
    },

    /**
     * Session storage methods
     */
    session: {
        get(key, defaultValue = null) {
            try {
                const item = sessionStorage.getItem(Storage.PREFIX + key);
                return item ? JSON.parse(item) : defaultValue;
            } catch (e) {
                return defaultValue;
            }
        },
        
        set(key, value) {
            try {
                sessionStorage.setItem(Storage.PREFIX + key, JSON.stringify(value));
                return true;
            } catch (e) {
                return false;
            }
        },
        
        remove(key) {
            try {
                sessionStorage.removeItem(Storage.PREFIX + key);
                return true;
            } catch (e) {
                return false;
            }
        }
    },

    /**
     * Draft management
     */
    drafts: {
        save(scriptId, content, title) {
            const drafts = Storage.get('drafts', {});
            drafts[scriptId] = {
                content,
                title,
                timestamp: Date.now()
            };
            return Storage.set('drafts', drafts);
        },
        
        load(scriptId) {
            const drafts = Storage.get('drafts', {});
            return drafts[scriptId] || null;
        },
        
        remove(scriptId) {
            const drafts = Storage.get('drafts', {});
            delete drafts[scriptId];
            return Storage.set('drafts', drafts);
        },
        
        getAll() {
            return Storage.get('drafts', {});
        }
    },

    /**
     * User preferences
     */
    preferences: {
        getAll() {
            return Storage.get('preferences', {
                theme: 'dark',
                fontSize: 48,
                scrollSpeed: 50,
                lineHeight: 1.8,
                gesturesEnabled: true,
                countdown: 5,
                autoSave: true,
                autoRestore: true,
                rememberLastScript: true,
                launchBehavior: 'dashboard'
            });
        },
        
        set(key, value) {
            const prefs = this.getAll();
            prefs[key] = value;
            return Storage.set('preferences', prefs);
        },
        
        get(key, defaultValue = null) {
            const prefs = this.getAll();
            return prefs[key] ?? defaultValue;
        }
    },

    /**
     * Recent scripts cache
     */
    recentScripts: {
        maxItems: 10,
        
        add(script) {
            const recent = this.getAll();
            // Remove if already exists
            const filtered = recent.filter(s => s.id !== script.id);
            // Add to front
            filtered.unshift({
                id: script.id,
                title: script.title,
                wordCount: script.word_count,
                lastOpened: Date.now()
            });
            // Limit size
            const trimmed = filtered.slice(0, this.maxItems);
            Storage.set('recentScripts', trimmed);
        },
        
        getAll() {
            return Storage.get('recentScripts', []);
        },
        
        clear() {
            Storage.remove('recentScripts');
        }
    },

    /**
     * Cache management for offline
     */
    cache: {
        async save(key, data) {
            return Storage.set(`cache_${key}`, {
                data,
                timestamp: Date.now()
            });
        },
        
        async load(key, maxAge = 24 * 60 * 60 * 1000) {
            const cached = Storage.get(`cache_${key}`, null);
            if (!cached) return null;
            
            const age = Date.now() - cached.timestamp;
            if (age > maxAge) {
                Storage.remove(`cache_${key}`);
                return null;
            }
            
            return cached.data;
        },
        
        async invalidate(key) {
            Storage.remove(`cache_${key}`);
        },
        
        async invalidateAll() {
            Object.keys(localStorage)
                .filter(k => k.startsWith(this.PREFIX + 'cache_'))
                .forEach(k => localStorage.removeItem(k));
        }
    },

    /**
     * Get storage usage statistics
     */
    getUsageStats() {
        let totalSize = 0;
        const items = {};
        
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            if (key && key.startsWith(this.PREFIX)) {
                const value = localStorage.getItem(key);
                const size = (key.length + value.length) * 2; // Approximate bytes
                totalSize += size;
                items[key.replace(this.PREFIX, '')] = size;
            }
        }
        
        return {
            totalBytes: totalSize,
            totalFormatted: this.formatBytes(totalSize),
            itemCount: Object.keys(items).length,
            items
        };
    },
    
    formatBytes(bytes) {
        if (bytes === 0) return '0 B';
        const k = 1024;
        const sizes = ['B', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }
};

// Freeze Storage to prevent modifications
Object.freeze(Storage);
Object.freeze(Storage.session);
Object.freeze(Storage.drafts);
Object.freeze(Storage.preferences);
Object.freeze(Storage.recentScripts);
Object.freeze(Storage.cache);

if (typeof module !== 'undefined' && module.exports) {
    module.exports = Storage;
}

const isDevelopment = import.meta.env.MODE === 'development';
const isProduction = import.meta.env.MODE === 'production';

const conf = {
    appwriteUrl: String(import.meta.env.VITE_APPWRITE_URL),
    appwriteProjectId: String(import.meta.env.VITE_APPWRITE_PROJECT_ID),
    appwriteDatabaseId: String(import.meta.env.VITE_APPWRITE_DATABASE_ID),
    appwriteTableId: String(import.meta.env.VITE_APPWRITE_TABLE_ID),
    appwriteBucketId: String(import.meta.env.VITE_APPWRITE_BUCKET_ID),
    tinymceEditorId: String(import.meta.env.VITE_TINYMCE_EDITOR_ID),
    backendApiUrl: String(import.meta.env.VITE_BACKEND_API_URL || 'http://localhost:8000'),
    
    // Environment flags
    isDevelopment,
    isProduction,
    
    // Feature flags
    enableLogging: isDevelopment,
}

// Helper function for conditional logging
export const logger = {
    log: (...args) => {
        if (conf.enableLogging) console.log(...args);
    },
    error: (...args) => {
        if (conf.enableLogging) console.error(...args);
    },
    warn: (...args) => {
        if (conf.enableLogging) console.warn(...args);
    },
};

export default conf;
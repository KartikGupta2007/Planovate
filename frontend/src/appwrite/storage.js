// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Appwrite Storage – Image Upload
// ============================================

// TODO: import { storage } from "./config";
// TODO: import { ID } from "appwrite";

const BUCKET_ID = import.meta.env.VITE_APPWRITE_BUCKET_ID || "";

export const uploadImage = async (file) => {
  // TODO: Implement with Appwrite
  // const response = await storage.createFile(BUCKET_ID, ID.unique(), file);
  // return response.$id;
  return null;
};

export const getImageUrl = (fileId) => {
  // TODO: Implement with Appwrite
  // return storage.getFileView(BUCKET_ID, fileId);
  return "";
};

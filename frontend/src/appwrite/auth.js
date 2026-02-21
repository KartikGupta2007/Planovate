// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Authentication Functions
// ============================================

// TODO: import { account } from "./config";
// TODO: import { ID } from "appwrite";

export const register = async (name, email, password) => {
  // TODO: Implement with Appwrite
  // await account.create(ID.unique(), email, password, name);
  // await account.createEmailPasswordSession(email, password);
  // return await account.get();
};

export const login = async (email, password) => {
  // TODO: Implement with Appwrite
  // await account.createEmailPasswordSession(email, password);
  // return await account.get();
};

export const logout = async () => {
  // TODO: Implement with Appwrite
  // await account.deleteSession("current");
};

export const getCurrentUser = async () => {
  // TODO: Implement with Appwrite
  // return await account.get();
  return null;
};

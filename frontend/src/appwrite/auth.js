// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Authentication Functions
// ============================================

// TODO: import { account } from "./config";
// TODO: import { ID } from "appwrite";

import conf, { logger } from "../Conf/conf.js";
import { Client, Account, ID } from "appwrite";

export class AuthService {
    client = new Client();
    account;
    constructor(){
        this.client
            .setEndpoint(conf.appwriteUrl)
            .setProject(conf.appwriteProjectId); 
        this.account = new Account(this.client);
    }
    async createAccount({email, password, name}){
        try {
            const user = await this.account.create({
                userId: ID.unique(),
                email: email,
                password: password,
                name:name
            });
            if(user){
                return await this.login({email, password});
            }else{
                return user;
            }
        } 
        catch (error) {
            logger.log(error);
            // Handle specific error cases
            if (error.code === 409 || error.message.includes('user_already_exists') || error.message.includes('already exists')) {
                throw new Error('A user with this email already exists. Please login or use a different email.');
            }
            throw new Error(error.message || 'Failed to create account. Please try again.');
        }
    }

    async login({email,password}){
        try{
            return await this.account.createEmailPasswordSession({
                email: email,
                password: password
            });
        }
        catch(error){
            logger.log(error);
            if (error.code === 401 || error.message.includes('Invalid credentials')) {
                throw new Error('Invalid email or password. Please try again.');
            }
            throw new Error(error.message || 'Login failed. Please try again.');
        }
    }
    
    async getCurrentUser(){
        try{
            return await this.account.get();
        }
        catch(error){
            logger.log(error);
            return null;
        }
    }

    async logout(){
        try{
            await this.account.deleteSessions();
        }
        catch(error){
            logger.log(error);
        }
    }
}

const authService = new AuthService();
export default authService;

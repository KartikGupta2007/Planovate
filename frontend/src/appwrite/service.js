// ============================================
// OWNER: Member 1 – Frontend + Appwrite
// FILE: Appwrite Storage – Image Upload
// ============================================
import conf from "../Conf/conf";
import { Client, ID, TablesDB, Storage , Query } from "appwrite";

export class Service{
    client = new Client();
    tablesDB;
    bucket;
    
    constructor(){
        this.client
            .setEndpoint(conf.appwriteUrl)
            .setProject(conf.appwriteProjectId); 
        this.tablesDB = new TablesDB(this.client);
        this.bucket = new Storage(this.client);
    }
    async uploadImage (file){
        try {
            return await this.bucket.createFile({
                bucketId: conf.appwriteBucketId,
                fileId: ID.unique(),
                file: file
            })
        } catch (error) {
            console.log(error)
            return null;
        }
    }
    
    async getAllRows(){
        try{
            return await this.tablesDB.listRows({
                databaseId: conf.appwriteDatabaseId,
                tableId: conf.appwriteTableId,
            })
        }
        catch(error){
            console.log(error)
            return null;
        }
    }

    async getUserRows(userId){
        try{
            return await this.tablesDB.listRows({
                databaseId: conf.appwriteDatabaseId,
                tableId: conf.appwriteTableId,
                queries:[
                    Query.equal("UserId", userId)
                ]
            })
        }
        catch(error){
            console.log("Get user rows error:", error)
            return null;
        }
    }
    async getRow(rowId){
        try{
            return await this.tablesDB.getRow({
                databaseId: conf.appwriteDatabaseId,
                tableId: conf.appwriteTableId,
                rowId: rowId
            })
        }
        catch(error){
            console.log(error)
            return null;
        }
    }

    async createRow({title,city,currentImage,idealImage,budget,description,userId}){
        try{
            return await this.tablesDB.createRow({
                databaseId: conf.appwriteDatabaseId,
                tableId: conf.appwriteTableId,
                rowId: ID.unique(),
                data: {
                    Title: title,
                    City: city,
                    CurrentPhoto: currentImage,
                    Idealphoto: idealImage,
                    Budget: budget,
                    Description: description,
                    UserId: userId
                }
            })
        }
        catch(error){
            console.log("Create row error:", error)
            return null;
        }
    }

    async updateRow({rowId,title,city,currentImage,idealImage,budget,description,userId}){
        try{
            return await this.tablesDB.updateRow({
                databaseId: conf.appwriteDatabaseId,
                tableId: conf.appwriteTableId,
                rowId: rowId,
                data: {
                    Title: title,
                    City: city,
                    CurrentPhoto: currentImage,
                    Idealphoto: idealImage,
                    Budget: budget,
                    Description: description,
                    UserId: userId
                }
            })
        }
        catch(error){
            console.log("Update row error:", error)
            return null;
        }
    }

    getFilePreview(fileId){
        try{
            return this.bucket.getFilePreview({
                bucketId: conf.appwriteBucketId,
                fileId: fileId,
                width: 400,
                height: 300,
                gravity: 'center',
                quality: 80
            })
        }
        catch(error){
            console.log(error)
            return null;
        }
    }

    getFileView(fileId){
        try{
            return this.bucket.getFileView({
                bucketId: conf.appwriteBucketId,
                fileId: fileId
            })
        }
        catch(error){
            console.log(error)
            return null;
        }
    }

    getFileDownload(fileId){
        try{
            return this.bucket.getFileDownload({
                bucketId: conf.appwriteBucketId,
                fileId: fileId
            })
        }
        catch(error){
            console.log(error)
            return null;
        }
    }
}


const service = new Service();
export default service;
"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.AppDataSource = void 0;
require("reflect-metadata");
const typeorm_1 = require("typeorm");
const User_1 = require("./entities/User");
const Collection_1 = require("./entities/Collection");
const Transaction_1 = require("./entities/Transaction");
const GalleryItem_1 = require("./entities/GalleryItem");
const AppDocument_1 = require("./entities/AppDocument");
const FoundationInfo_1 = require("./entities/FoundationInfo");
const dotenv_1 = __importDefault(require("dotenv"));
dotenv_1.default.config();
exports.AppDataSource = new typeorm_1.DataSource({
    type: "postgres",
    host: process.env.DB_HOST || "localhost",
    port: parseInt(process.env.DB_PORT || "5432"),
    username: process.env.DB_USERNAME || "postgres",
    password: process.env.DB_PASSWORD || "postgres",
    database: process.env.DB_NAME || "charity_db",
    synchronize: true, // Set to false in production
    logging: false,
    entities: [User_1.User, Collection_1.Collection, Transaction_1.Transaction, GalleryItem_1.GalleryItem, AppDocument_1.AppDocument, FoundationInfo_1.FoundationInfo],
    migrations: [],
    subscribers: [],
});

import "reflect-metadata";
import { DataSource } from "typeorm";
import { User } from "./entities/User";
import { Collection } from "./entities/Collection";
import { Transaction } from "./entities/Transaction";
import { GalleryItem } from "./entities/GalleryItem";
import { AppDocument } from "./entities/AppDocument";
import { FoundationInfo } from "./entities/FoundationInfo";
import { Partner } from "./entities/Partner";
import { ProjectUpdate } from "./entities/ProjectUpdate";
import { News } from "./entities/News";
import dotenv from "dotenv";

dotenv.config();

export const AppDataSource = new DataSource({
  type: "postgres",
  host: process.env.DB_HOST || "localhost",
  port: parseInt(process.env.DB_PORT || "5432"),
  username: process.env.DB_USERNAME || "postgres",
  password: process.env.DB_PASSWORD || "postgres",
  database: process.env.DB_NAME || "charity_db",
  synchronize: true, // Set to false in production
  logging: false,
  entities: [User, Collection, Transaction, GalleryItem, AppDocument, FoundationInfo, Partner, ProjectUpdate, News],
  migrations: [],
  subscribers: [],
});


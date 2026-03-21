import { Request, Response } from "express";
import { CollectionService } from "../services/CollectionService";
import { AppDataSource } from "../data-source";
import { Transaction } from "../entities/Transaction";

export class AdminController {
  private collectionService = new CollectionService();
  private transactionRepository = AppDataSource.getRepository(Transaction);

  login = async (req: Request, res: Response) => {
    const { login, password } = req.body;
    if (login === "123" && password === "123") {
      res.json({ token: "admin-secret-token", message: "Success" });
    } else {
      res.status(401).json({ message: "Invalid credentials" });
    }
  };

  getDashboardStats = async (req: Request, res: Response) => {
    try {
      const totalRaised = await this.transactionRepository
        .createQueryBuilder("transaction")
        .select("SUM(transaction.amount)", "sum")
        .where("transaction.status = :status", { status: "completed" })
        .getRawOne();

      const collectionsCount = await this.collectionService.getAllActive();

      res.json({
        totalRaised: totalRaised.sum || 0,
        activeCollections: collectionsCount.length,
      });
    } catch (error) {
      res.status(500).json({ message: "Error fetching admin stats" });
    }
  };

  createCollection = async (req: Request, res: Response) => {
    try {
      const collection = await this.collectionService.create(req.body);
      res.status(201).json(collection);
    } catch (error) {
      res.status(500).json({ message: "Error creating collection" });
    }
  };
}


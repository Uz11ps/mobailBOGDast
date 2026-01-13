import { Request, Response } from "express";
import { CollectionService } from "../services/CollectionService";

export class CollectionController {
  private collectionService = new CollectionService();

  getAll = async (req: Request, res: Response) => {
    try {
      const collections = await this.collectionService.getAllActive();
      res.json(collections);
    } catch (error) {
      res.status(500).json({ message: "Error fetching collections" });
    }
  };

  getOne = async (req: Request, res: Response) => {
    try {
      const collection = await this.collectionService.getById(req.params.id as string);
      if (!collection) {
        return res.status(404).json({ message: "Collection not found" });
      }
      res.json(collection);
    } catch (error) {
      res.status(500).json({ message: "Error fetching collection" });
    }
  };

  create = async (req: Request, res: Response) => {
    try {
      const collection = await this.collectionService.create(req.body);
      res.status(201).json(collection);
    } catch (error) {
      res.status(500).json({ message: "Error creating collection" });
    }
  };

  update = async (req: Request, res: Response) => {
    try {
      const collection = await this.collectionService.update(req.params.id, req.body);
      res.json(collection);
    } catch (error) {
      res.status(500).json({ message: "Error updating collection" });
    }
  };
}


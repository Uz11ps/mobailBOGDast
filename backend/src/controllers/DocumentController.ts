import { Request, Response } from "express";
import { AppDataSource } from "../data-source";
import { AppDocument } from "../entities/AppDocument";

export class DocumentController {
  private documentRepository = AppDataSource.getRepository(AppDocument);

  getAll = async (req: Request, res: Response) => {
    const docs = await this.documentRepository.find({ order: { createdAt: "DESC" } });
    res.json(docs);
  };

  create = async (req: Request, res: Response) => {
    const doc = this.documentRepository.create(req.body as object);
    await this.documentRepository.save(doc);
    res.status(201).json(doc);
  };

  delete = async (req: Request, res: Response) => {
    await this.documentRepository.delete(req.params.id);
    res.status(204).send();
  };
}

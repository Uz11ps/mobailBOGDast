import { Request, Response } from "express";
import { AppDataSource } from "../data-source";
import { News } from "../entities/News";

export class NewsController {
  private newsRepository = AppDataSource.getRepository(News);

  getAll = async (req: Request, res: Response) => {
    const news = await this.newsRepository.find({ order: { createdAt: "DESC" } });
    res.json(news);
  };

  create = async (req: Request, res: Response) => {
    const news = this.newsRepository.create(req.body as object);
    await this.newsRepository.save(news);
    res.status(201).json(news);
  };

  delete = async (req: Request, res: Response) => {
    await this.newsRepository.delete(req.params.id);
    res.status(204).send();
  };
}

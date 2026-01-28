import { Request, Response } from "express";
import { AppDataSource } from "../data-source";
import { GalleryItem } from "../entities/GalleryItem";

export class GalleryController {
  private galleryRepository = AppDataSource.getRepository(GalleryItem);

  getAll = async (req: Request, res: Response) => {
    const items = await this.galleryRepository.find({ order: { createdAt: "DESC" } });
    res.json(items);
  };

  create = async (req: Request, res: Response) => {
    const item = this.galleryRepository.create(req.body);
    await this.galleryRepository.save(item);
    res.status(201).json(item);
  };

  delete = async (req: Request, res: Response) => {
    await this.galleryRepository.delete(req.params.id);
    res.status(204).send();
  };
}





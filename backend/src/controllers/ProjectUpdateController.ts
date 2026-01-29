import { Request, Response } from "express";
import { AppDataSource } from "../data-source";
import { ProjectUpdate } from "../entities/ProjectUpdate";

export class ProjectUpdateController {
  private updateRepository = AppDataSource.getRepository(ProjectUpdate);

  getByCollection = async (req: Request, res: Response) => {
    const updates = await this.updateRepository.find({
      where: { collection: { id: req.params.collectionId } },
      order: { createdAt: "DESC" }
    });
    res.json(updates);
  };

  create = async (req: Request, res: Response) => {
    const update = this.updateRepository.create(req.body as object);
    await this.updateRepository.save(update);
    res.status(201).json(update);
  };

  delete = async (req: Request, res: Response) => {
    await this.updateRepository.delete(req.params.id);
    res.status(204).send();
  };
}

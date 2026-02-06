import { Request, Response } from "express";
import { AppDataSource } from "../data-source";
import { Story } from "../entities/Story";

export class StoryController {
  private storyRepository = AppDataSource.getRepository(Story);

  getAll = async (req: Request, res: Response) => {
    const stories = await this.storyRepository.find({ order: { createdAt: "DESC" } });
    res.json(stories);
  };

  create = async (req: Request, res: Response) => {
    const story = this.storyRepository.create(req.body as object);
    await this.storyRepository.save(story);
    res.status(201).json(story);
  };

  delete = async (req: Request, res: Response) => {
    await this.storyRepository.delete(req.params.id);
    res.status(204).send();
  };
}

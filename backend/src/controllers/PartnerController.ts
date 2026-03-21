import { Request, Response } from "express";
import { AppDataSource } from "../data-source";
import { Partner } from "../entities/Partner";

export class PartnerController {
  private partnerRepository = AppDataSource.getRepository(Partner);

  getAll = async (req: Request, res: Response) => {
    const partners = await this.partnerRepository.find({ order: { createdAt: "ASC" } });
    res.json(partners);
  };

  create = async (req: Request, res: Response) => {
    const partner = this.partnerRepository.create(req.body as object);
    await this.partnerRepository.save(partner);
    res.status(201).json(partner);
  };

  delete = async (req: Request, res: Response) => {
    await this.partnerRepository.delete(req.params.id);
    res.status(204).send();
  };
}

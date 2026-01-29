import { Request, Response } from "express";
import { DeepPartial } from "typeorm";
import { AppDataSource } from "../data-source";
import { FoundationInfo } from "../entities/FoundationInfo";

export class FoundationController {
  private foundationRepository = AppDataSource.getRepository(FoundationInfo);

  getInfo = async (req: Request, res: Response) => {
    let info = await this.foundationRepository.findOne({ where: { id: 1 } });
    if (!info) {
      info = this.foundationRepository.create({
        id: 1,
        aboutText: "Благотворительный фонд «Новая жизнь»",
        historyText: "Основан в 2026 году...",
        leadershipText: "Руководитель: ...",
        frenchConnectionText: "Российский партнер французской ассоциации «Nouvelle Vie»"
      });
      await this.foundationRepository.save(info);
    }
    res.json(info);
  };

  updateInfo = async (req: Request, res: Response) => {
    let info = await this.foundationRepository.findOne({ where: { id: 1 } });
    if (info) {
      Object.assign(info, req.body);
      await this.foundationRepository.save(info);
    } else {
      const newInfo = this.foundationRepository.create({ ...req.body, id: 1 } as DeepPartial<FoundationInfo>);
      info = await this.foundationRepository.save(newInfo);
    }
    res.json(info);
  };
}

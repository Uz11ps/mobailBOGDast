import { AppDataSource } from "../data-source";
import { Collection, CollectionStatus } from "../entities/Collection";

export class CollectionService {
  private collectionRepository = AppDataSource.getRepository(Collection);

  async getAllActive() {
    return await this.collectionRepository.find({
      where: { status: CollectionStatus.ACTIVE },
      order: { createdAt: "DESC" },
    });
  }

  async getById(id: string) {
    return await this.collectionRepository.findOne({
      where: { id },
    });
  }

  async create(data: Partial<Collection>) {
    const collection = this.collectionRepository.create(data);
    return await this.collectionRepository.save(collection);
  }
}


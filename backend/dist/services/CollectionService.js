"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.CollectionService = void 0;
const data_source_1 = require("../data-source");
const Collection_1 = require("../entities/Collection");
class CollectionService {
    constructor() {
        this.collectionRepository = data_source_1.AppDataSource.getRepository(Collection_1.Collection);
    }
    getAllActive() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.collectionRepository.find({
                where: { status: Collection_1.CollectionStatus.ACTIVE },
                order: { createdAt: "DESC" },
            });
        });
    }
    getById(id) {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.collectionRepository.findOne({
                where: { id },
            });
        });
    }
    create(data) {
        return __awaiter(this, void 0, void 0, function* () {
            const collection = this.collectionRepository.create(data);
            return yield this.collectionRepository.save(collection);
        });
    }
    update(id, data) {
        return __awaiter(this, void 0, void 0, function* () {
            yield this.collectionRepository.update(id, data);
            return yield this.collectionRepository.findOne({ where: { id } });
        });
    }
}
exports.CollectionService = CollectionService;

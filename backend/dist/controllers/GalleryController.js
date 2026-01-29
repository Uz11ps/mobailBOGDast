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
exports.GalleryController = void 0;
const data_source_1 = require("../data-source");
const GalleryItem_1 = require("../entities/GalleryItem");
class GalleryController {
    constructor() {
        this.galleryRepository = data_source_1.AppDataSource.getRepository(GalleryItem_1.GalleryItem);
        this.getAll = (req, res) => __awaiter(this, void 0, void 0, function* () {
            const items = yield this.galleryRepository.find({ order: { createdAt: "DESC" } });
            res.json(items);
        });
        this.create = (req, res) => __awaiter(this, void 0, void 0, function* () {
            const item = this.galleryRepository.create(req.body);
            yield this.galleryRepository.save(item);
            res.status(201).json(item);
        });
        this.delete = (req, res) => __awaiter(this, void 0, void 0, function* () {
            yield this.galleryRepository.delete(req.params.id);
            res.status(204).send();
        });
    }
}
exports.GalleryController = GalleryController;

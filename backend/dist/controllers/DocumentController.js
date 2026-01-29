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
exports.DocumentController = void 0;
const data_source_1 = require("../data-source");
const AppDocument_1 = require("../entities/AppDocument");
class DocumentController {
    constructor() {
        this.documentRepository = data_source_1.AppDataSource.getRepository(AppDocument_1.AppDocument);
        this.getAll = (req, res) => __awaiter(this, void 0, void 0, function* () {
            const docs = yield this.documentRepository.find({ order: { createdAt: "DESC" } });
            res.json(docs);
        });
        this.create = (req, res) => __awaiter(this, void 0, void 0, function* () {
            const doc = this.documentRepository.create(req.body);
            yield this.documentRepository.save(doc);
            res.status(201).json(doc);
        });
        this.delete = (req, res) => __awaiter(this, void 0, void 0, function* () {
            yield this.documentRepository.delete(req.params.id);
            res.status(204).send();
        });
    }
}
exports.DocumentController = DocumentController;

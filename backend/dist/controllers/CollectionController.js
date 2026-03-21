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
exports.CollectionController = void 0;
const CollectionService_1 = require("../services/CollectionService");
class CollectionController {
    constructor() {
        this.collectionService = new CollectionService_1.CollectionService();
        this.getAll = (req, res) => __awaiter(this, void 0, void 0, function* () {
            try {
                const collections = yield this.collectionService.getAllActive();
                res.json(collections);
            }
            catch (error) {
                res.status(500).json({ message: "Error fetching collections" });
            }
        });
        this.getOne = (req, res) => __awaiter(this, void 0, void 0, function* () {
            try {
                const collection = yield this.collectionService.getById(req.params.id);
                if (!collection) {
                    return res.status(404).json({ message: "Collection not found" });
                }
                res.json(collection);
            }
            catch (error) {
                res.status(500).json({ message: "Error fetching collection" });
            }
        });
        this.create = (req, res) => __awaiter(this, void 0, void 0, function* () {
            try {
                const collection = yield this.collectionService.create(req.body);
                res.status(201).json(collection);
            }
            catch (error) {
                res.status(500).json({ message: "Error creating collection" });
            }
        });
        this.update = (req, res) => __awaiter(this, void 0, void 0, function* () {
            try {
                const collection = yield this.collectionService.update(req.params.id, req.body);
                res.json(collection);
            }
            catch (error) {
                res.status(500).json({ message: "Error updating collection" });
            }
        });
    }
}
exports.CollectionController = CollectionController;

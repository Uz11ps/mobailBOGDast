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
exports.AdminController = void 0;
const CollectionService_1 = require("../services/CollectionService");
const data_source_1 = require("../data-source");
const Transaction_1 = require("../entities/Transaction");
class AdminController {
    constructor() {
        this.collectionService = new CollectionService_1.CollectionService();
        this.transactionRepository = data_source_1.AppDataSource.getRepository(Transaction_1.Transaction);
        this.login = (req, res) => __awaiter(this, void 0, void 0, function* () {
            const { login, password } = req.body;
            if (login === "123" && password === "123") {
                res.json({ token: "admin-secret-token", message: "Success" });
            }
            else {
                res.status(401).json({ message: "Invalid credentials" });
            }
        });
        this.getDashboardStats = (req, res) => __awaiter(this, void 0, void 0, function* () {
            try {
                const totalRaised = yield this.transactionRepository
                    .createQueryBuilder("transaction")
                    .select("SUM(transaction.amount)", "sum")
                    .where("transaction.status = :status", { status: "completed" })
                    .getRawOne();
                const collectionsCount = yield this.collectionService.getAllActive();
                res.json({
                    totalRaised: totalRaised.sum || 0,
                    activeCollections: collectionsCount.length,
                });
            }
            catch (error) {
                res.status(500).json({ message: "Error fetching admin stats" });
            }
        });
        this.createCollection = (req, res) => __awaiter(this, void 0, void 0, function* () {
            try {
                const collection = yield this.collectionService.create(req.body);
                res.status(201).json(collection);
            }
            catch (error) {
                res.status(500).json({ message: "Error creating collection" });
            }
        });
    }
}
exports.AdminController = AdminController;

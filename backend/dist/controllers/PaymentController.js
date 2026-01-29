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
exports.PaymentController = void 0;
const data_source_1 = require("../data-source");
const Transaction_1 = require("../entities/Transaction");
const Collection_1 = require("../entities/Collection");
class PaymentController {
    constructor() {
        this.transactionRepository = data_source_1.AppDataSource.getRepository(Transaction_1.Transaction);
        this.collectionRepository = data_source_1.AppDataSource.getRepository(Collection_1.Collection);
        this.createIntent = (req, res) => __awaiter(this, void 0, void 0, function* () {
            try {
                const { collectionId, amount } = req.body;
                const userId = req.user.id;
                const collection = yield this.collectionRepository.findOne({ where: { id: collectionId } });
                if (!collection) {
                    return res.status(404).json({ message: "Collection not found" });
                }
                const transaction = this.transactionRepository.create({
                    user: req.user,
                    collection,
                    amount,
                    status: Transaction_1.TransactionStatus.PENDING,
                });
                yield this.transactionRepository.save(transaction);
                // Here you would normally call CloudPayments/YooKassa API to get a payment session
                // For now we return the transaction ID as a "payment intent"
                res.json({
                    transactionId: transaction.id,
                    message: "Intent created",
                });
            }
            catch (error) {
                res.status(500).json({ message: "Error creating payment intent" });
            }
        });
        this.confirmPayment = (req, res) => __awaiter(this, void 0, void 0, function* () {
            try {
                const { transactionId, paymentId } = req.body;
                const transaction = yield this.transactionRepository.findOne({
                    where: { id: transactionId },
                    relations: ["collection"],
                });
                if (!transaction) {
                    return res.status(404).json({ message: "Transaction not found" });
                }
                transaction.status = Transaction_1.TransactionStatus.COMPLETED;
                transaction.paymentId = paymentId;
                yield this.transactionRepository.save(transaction);
                // Update collection raised amount
                const collection = transaction.collection;
                collection.raisedAmount = Number(collection.raisedAmount) + Number(transaction.amount);
                yield this.collectionRepository.save(collection);
                res.json({ message: "Payment confirmed", collection });
            }
            catch (error) {
                res.status(500).json({ message: "Error confirming payment" });
            }
        });
    }
}
exports.PaymentController = PaymentController;

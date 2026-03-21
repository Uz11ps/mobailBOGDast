import { Request, Response } from "express";
import { AppDataSource } from "../data-source";
import { Transaction, TransactionStatus } from "../entities/Transaction";
import { Collection } from "../entities/Collection";

export class PaymentController {
  private transactionRepository = AppDataSource.getRepository(Transaction);
  private collectionRepository = AppDataSource.getRepository(Collection);

  createIntent = async (req: any, res: Response) => {
    try {
      const { collectionId, amount } = req.body;
      const userId = req.user.id;

      const collection = await this.collectionRepository.findOne({ where: { id: collectionId } });
      if (!collection) {
        return res.status(404).json({ message: "Collection not found" });
      }

      const transaction = this.transactionRepository.create({
        user: req.user,
        collection,
        amount,
        status: TransactionStatus.PENDING,
      });

      await this.transactionRepository.save(transaction);

      // Here you would normally call CloudPayments/YooKassa API to get a payment session
      // For now we return the transaction ID as a "payment intent"
      res.json({
        transactionId: transaction.id,
        message: "Intent created",
      });
    } catch (error) {
      res.status(500).json({ message: "Error creating payment intent" });
    }
  };

  confirmPayment = async (req: Request, res: Response) => {
    try {
      const { transactionId, paymentId } = req.body;
      const transaction = await this.transactionRepository.findOne({
        where: { id: transactionId },
        relations: ["collection"],
      });

      if (!transaction) {
        return res.status(404).json({ message: "Transaction not found" });
      }

      transaction.status = TransactionStatus.COMPLETED;
      transaction.paymentId = paymentId;
      await this.transactionRepository.save(transaction);

      // Update collection raised amount
      const collection = transaction.collection;
      collection.raisedAmount = Number(collection.raisedAmount) + Number(transaction.amount);
      await this.collectionRepository.save(collection);

      res.json({ message: "Payment confirmed", collection });
    } catch (error) {
      res.status(500).json({ message: "Error confirming payment" });
    }
  };

  getMyDonations = async (req: any, res: Response) => {
    try {
      const donations = await this.transactionRepository.find({
        where: { user: { id: req.user.id }, status: TransactionStatus.COMPLETED },
        relations: ["collection"],
        order: { createdAt: "DESC" }
      });
      res.json(donations);
    } catch (error) {
      res.status(500).json({ message: "Error fetching donations" });
    }
  };
}





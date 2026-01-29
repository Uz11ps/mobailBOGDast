import "reflect-metadata";
import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import { AppDataSource } from "./data-source";
import collectionRoutes from "./routes/collectionRoutes";
import authRoutes from "./routes/authRoutes";
import paymentRoutes from "./routes/paymentRoutes";
import adminRoutes from "./routes/adminRoutes";
import galleryRoutes from "./routes/galleryRoutes";
import documentRoutes from "./routes/documentRoutes";
import foundationRoutes from "./routes/foundationRoutes";
import partnerRoutes from "./routes/partnerRoutes";
import projectUpdateRoutes from "./routes/projectUpdateRoutes";

dotenv.config();

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.use("/api/collections", collectionRoutes);
app.use("/api/auth", authRoutes);
app.use("/api/payments", paymentRoutes);
app.use("/api/admin", adminRoutes);
app.use("/api/gallery", galleryRoutes);
app.use("/api/documents", documentRoutes);
app.use("/api/foundation", foundationRoutes);
app.use("/api/partners", partnerRoutes);
app.use("/api/project-updates", projectUpdateRoutes);

app.get("/", (req, res) => {
  res.send("Charity API is running");
});

AppDataSource.initialize()
  .then(() => {
    console.log("Database connected");
    app.listen(Number(port), "0.0.0.0", () => {
      console.log(`Server is running on port ${port}`);
    });
  })
  .catch((error) => console.log("Database connection error:", error));


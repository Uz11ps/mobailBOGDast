"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
require("reflect-metadata");
const express_1 = __importDefault(require("express"));
const cors_1 = __importDefault(require("cors"));
const dotenv_1 = __importDefault(require("dotenv"));
const data_source_1 = require("./data-source");
const collectionRoutes_1 = __importDefault(require("./routes/collectionRoutes"));
const authRoutes_1 = __importDefault(require("./routes/authRoutes"));
const paymentRoutes_1 = __importDefault(require("./routes/paymentRoutes"));
const adminRoutes_1 = __importDefault(require("./routes/adminRoutes"));
const galleryRoutes_1 = __importDefault(require("./routes/galleryRoutes"));
const documentRoutes_1 = __importDefault(require("./routes/documentRoutes"));
const foundationRoutes_1 = __importDefault(require("./routes/foundationRoutes"));
dotenv_1.default.config();
const app = (0, express_1.default)();
const port = process.env.PORT || 3000;
app.use((0, cors_1.default)());
app.use(express_1.default.json());
app.use("/api/collections", collectionRoutes_1.default);
app.use("/api/auth", authRoutes_1.default);
app.use("/api/payments", paymentRoutes_1.default);
app.use("/api/admin", adminRoutes_1.default);
app.use("/api/gallery", galleryRoutes_1.default);
app.use("/api/documents", documentRoutes_1.default);
app.use("/api/foundation", foundationRoutes_1.default);
app.get("/", (req, res) => {
    res.send("Charity API is running");
});
data_source_1.AppDataSource.initialize()
    .then(() => {
    console.log("Database connected");
    app.listen(Number(port), "0.0.0.0", () => {
        console.log(`Server is running on port ${port}`);
    });
})
    .catch((error) => console.log("Database connection error:", error));

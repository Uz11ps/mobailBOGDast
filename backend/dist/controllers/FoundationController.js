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
exports.FoundationController = void 0;
const data_source_1 = require("../data-source");
const FoundationInfo_1 = require("../entities/FoundationInfo");
class FoundationController {
    constructor() {
        this.foundationRepository = data_source_1.AppDataSource.getRepository(FoundationInfo_1.FoundationInfo);
        this.getInfo = (req, res) => __awaiter(this, void 0, void 0, function* () {
            let info = yield this.foundationRepository.findOne({ where: { id: 1 } });
            if (!info) {
                info = this.foundationRepository.create({
                    id: 1,
                    aboutText: "Благотворительный фонд «Новая жизнь»",
                    historyText: "Основан в 2026 году...",
                    leadershipText: "Руководитель: ...",
                    frenchConnectionText: "Российский партнер французской ассоциации «Nouvelle Vie»"
                });
                yield this.foundationRepository.save(info);
            }
            res.json(info);
        });
        this.updateInfo = (req, res) => __awaiter(this, void 0, void 0, function* () {
            let info = yield this.foundationRepository.findOne({ where: { id: 1 } });
            if (info) {
                Object.assign(info, req.body);
                yield this.foundationRepository.save(info);
            }
            else {
                const newInfo = this.foundationRepository.create(Object.assign(Object.assign({}, req.body), { id: 1 }));
                info = yield this.foundationRepository.save(newInfo);
            }
            res.json(info);
        });
    }
}
exports.FoundationController = FoundationController;

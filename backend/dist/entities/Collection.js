"use strict";
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.Collection = exports.CollectionStatus = void 0;
const typeorm_1 = require("typeorm");
var CollectionStatus;
(function (CollectionStatus) {
    CollectionStatus["ACTIVE"] = "active";
    CollectionStatus["CLOSED"] = "closed";
})(CollectionStatus || (exports.CollectionStatus = CollectionStatus = {}));
let Collection = class Collection {
};
exports.Collection = Collection;
__decorate([
    (0, typeorm_1.PrimaryGeneratedColumn)("uuid"),
    __metadata("design:type", String)
], Collection.prototype, "id", void 0);
__decorate([
    (0, typeorm_1.Column)(),
    __metadata("design:type", String)
], Collection.prototype, "title", void 0);
__decorate([
    (0, typeorm_1.Column)("text"),
    __metadata("design:type", String)
], Collection.prototype, "description", void 0);
__decorate([
    (0, typeorm_1.Column)("decimal", { precision: 12, scale: 2 }),
    __metadata("design:type", Number)
], Collection.prototype, "goalAmount", void 0);
__decorate([
    (0, typeorm_1.Column)("decimal", { precision: 12, scale: 2, default: 0 }),
    __metadata("design:type", Number)
], Collection.prototype, "raisedAmount", void 0);
__decorate([
    (0, typeorm_1.Column)({ nullable: true }),
    __metadata("design:type", String)
], Collection.prototype, "imageUrl", void 0);
__decorate([
    (0, typeorm_1.Column)({ nullable: true }),
    __metadata("design:type", String)
], Collection.prototype, "country", void 0);
__decorate([
    (0, typeorm_1.Column)({ nullable: true }),
    __metadata("design:type", String)
], Collection.prototype, "category", void 0);
__decorate([
    (0, typeorm_1.Column)({
        type: "enum",
        enum: CollectionStatus,
        default: CollectionStatus.ACTIVE,
    }),
    __metadata("design:type", String)
], Collection.prototype, "status", void 0);
__decorate([
    (0, typeorm_1.CreateDateColumn)(),
    __metadata("design:type", Date)
], Collection.prototype, "createdAt", void 0);
exports.Collection = Collection = __decorate([
    (0, typeorm_1.Entity)()
], Collection);

import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from "typeorm";

export enum CollectionStatus {
  ACTIVE = "active",
  CLOSED = "closed",
}

@Entity()
export class Collection {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column()
  title!: string;

  @Column("text")
  description!: string;

  @Column("decimal", { precision: 12, scale: 2 })
  goalAmount!: number;

  @Column("decimal", { precision: 12, scale: 2, default: 0 })
  raisedAmount!: number;

  @Column({ nullable: true })
  imageUrl!: string;

  @Column({ nullable: true })
  country!: string;

  @Column({ nullable: true })
  category!: string; // e.g., "Mosques", "Schools", "Food"

  @Column({
    type: "enum",
    enum: CollectionStatus,
    default: CollectionStatus.ACTIVE,
  })
  status!: CollectionStatus;

  @CreateDateColumn()
  createdAt!: Date;
}


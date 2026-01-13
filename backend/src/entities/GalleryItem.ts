import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn } from "typeorm";

@Entity()
export class GalleryItem {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @Column()
  imageUrl!: string;

  @Column({ nullable: true })
  title!: string;

  @Column("text", { nullable: true })
  description!: string;

  @CreateDateColumn()
  createdAt!: Date;
}


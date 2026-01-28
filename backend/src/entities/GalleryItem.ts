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

  @Column({ nullable: true })
  country!: string;

  @Column({ nullable: true })
  category!: string;

  @Column({ nullable: true })
  projectId!: string; // Reference to a collection if needed

  @CreateDateColumn()
  createdAt!: Date;
}





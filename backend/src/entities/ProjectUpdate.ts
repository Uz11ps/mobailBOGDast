import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, ManyToOne } from "typeorm";
import { Collection } from "./Collection";

@Entity()
export class ProjectUpdate {
  @PrimaryGeneratedColumn("uuid")
  id!: string;

  @ManyToOne(() => Collection)
  collection!: Collection;

  @Column()
  title!: string;

  @Column("text")
  content!: string;

  @Column({ nullable: true })
  videoUrl!: string;

  @Column({ nullable: true })
  imageUrl!: string;

  @CreateDateColumn()
  createdAt!: Date;
}

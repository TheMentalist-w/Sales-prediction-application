import { DocumentItem } from "./document-item";
import { Shop } from "./shop";

export interface Document {
    id: number,
    documentType: number,
    date: Date,
    shop: Shop,
    sender?: Shop,
    items: DocumentItem[];
}
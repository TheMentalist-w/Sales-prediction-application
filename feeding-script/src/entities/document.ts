import { DocumentItem } from "./document-item";
import { Shop } from "./shop";

export interface Document {
    id: number,
    documentType: number,
    date: Date,
    shop: Shop,
    senderId?: number,
    items: DocumentItem[];
}
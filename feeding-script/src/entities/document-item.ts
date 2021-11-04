import { AssortmentItem } from "./assortment-item";
import { Document } from "./document";

export interface DocumentItem {
    id: number,
    item: AssortmentItem,
    document: Document,
    quantity: number,
}
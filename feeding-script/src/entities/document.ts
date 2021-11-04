import { DocumentItem } from "./document-item";

export interface Document {
    id: number,
    type: number,
    place: string,
    receiverId?: number,
    warehouseId?: number,
    items: DocumentItem[];
}
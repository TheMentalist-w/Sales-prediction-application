import { DocumentItem } from "./document-item";
import { Shop } from "./shop";

export interface Document {
    id: number,
    documentType: number,
    date: Date,
    shop: Shop,
    receiver?: Shop,
    items: DocumentItem[];
}

export const getDocumentAsQuery = (document: Document): string[] => {
    return [`
        INSERT INTO d_Dokument(dok_Id, dok_Typ, dok_MagId, dok_OdbiorcaId, dok_DataWyst)
        VALUES (${document.id}, ${document.documentType}, ${document.shop.id}, ${document.receiver?.id || 'NULL'}, '${document.date.toISOString()}');
        `.trim(),
        ...document.items.map(docItem => `
            INSERT INTO d_Pozycja(ob_DokMagId, ob_TowId, ob_Ilosc)
            VALUES (${document.id}, ${docItem.item.id}, ${docItem.quantity});
        `),
    ]
}
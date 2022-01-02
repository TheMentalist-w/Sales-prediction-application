import { AssortmentGroup } from "./assortment-group";
import { Trait } from "./trait";

export interface AssortmentItem {
    id: number,
    name: string,
    type: AssortmentGroup,
    symbol: string,
    traits: Trait[],
    saleProbability: number[]
}

export const getItemAsDBQuery = (item: AssortmentItem): string[] => {
    return [`
        INSERT INTO t_Towar (tw_Id, tw_IdGrupa, tw_Symbol, tw_Nazwa, tw_Rodzaj) 
        VALUES (${item.id}, ${item.type.id}, '${item.symbol}', '${item.name}', 1);
    `.trim(),
        ...item.traits.map(trait => `
            INSERT INTO t_CechaTw(cht_IdTowar, cht_IdCecha)
            VALUES (${item.id}, ${trait.id});
        `.trim())
    ]
}
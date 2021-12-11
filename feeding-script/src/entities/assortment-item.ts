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
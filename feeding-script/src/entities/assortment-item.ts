import { Trait } from "./trait";

export interface AssortmentItem {
    id: number,
    name: string,
    type: string,
    symbol: string,
    traits: Trait[],
}
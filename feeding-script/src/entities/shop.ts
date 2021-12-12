export enum ShopSize {
    TINY,
    SMALL,
    MEDIUM,
    BIG,
    HUGE,
}

export interface Shop {
    id: number;
    symbol: string;
    size: ShopSize;
    name: string;
}
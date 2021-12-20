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

export const getShopAsQuery = (shop: Shop) => {
    return `
        INSERT INTO s_Magazyn (mag_Id, mag_Symbol, mag_Nazwa)
        VALUES (${shop.id}, '${shop.symbol}', '${shop.name}');
    `.trim();
}
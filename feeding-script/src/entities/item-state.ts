export interface ItemState {
    itemId: number,
    warehouseId: number,
    amount: number,
}

export const getItemStateAsQuery = (itemState: ItemState) => {
    return `INSERT INTO t_Stan (st_TowId, st_MagId, st_Stan) VALUES(${itemState.itemId}, ${itemState.warehouseId}, ${itemState.amount})`;
}
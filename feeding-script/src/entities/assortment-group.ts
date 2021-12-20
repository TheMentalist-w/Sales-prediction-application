export interface AssortmentGroup {
    id: number,
    name: string,
}

export const getGroupAsQuery = (group: AssortmentGroup) => {
    return `INSERT INTO s_GrupaTw (grt_Id, grt_Nazwa) VALUES (${group.id}, '${group.name}');`
};
export interface Trait {
    id: number,
    name: string
}

export const getTraitAsQuery = (trait: Trait) => 
    `INSERT INTO s_CechaTw VALUES (${trait.id}, '${trait.name}');`;
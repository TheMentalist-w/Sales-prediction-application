export interface EnumLike {
    [key: string]: number | string;
}

export const getEnumValueRange = (enumValues: EnumLike): number[] => {
    return Object.entries(enumValues)
        .filter(val => typeof val[1] === "number")
        .map(entry => entry[1] as number);
}
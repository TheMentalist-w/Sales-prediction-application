import { AssortmentGroup } from "../entities/assortment-group";
import { AssortmentItem } from "../entities/assortment-item";
import { Document } from "../entities/document";
import { DocumentItem } from "../entities/document-item";
import { Shop, ShopSize } from "../entities/shop";
import { Trait } from "../entities/trait";
import { stubItems, stubShops, stubTraits } from "./stub-data";
import { getEnumValueRange } from "./utilfuncs";

const getRandomNumber = (lo: number, hi: number): number => {
    return Math.round((Math.random() * (hi - lo)) + lo) 
}

const getRandomArrayElement = <T>(array: T[]): T => {
    return array[Math.floor(Math.random() * array.length)];
}

const combineTwoArrays = (arr1: string[], arr2: string[]): string[] => {
    if(arr1.length && arr2.length) {
        return arr1.flatMap(el1 => arr2.map(el2 => `${el1} ${el2}`));
    }
    
    if(!arr1.length && !arr2.length) {
        return [];
    }

    return arr1.length ? arr1 : arr2;
}

const getEveryPossibleCombination = (array2d: string[][]): string[] => {
    let combinedArray: string[] = [];
    for(const arr of array2d) {
        combinedArray = combineTwoArrays(combinedArray, arr);
    }
    return combinedArray;
}

export const generateShops = (): Shop[] => {
    return stubShops.map((value, index) => ({
        id: index,
        name: value,
        symbol: value.substring(0, 3).toUpperCase(),
        size: getRandomArrayElement(getEnumValueRange(ShopSize))
    }));
}

export const generateTraits = (): Trait[] => {
    return stubTraits.map((name, id) => ({name, id}));
}

export const generateAssortmentGroups = (): AssortmentGroup[] => {
    return stubItems.map((item, index) => ({id: index, name: item.name}));
}

export const generateItems = (groups: AssortmentGroup[], traits: Trait[]): AssortmentItem[] => {
    const items = stubItems.flatMap(item => {
        const variants = item.variants.map(variant => variant.split("|"));
        
        const combinedVariants = getEveryPossibleCombination(variants);
        const firstItems = combinedVariants.map((variant, index) => ({
            id: 0,
            name: `${item.name} ${variant}`,
            type: groups.find(e => e.name === item.name) || groups[0],
            traits: [],
            symbol: `${item.name.substring(0, 3).toUpperCase()}${index}`,
            saleProbability: item.saleProbabilities,
        }));

        const items = firstItems.map(item => {
            const selectedTraits = getRandomElementsFromArray(traits, getRandomNumber(1, 2)); 
            return {...item, traits: selectedTraits, saleProbability: updateSalesProbability(item)};
        });

        return items;
    });
    
    return items.map((item, index) => ({...item, id: index}));
}

export const generateDocuments = (shops: Shop[], items: AssortmentItem[]): Document[] => {
    const documentAmount = 50000;
    const documents: Document[] = [];
    const availableDocumentTypes = [9,36,14,10,12,11,13,35];

    for(let i = 1; i <= documentAmount; i++) {
        const documentType = getRandomArrayElement(availableDocumentTypes);
        const warehouses = getRandomElementsFromArray(shops, 2);

        documents.push({
            id: i,
            shop: warehouses[0],
            receiver: documentType === 9 ? warehouses[1] : undefined,
            documentType,
            date: getRandomDate(),
            items: generateItemsForDocument(items),
        });
    }
    return documents;
}

const generateItemsForDocument = (items: AssortmentItem[]): DocumentItem[] => {
    const itemAmount = getRandomNumber(2, 6);
    const selectedItems = getRandomElementsFromArray(items, itemAmount);
    const documentItems = selectedItems.map((item, index) => ({
        id: index,
        item,
        quantity: getRandomNumber(1, 5),
    }));

    return documentItems;
}

const getRandomDate = (): Date => {
    const date = new Date();
    date.setDate(date.getDate() + getRandomNumber(-3650, -1)); // roughly 10year range
    return date;
}

// low is included, high is excluded (range(0, 5) => [0, 1, 2, 3, 4]) 
const range = (lo: number, hi: number) => {
    return Array.from(Array(hi - lo).keys()).map(val => val + lo);
}

const getRandomElementsFromArray = <T>(array: T[], amount: number): T[] => {
    if(amount >= array.length) return array;
    const availableIndexes = range(0, array.length);
    const selectedIndexes = [];
    for(const i of range(0, amount)) {
        const selectedIndex = availableIndexes.splice(getRandomNumber(0, availableIndexes.length - 1), 1);
        selectedIndexes.push(...selectedIndex);
    }

    return selectedIndexes.map(index => array[index]);
}

const updateSalesProbability = (item: AssortmentItem): number[] => {
    let modifiedArray = [0,0,0,0,0,0,0,0,0,0,0,0];
    item.traits.forEach(trait => {
        modifiedArray = modifiedArray.map((el, idx) => {
            return el + getTraitModifier(trait)[idx];
        })
    });

    return item.saleProbability.map((prob, idx) => prob + modifiedArray[idx]);
}

const getTraitModifier = (trait: Trait): number[] => {
    switch(trait.name) {
        case "Na zimę":
            return [2,1,0,-1,-1,-2,-2,-1,0,0,1,2];
        case "Na jesień":
            return [1,2,2,1,1,0,-1,0,1,2,2,1];
        case "Nieprzemakalna":
            return [0,0,1,1,0,1,0,1,1,2,2,1];
        case "Polar":
            return [1,1,1,0,0,-1,-1,-1,0,1,1,1];
        case "Dres":
            return [1,1,0,0,0,0,-1,0,1,1,1,1];
        case "Odzież sportowa":
            return [2,0,0,1,1,1,2,1,0,-1,0,1];
        case "Oddychające":
            return [1,2,1,0,0,1,2,2,1,0,-1,0];
        default:
            return Array(12).fill(0);
        };
}

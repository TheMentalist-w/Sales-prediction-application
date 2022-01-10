import { DatabaseService } from "./database-service";
import { AssortmentGroup, getGroupAsQuery } from "./entities/assortment-group";
import { AssortmentItem, getItemAsDBQuery } from "./entities/assortment-item";
import { Document, getDocumentAsQuery } from "./entities/document";
import { getItemStateAsQuery, ItemState } from "./entities/item-state";
import { getShopAsQuery, Shop } from "./entities/shop";
import { getTraitAsQuery, Trait } from "./entities/trait";
import { 
    generateAssortmentGroups, 
    generateDocuments, 
    generateItems, 
    generateShops, 
    generateStates, 
    generateTraits 
} from "./utils/generators";

type ApplicationData = {
    shops: Shop[],
    traits: Trait[],
    groups: AssortmentGroup[],
    items: AssortmentItem[],
    documents: Document[],
    states: ItemState[]
}


export class Application {
    databaseService: DatabaseService;
    generatedDocuments: Document[];
    generatedItems: AssortmentItem[];

    constructor() {
        this.databaseService = new DatabaseService();
        this.generatedDocuments = [];
        this.generatedItems = [];
    }

    private async startup() {
        console.log("Connecting to the database...");
        await this.databaseService.setupDb();
        console.log("Removing old tables and data...");
        // await this.databaseService.removeTables();
        console.log("Creating new tables...");
        await this.databaseService.setupTables();
        console.log("Old data removed.")
    }

    private generateData(): ApplicationData {
        console.log("Generating data...");
        const shops = generateShops();
        console.log(`Generated ${shops.length} shops`);
        const traits = generateTraits();
        console.log(`Generated ${traits.length} traits`);
        const groups = generateAssortmentGroups();
        console.log(`Generated ${groups.length} assortment groups`);
        const items = generateItems(groups, traits);
        console.log(`Generated ${items.length} assortment items`);
        const documents = generateDocuments(shops, items);
        console.log(`Generated ${documents.length} documents`);
        const states = generateStates(items, shops, documents);
        console.log(`Generated ${states.length} states`);
        return {shops, traits, groups, items, documents, states};
    }

    private async saveData(
        {shops, traits, groups, items, documents, states}: ApplicationData
    ) {
        const queries: string[] = [
            ...shops.map(getShopAsQuery),
            ...traits.map(getTraitAsQuery),
            ...groups.map(getGroupAsQuery),
            ...items.flatMap(getItemAsDBQuery),
            ...documents.flatMap(getDocumentAsQuery),
            ...states.map(getItemStateAsQuery),
        ]

        console.log(`Executing ${queries.length} queries`);
        for(let i = 0; i < queries.length; i++) {
            if (i % 1000 === 0) console.log(`Executed ${i} queries`);
            await this.databaseService.query(queries[i]);
        }
    }

    async run() {
        await this.startup();
        const data = this.generateData();
        await this.saveData(data);
        console.log('Data saved');
        await this.databaseService.disconnect();
        console.log('Connection to the DB closed.');
    }
}
import { DatabaseService } from "./database-service";
import { AssortmentItem } from "./entities/assortment-item";
import { Document } from "./entities/document";
import { 
    generateAssortmentGroups, 
    generateDocuments, 
    generateItems, 
    generateShops, 
    generateTraits 
} from "./utils/generators";

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
        await this.databaseService.setupDb();
    }

    private generateData() {
        // done
        const shops = generateShops();
        // done
        const traits = generateTraits();
        
        // done
        const groups = generateAssortmentGroups();

        // done
        const items = generateItems(groups, traits);

        const documents = generateDocuments(shops, items);
    }

    private async saveData() {
        
    }

    async run() {
        await this.startup();
        this.generateData();
    }
}
import { DatabaseService } from "./database-service";
import { AssortmentItem } from "./entities/assortment-item";
import { Document } from "./entities/document";
import { 
    generateAssortmentGroups, 
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
        const shops = generateShops();
        const traits = generateTraits();
        const groups = generateAssortmentGroups();
        const items = generateItems(groups, traits);
    }

    private async saveData() {
        
    }

    async run() {
        await this.startup();
        this.generateData();
    }
}
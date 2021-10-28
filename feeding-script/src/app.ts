import { DatabaseService } from "./database-service";

export class Application {
    databaseService: DatabaseService;
    
    constructor() {
        this.databaseService = new DatabaseService();
    }

    private async startup() {
        await this.databaseService.setupDb();
    }

    async run() {
        await this.startup();
        await this.databaseService.purgeDatabase();
    }
}
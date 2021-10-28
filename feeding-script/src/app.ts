import { DatabaseService } from "./database-service";

export class Application {
    databaseService: DatabaseService;
    
    constructor() {
        this.databaseService = new DatabaseService();
    }

    run(): void {
    }
}
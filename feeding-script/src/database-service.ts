import {config, IResult, query, connect} from "mssql";

export class DatabaseService {
    config: config = {
        database: process.env.DB_NAME,
        server: 'localhost',
        port: 1433,
        user: process.env.DB_USERNAME,
        password: process.env.DB_PASSWORD,
        options: {
            trustServerCertificate: true,
        }
    }

    constructor() {}

    async setupDb() {
        await connect(this.config);
    }

    async query<T>(queryString: string): Promise<IResult<T>> {
        return await query<T>(queryString);
    }

    // PURGING relevant tables
    async purgeDatabase() {
        try {
            [
                'tw__Towar', 
                'tw_CechaTw', 
                'dok__Dokument', 
                'dok_Pozycja', 
                'sl_CechaTw', 
                'sl_GrupaTw'].forEach(tableName => {
                    this.query(`DELETE FROM ${tableName}`)
            });
            console.log('Tables purged');
        } catch (error) {
            console.error(error);
        }
    }
}
import * as mssql from "mssql";

export class DatabaseService {
    config: mssql.config = {
        database: 'testowy',
        server: 'localhost',
        port: 1433,
        user: 'sa',
        password: 'rootpass',
        options: {
            trustServerCertificate: true,
        }
    }

    constructor() {
        this.setupDb();
    }

    async setupDb() {
        await mssql.connect(this.config);
        await mssql.query('SELECT 2').then((res) => console.log(res.recordset)).catch(err => console.log(err));
    }
}
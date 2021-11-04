import { config, IResult, query, connect } from "mssql";
import { ColumnData } from "./utils/table-data";

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

    constructor() { }

    async setupDb() {
        await connect(this.config);
    }

    async query<T>(queryString: string): Promise<IResult<T>> {
        return await query<T>(queryString);
    }

    // PURGING relevant tables
    async purgeDatabase() {
        try {
            const tables = [
                't_Towar',
                't_CechaTw',
                'd_Dokument',
                'd_Pozycja',
                's_CechaTw',
                's_GrupaTw',
            ];
            tables.forEach(tableName => {
                this.query(`DELETE FROM ${tableName}`)
            });
            console.log('Tables purged');
        } catch (error) {
            console.error(error);
        }
    }

    async setupTables() {
        await this.createTable('t_Towar', [
            {name: 'tw_Id', type: 'int', isPrimaryKey: true},

        ]);
        await this.createTable('t_CechaTw', []);
        await this.createTable('s_CechaTw', []);
        await this.createTable('s_GrupaTw', []);
        await this.createTable('d_Dokument', []);
        await this.createTable('d_Pozycja', []);
    }

    private async createTable(name: string, columns: ColumnData[]) {
        let query = `IF OBJECT_ID(N'${name}', N'U') IS NULL CREATE TABLE ${name} (`;
        columns.forEach((column, index) => {
            query += `\n${column.name} ${column.type}`;
            if (!column.isNullable) query += ' NOT NULL';
            if (column.isPrimaryKey) query += ' PRIMARY KEY';
            if (index + 1 < columns.length) query += ',';
        });
        query += "\n);"
        return await this.query(query);
    }
}
import { config, IResult, query, connect, Connection, ConnectionPool } from "mssql";
import { ColumnData } from "./utils/table-data";

export class DatabaseService {
    config: config = {
        database: process.env.DB_NAME,
        server: process.env.DB_SERVER || 'localhost',
        port: parseInt(process.env.DB_PORT || '1433'),
        user: process.env.DB_USERNAME,
        password: process.env.DB_PASSWORD,
        options: {
            trustServerCertificate: true,
        }
    }

    connection: ConnectionPool | undefined;

    constructor() { }

    async setupDb() {
        this.connection = await connect(this.config);
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
                't_Stan',
                's_Magazyn'
            ];
            for(const tableName of tables) {
                await this.query(`DELETE FROM ${tableName}`);
            }
            console.log('Tables purged');
        } catch (error) {
            console.error(error);
        }
    }

    async setupTables() {
        await this.createTable('t_Towar', [
            {name: 'tw_Id', type: 'int', isPrimaryKey: true},
            {name: 'tw_Rodzaj', type: 'int'},
            {name: 'tw_Symbol', type: 'varchar(20)'},
            {name: 'tw_Nazwa', type: 'varchar(50)'}
        ]);
        await this.createTable('t_CechaTw', [
            {name: 'cht_Id', type: 'int', isPrimaryKey: true, autoIncrement: true},
            {name: 'cht_IdTowar', type: 'int'},
            {name: 'cht_IdCecha', type: 'int'}
        ]);
        await this.createTable('s_CechaTw', [
            {name: 'ctw_Id', type: 'int', isPrimaryKey: true},
            {name: 'ctw_Nazwa', type: 'varchar(50)'}
        ]);
        await this.createTable('s_GrupaTw', [
            {name: 'grt_Id', type: 'int', isPrimaryKey: true},
            {name: 'grt_Nazwa', type: 'varchar(50)'}
        ]);
        await this.createTable('d_Dokument', [
            {name: 'dok_Id', type: 'int', isPrimaryKey: true},
            {name: 'dok_Typ', type: 'int'},
            {name: 'dok_MagId', type: 'int'},
            {name: 'dok_OdbiorcaId', type: 'int', isNullable: true},
            {name: 'dok_DataWyst', type: 'datetime'}
        ]);
        await this.createTable('d_Pozycja', [
            {name: 'ob_Id', type: 'int', isPrimaryKey: true, autoIncrement: true},
            {name: 'ob_DokMagId', type: 'int'},
            {name: 'ob_TowId', type: 'int'},
            {name: 'ob_Ilosc', type: 'money'}
        ]);
        await this.createTable('t_Stan', [
            {name: 'st_TowId', type: 'int'},
            {name: 'st_MagId', type: 'int'},
            {name: 'st_Stan', type: 'money'}
        ]);
        await this.createTable('s_Magazyn', [
            {name: 'mag_Id', type: 'int', isPrimaryKey: true},
            {name: 'mag_Symbol', type: 'varchar(3)'},
            {name: 'mag_Nazwa', type: 'varchar(50)'}
        ]);
    }

    private async createTable(name: string, columns: ColumnData[]) {
        let query = `IF OBJECT_ID(N'${name}', N'U') IS NULL CREATE TABLE ${name} (`;
        columns.forEach((column, index) => {
            query += `\n${column.name} ${column.type}`;
            if (!column.isNullable) query += ' NOT NULL';
            if (column.isPrimaryKey) query += ' PRIMARY KEY';
            if (column.autoIncrement) query += ' IDENTITY';
            if (index + 1 < columns.length) query += ',';
        });
        query += "\n);"
        return await this.query(query);
    }

    async disconnect() {
        await this.connection?.close();
    }
}
#!/usr/bin/env node

/**
 * SAP HANA MCP Server
 * Servidor MCP personalizado para integración con SAP HANA
 * Basado en el contexto del proyecto de Control de Diseño
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';

interface HanaConfig {
  host: string;
  port: number;
  user: string;
  password: string;
  database: string;
  schema: string;
}

class HANAMCPServer {
  private server: Server;
  private hanaConfig: HanaConfig;

  constructor() {
    this.server = new Server(
      {
        name: 'hana-mcp-server',
        version: '0.1.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    // Configuración desde variables de entorno
    this.hanaConfig = {
      host: process.env.HANA_HOST || 'localhost',
      port: parseInt(process.env.HANA_PORT || '30015'),
      user: process.env.HANA_USER || '',
      password: process.env.HANA_PASSWORD || '',
      database: process.env.HANA_DATABASE || '',
      schema: process.env.HANA_SCHEMA || 'GARMENT_PRODUCTION_CONTROL',
    };

    this.setupToolHandlers();
    this.setupErrorHandling();
  }

  private setupErrorHandling(): void {
    this.server.onerror = (error) => {
      console.error('[MCP Error]', error);
    };

    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  private setupToolHandlers(): void {
    // Handler para listar herramientas disponibles
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'query_hana',
            description: 'Ejecuta consultas SQL en SAP HANA',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'Consulta SQL a ejecutar',
                },
                schema: {
                  type: 'string',
                  description: 'Esquema de la base de datos (opcional)',
                },
              },
              required: ['query'],
            },
          },
          {
            name: 'get_collections',
            description: 'Obtiene las colecciones disponibles de la base de datos HANA',
            inputSchema: {
              type: 'object',
              properties: {
                filter: {
                  type: 'string',
                  description: 'Filtro opcional para las colecciones',
                },
              },
              required: [],
            },
          },
          {
            name: 'get_references_by_collection',
            description: 'Obtiene referencias por ID de colección',
            inputSchema: {
              type: 'object',
              properties: {
                collection_id: {
                  type: 'string',
                  description: 'ID de la colección',
                },
              },
              required: ['collection_id'],
            },
          },
          {
            name: 'get_fabrics_by_reference',
            description: 'Obtiene telas por referencia y colección',
            inputSchema: {
              type: 'object',
              properties: {
                reference_id: {
                  type: 'string',
                  description: 'ID de la referencia',
                },
                collection_id: {
                  type: 'string',
                  description: 'ID de la colección',
                },
              },
              required: ['reference_id', 'collection_id'],
            },
          },
          {
            name: 'get_materials_by_reference',
            description: 'Obtiene insumos por referencia y colección',
            inputSchema: {
              type: 'object',
              properties: {
                reference_id: {
                  type: 'string',
                  description: 'ID de la referencia',
                },
                collection_id: {
                  type: 'string',
                  description: 'ID de la colección',
                },
              },
              required: ['reference_id', 'collection_id'],
            },
          },
          {
            name: 'search_pt_code',
            description: 'Busca códigos PT en el sistema',
            inputSchema: {
              type: 'object',
              properties: {
                pt_code: {
                  type: 'string',
                  description: 'Código PT a buscar',
                },
              },
              required: ['pt_code'],
            },
          },
        ],
      };
    });

    // Handler para ejecutar herramientas
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        switch (name) {
          case 'query_hana':
            return await this.handleQueryHana(args);
          case 'get_collections':
            return await this.handleGetCollections(args);
          case 'get_references_by_collection':
            return await this.handleGetReferencesByCollection(args);
          case 'get_fabrics_by_reference':
            return await this.handleGetFabricsByReference(args);
          case 'get_materials_by_reference':
            return await this.handleGetMaterialsByReference(args);
          case 'search_pt_code':
            return await this.handleSearchPTCode(args);
          default:
            throw new McpError(
              ErrorCode.MethodNotFound,
              `Herramienta desconocida: ${name}`
            );
        }
      } catch (error) {
        const errorMessage = error instanceof Error ? error.message : String(error);
        throw new McpError(
          ErrorCode.InternalError,
          `Error ejecutando herramienta ${name}: ${errorMessage}`
        );
      }
    });
  }

  private async executeHanaQuery(query: string, schema?: string): Promise<any[]> {
    // Simulación de ejecución de consulta HANA
    // En una implementación real, aquí usarías @sap/hana-client
    console.log(`[HANA Query] Schema: ${schema || this.hanaConfig.schema}`);
    console.log(`[HANA Query] SQL: ${query}`);
    
    // Datos simulados basados en tu proyecto
    const mockData = this.getMockDataForQuery(query);
    return mockData;
  }

  private getMockDataForQuery(query: string): any[] {
    const queryLower = query.toLowerCase();
    
    if (queryLower.includes('collection') && queryLower.includes('select')) {
      return [
        { COLLECTION_ID: '063', COLLECTION_NAME: 'Winter Sun 2024', YEAR: '2024', STATUS: 'active' },
        { COLLECTION_ID: '085', COLLECTION_NAME: 'Winter Sun 2025', YEAR: '2025', STATUS: 'active' },
        { COLLECTION_ID: '067', COLLECTION_NAME: 'Spring Summer 2024', YEAR: '2024', STATUS: 'active' },
      ];
    }
    
    if (queryLower.includes('reference') || queryLower.includes('pt_code')) {
      return [
        { PT_CODE: 'REF001', COLLECTION_ID: '063', DESCRIPTION: 'Vestido largo invierno', STATUS: 'active' },
        { PT_CODE: 'REF002', COLLECTION_ID: '085', DESCRIPTION: 'Chaqueta primavera', STATUS: 'development' },
      ];
    }
    
    if (queryLower.includes('tela') || queryLower.includes('fabric')) {
      return [
        { TELA_CODE: 'TEL001', DESCRIPTION: 'Algodón orgánico', COLOR: 'Natural', REFERENCE_ID: 'REF001' },
        { TELA_CODE: 'TEL002', DESCRIPTION: 'Lino premium', COLOR: 'Blanco', REFERENCE_ID: 'REF001' },
      ];
    }
    
    if (queryLower.includes('insumo') || queryLower.includes('material')) {
      return [
        { MATERIAL_CODE: 'INS001', DESCRIPTION: 'Botón metálico', QUANTITY: 5, REFERENCE_ID: 'REF001' },
        { MATERIAL_CODE: 'INS002', DESCRIPTION: 'Cremallera 20cm', QUANTITY: 1, REFERENCE_ID: 'REF001' },
      ];
    }
    
    return [{ message: 'Consulta ejecutada correctamente', query }];
  }

  private async handleQueryHana(args: any): Promise<any> {
    const { query, schema } = args;
    const results = await this.executeHanaQuery(query, schema);
    
    return {
      content: [
        {
          type: 'text',
          text: `Consulta HANA ejecutada:\n\nSQL: ${query}\nEsquema: ${schema || this.hanaConfig.schema}\n\nResultados:\n${JSON.stringify(results, null, 2)}`,
        },
      ],
    };
  }

  private async handleGetCollections(args: any): Promise<any> {
    const query = `SELECT COLLECTION_ID, COLLECTION_NAME, YEAR, STATUS FROM ${this.hanaConfig.schema}.COLLECTIONS`;
    const results = await this.executeHanaQuery(query);
    
    return {
      content: [
        {
          type: 'text',
          text: `Colecciones encontradas:\n${JSON.stringify(results, null, 2)}`,
        },
      ],
    };
  }

  private async handleGetReferencesByCollection(args: any): Promise<any> {
    const { collection_id } = args;
    const query = `SELECT PT_CODE, DESCRIPTION, STATUS FROM ${this.hanaConfig.schema}.REFERENCES WHERE COLLECTION_ID = '${collection_id}'`;
    const results = await this.executeHanaQuery(query);
    
    return {
      content: [
        {
          type: 'text',
          text: `Referencias para colección ${collection_id}:\n${JSON.stringify(results, null, 2)}`,
        },
      ],
    };
  }

  private async handleGetFabricsByReference(args: any): Promise<any> {
    const { reference_id, collection_id } = args;
    const query = `SELECT TELA_CODE, DESCRIPTION, COLOR FROM ${this.hanaConfig.schema}.FABRICS WHERE REFERENCE_ID = '${reference_id}'`;
    const results = await this.executeHanaQuery(query);
    
    return {
      content: [
        {
          type: 'text',
          text: `Telas para referencia ${reference_id}:\n${JSON.stringify(results, null, 2)}`,
        },
      ],
    };
  }

  private async handleGetMaterialsByReference(args: any): Promise<any> {
    const { reference_id, collection_id } = args;
    const query = `SELECT MATERIAL_CODE, DESCRIPTION, QUANTITY FROM ${this.hanaConfig.schema}.MATERIALS WHERE REFERENCE_ID = '${reference_id}'`;
    const results = await this.executeHanaQuery(query);
    
    return {
      content: [
        {
          type: 'text',
          text: `Insumos para referencia ${reference_id}:\n${JSON.stringify(results, null, 2)}`,
        },
      ],
    };
  }

  private async handleSearchPTCode(args: any): Promise<any> {
    const { pt_code } = args;
    const query = `SELECT PT_CODE, COLLECTION_ID, DESCRIPTION FROM ${this.hanaConfig.schema}.REFERENCES WHERE PT_CODE LIKE '%${pt_code}%'`;
    const results = await this.executeHanaQuery(query);
    
    return {
      content: [
        {
          type: 'text',
          text: `Búsqueda PT Code '${pt_code}':\n${JSON.stringify(results, null, 2)}`,
        },
      ],
    };
  }

  async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('SAP HANA MCP Server running on stdio');
  }
}

// Iniciar el servidor
const server = new HANAMCPServer();
server.run().catch(console.error);
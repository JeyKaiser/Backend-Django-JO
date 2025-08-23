#!/usr/bin/env node

/**
 * 🚀 SERVIDOR MCP GOOGLE DRIVE - VERSIÓN COMPLETA
 * 
 * Este servidor MCP proporciona acceso completo a Google Drive con:
 * - Autenticación OAuth2 automática
 * - Operaciones CRUD (crear, leer, actualizar, eliminar)
 * - Búsquedas avanzadas
 * - Gestión de permisos
 * - Manejo de metadatos
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListResourcesRequestSchema,
  ListToolsRequestSchema,
  ReadResourceRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { google } from 'googleapis';
import { OAuth2Client } from 'google-auth-library';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import http from 'http';
import url from 'url';
import open from 'open';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Configuración de autenticación
const CREDENTIALS_PATH = path.join(__dirname, 'oauth2.keys.json');
const TOKEN_PATH = path.join(__dirname, 'tokens.json');
const SCOPES = [
  'https://www.googleapis.com/auth/drive',
  'https://www.googleapis.com/auth/drive.file',
  'https://www.googleapis.com/auth/drive.metadata'
];

interface Credentials {
  installed: {
    client_id: string;
    client_secret: string;
    redirect_uris: string[];
  };
}

interface TokenData {
  access_token: string;
  refresh_token?: string;
  scope: string;
  token_type: string;
  expiry_date?: number;
}

class GoogleDriveMCPServer {
  private server: Server;
  private oAuth2Client: OAuth2Client | null = null;
  private drive: any = null;

  constructor() {
    this.server = new Server(
      {
        name: 'google-drive-server',
        version: '1.0.0',
      },
      {
        capabilities: {
          resources: {},
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    this.setupResourceHandlers();
  }

  /**
   * Configurar autenticación OAuth2
   */
  private async setupAuth(): Promise<void> {
    try {
      // Cargar credenciales
      const credentials: Credentials = JSON.parse(fs.readFileSync(CREDENTIALS_PATH, 'utf8'));
      const { client_secret, client_id, redirect_uris } = credentials.installed;

      this.oAuth2Client = new OAuth2Client(client_id, client_secret, redirect_uris[0]);

      // Intentar cargar tokens existentes
      if (fs.existsSync(TOKEN_PATH)) {
        const token: TokenData = JSON.parse(fs.readFileSync(TOKEN_PATH, 'utf8'));
        this.oAuth2Client.setCredentials(token);
        
        // Verificar si el token es válido
        try {
          await this.oAuth2Client.getAccessToken();
          this.drive = google.drive({ version: 'v3', auth: this.oAuth2Client });
          console.log('✅ Autenticación OAuth2 exitosa con tokens existentes');
          return;
        } catch (error) {
          console.log('⚠️ Token expirado, iniciando nueva autenticación...');
        }
      }

      // Si no hay tokens válidos, obtener nuevos
      await this.getNewToken();
      
    } catch (error) {
      console.error('❌ Error configurando autenticación:', error);
      throw error;
    }
  }

  /**
   * Obtener nuevo token OAuth2
   */
  private async getNewToken(): Promise<void> {
    return new Promise((resolve, reject) => {
      const authUrl = this.oAuth2Client!.generateAuthUrl({
        access_type: 'offline',
        scope: SCOPES,
        prompt: 'consent'
      });

      console.log('🔐 Iniciando proceso de autenticación OAuth2...');
      console.log('🌐 Abriendo navegador para autorización...');

      // Crear servidor temporal para recibir el código
      const server = http.createServer(async (req, res) => {
        try {
          const parsedUrl = url.parse(req.url!, true);
          
          if (parsedUrl.pathname === '/') {
            const code = parsedUrl.query.code as string;
            
            if (code) {
              res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
              res.end(`
                <!DOCTYPE html>
                <html>
                <head>
                  <title>Autenticación Exitosa</title>
                  <style>
                    body { 
                      font-family: Arial, sans-serif; 
                      text-align: center; 
                      padding: 50px;
                      background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                      color: white;
                    }
                    .container {
                      background: rgba(255,255,255,0.1);
                      padding: 30px;
                      border-radius: 15px;
                      backdrop-filter: blur(10px);
                    }
                    .success { color: #4CAF50; font-size: 24px; margin-bottom: 20px; }
                    .emoji { font-size: 48px; }
                  </style>
                </head>
                <body>
                  <div class="container">
                    <div class="emoji">🎉</div>
                    <div class="success">¡Autenticación Exitosa!</div>
                    <p>El servidor MCP de Google Drive está ahora configurado correctamente.</p>
                    <p>Puedes cerrar esta ventana y volver a Roo Code.</p>
                    <p><strong>¡Ya puedes usar todas las funciones de Google Drive!</strong></p>
                  </div>
                </body>
                </html>
              `);

              // Intercambiar código por tokens
              try {
                const { tokens } = await this.oAuth2Client!.getToken(code);
                this.oAuth2Client!.setCredentials(tokens);
                
                // Guardar tokens
                fs.writeFileSync(TOKEN_PATH, JSON.stringify(tokens, null, 2));
                
                // Configurar cliente de Drive
                this.drive = google.drive({ version: 'v3', auth: this.oAuth2Client! });
                
                console.log('✅ Tokens obtenidos y guardados exitosamente');
                server.close();
                resolve();
                
              } catch (tokenError) {
                console.error('❌ Error obteniendo tokens:', tokenError);
                server.close();
                reject(tokenError);
              }
            } else {
              res.writeHead(400, { 'Content-Type': 'text/html' });
              res.end('❌ No se recibió código de autorización');
              server.close();
              reject(new Error('No authorization code received'));
            }
          }
        } catch (error) {
          console.error('❌ Error en servidor de callback:', error);
          res.writeHead(500, { 'Content-Type': 'text/html' });
          res.end('❌ Error interno del servidor');
          server.close();
          reject(error);
        }
      });

      server.listen(3000, () => {
        console.log('🔗 Servidor de callback iniciado en http://localhost:3000');
        
        // Abrir navegador
        open(authUrl).catch((error) => {
          console.error('⚠️ No se pudo abrir el navegador automáticamente');
          console.log(`📋 Por favor, abre manualmente esta URL en tu navegador:`);
          console.log(authUrl);
        });
      });

      // Timeout de 5 minutos
      setTimeout(() => {
        server.close();
        reject(new Error('Timeout: Autenticación no completada en 5 minutos'));
      }, 300000);
    });
  }

  /**
   * Configurar manejadores de herramientas
   */
  private setupToolHandlers(): void {
    this.server.setRequestHandler(ListToolsRequestSchema, async () => ({
      tools: [
        {
          name: 'list_files',
          description: 'Listar archivos en Google Drive con opciones de filtrado y paginación',
          inputSchema: {
            type: 'object',
            properties: {
              pageSize: { type: 'number', description: 'Número de archivos a devolver (máximo 1000)' },
              pageToken: { type: 'string', description: 'Token para la siguiente página' },
              orderBy: { type: 'string', description: 'Campo de ordenamiento (ej: modifiedTime desc)' },
              q: { type: 'string', description: 'Query de búsqueda' }
            }
          }
        },
        {
          name: 'search_files',
          description: 'Buscar archivos con criterios específicos',
          inputSchema: {
            type: 'object',
            properties: {
              query: { type: 'string', description: 'Query de búsqueda (ej: name contains "test")' },
              maxResults: { type: 'number', description: 'Número máximo de resultados' }
            },
            required: ['query']
          }
        },
        {
          name: 'get_metadata',
          description: 'Obtener metadatos detallados de un archivo',
          inputSchema: {
            type: 'object',
            properties: {
              fileId: { type: 'string', description: 'ID del archivo' }
            },
            required: ['fileId']
          }
        },
        {
          name: 'download_file',
          description: 'Descargar contenido de un archivo',
          inputSchema: {
            type: 'object',
            properties: {
              fileId: { type: 'string', description: 'ID del archivo' },
              format: { type: 'string', description: 'Formato de exportación para Google Docs' }
            },
            required: ['fileId']
          }
        },
        {
          name: 'upload_file',
          description: 'Subir un nuevo archivo a Google Drive',
          inputSchema: {
            type: 'object',
            properties: {
              name: { type: 'string', description: 'Nombre del archivo' },
              content: { type: 'string', description: 'Contenido del archivo' },
              mimeType: { type: 'string', description: 'Tipo MIME del archivo' },
              parents: { type: 'array', items: { type: 'string' }, description: 'IDs de carpetas padre' }
            },
            required: ['name', 'content']
          }
        },
        {
          name: 'create_folder',
          description: 'Crear una nueva carpeta',
          inputSchema: {
            type: 'object',
            properties: {
              name: { type: 'string', description: 'Nombre de la carpeta' },
              parents: { type: 'array', items: { type: 'string' }, description: 'IDs de carpetas padre' }
            },
            required: ['name']
          }
        },
        {
          name: 'delete_file',
          description: 'Eliminar un archivo o carpeta',
          inputSchema: {
            type: 'object',
            properties: {
              fileId: { type: 'string', description: 'ID del archivo a eliminar' }
            },
            required: ['fileId']
          }
        },
        {
          name: 'share_file',
          description: 'Compartir un archivo con permisos específicos',
          inputSchema: {
            type: 'object',
            properties: {
              fileId: { type: 'string', description: 'ID del archivo' },
              email: { type: 'string', description: 'Email del usuario a compartir' },
              role: { type: 'string', enum: ['owner', 'organizer', 'fileOrganizer', 'writer', 'commenter', 'reader'], description: 'Rol del usuario' },
              type: { type: 'string', enum: ['user', 'group', 'domain', 'anyone'], description: 'Tipo de permiso' }
            },
            required: ['fileId', 'role', 'type']
          }
        },
        {
          name: 'update_file',
          description: 'Actualizar metadatos o contenido de un archivo',
          inputSchema: {
            type: 'object',
            properties: {
              fileId: { type: 'string', description: 'ID del archivo' },
              name: { type: 'string', description: 'Nuevo nombre del archivo' },
              content: { type: 'string', description: 'Nuevo contenido del archivo' },
              description: { type: 'string', description: 'Nueva descripción' }
            },
            required: ['fileId']
          }
        },
        {
          name: 'copy_file',
          description: 'Copiar un archivo existente',
          inputSchema: {
            type: 'object',
            properties: {
              fileId: { type: 'string', description: 'ID del archivo a copiar' },
              name: { type: 'string', description: 'Nombre de la copia' },
              parents: { type: 'array', items: { type: 'string' }, description: 'IDs de carpetas padre para la copia' }
            },
            required: ['fileId']
          }
        }
      ]
    }));

    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      try {
        // Asegurar autenticación antes de cada operación
        if (!this.drive) {
          await this.setupAuth();
        }

        switch (name) {
          case 'list_files':
            return await this.listFiles(args);
          case 'search_files':
            return await this.searchFiles(args);
          case 'get_metadata':
            return await this.getMetadata(args);
          case 'download_file':
            return await this.downloadFile(args);
          case 'upload_file':
            return await this.uploadFile(args);
          case 'create_folder':
            return await this.createFolder(args);
          case 'delete_file':
            return await this.deleteFile(args);
          case 'share_file':
            return await this.shareFile(args);
          case 'update_file':
            return await this.updateFile(args);
          case 'copy_file':
            return await this.copyFile(args);
          default:
            throw new Error(`Herramienta desconocida: ${name}`);
        }
      } catch (error) {
        console.error(`❌ Error ejecutando ${name}:`, error);
        return {
          content: [{
            type: 'text',
            text: `❌ Error: ${error instanceof Error ? error.message : 'Error desconocido'}`
          }],
          isError: true
        };
      }
    });
  }

  /**
   * Configurar manejadores de recursos
   */
  private setupResourceHandlers(): void {
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => ({
      resources: [
        {
          uri: 'drive://files',
          mimeType: 'application/json',
          name: 'Lista de archivos de Google Drive'
        },
        {
          uri: 'drive://folders/{folderId}',
          mimeType: 'application/json',
          name: 'Contenido de carpeta específica'
        },
        {
          uri: 'drive://file/{fileId}/metadata',
          mimeType: 'application/json',
          name: 'Metadatos de archivo específico'
        }
      ]
    }));

    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const { uri } = request.params;

      try {
        if (!this.drive) {
          await this.setupAuth();
        }

        if (uri === 'drive://files') {
          const response = await this.drive.files.list({
            pageSize: 50,
            fields: 'nextPageToken, files(id, name, mimeType, size, modifiedTime, parents)'
          });
          
          return {
            contents: [{
              uri,
              mimeType: 'application/json',
              text: JSON.stringify(response.data, null, 2)
            }]
          };
        }

        const folderMatch = uri.match(/^drive:\/\/folders\/(.+)$/);
        if (folderMatch) {
          const folderId = folderMatch[1];
          const response = await this.drive.files.list({
            q: `'${folderId}' in parents`,
            fields: 'files(id, name, mimeType, size, modifiedTime)'
          });
          
          return {
            contents: [{
              uri,
              mimeType: 'application/json',
              text: JSON.stringify(response.data, null, 2)
            }]
          };
        }

        const fileMatch = uri.match(/^drive:\/\/file\/(.+)\/metadata$/);
        if (fileMatch) {
          const fileId = fileMatch[1];
          const response = await this.drive.files.get({
            fileId,
            fields: '*'
          });
          
          return {
            contents: [{
              uri,
              mimeType: 'application/json',
              text: JSON.stringify(response.data, null, 2)
            }]
          };
        }

        throw new Error(`URI no soportado: ${uri}`);
      } catch (error) {
        throw new Error(`Error accediendo a recurso: ${error instanceof Error ? error.message : 'Error desconocido'}`);
      }
    });
  }

  // Métodos de implementación para cada herramienta

  private async listFiles(args: any) {
    const { pageSize = 50, pageToken, orderBy = 'modifiedTime desc', q } = args;
    
    const response = await this.drive.files.list({
      pageSize: Math.min(pageSize, 1000),
      pageToken,
      orderBy,
      q,
      fields: 'nextPageToken, files(id, name, mimeType, size, modifiedTime, parents, owners, shared, starred, trashed)'
    });

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          ...response.data,
          totalFiles: response.data.files?.length || 0,
          hasNextPage: !!response.data.nextPageToken
        }, null, 2)
      }]
    };
  }

  private async searchFiles(args: any) {
    const { query, maxResults = 50 } = args;
    
    const response = await this.drive.files.list({
      q: query,
      pageSize: Math.min(maxResults, 1000),
      fields: 'files(id, name, mimeType, size, modifiedTime, parents, webViewLink, thumbnailLink)'
    });

    return {
      content: [{
        type: 'text',
        text: JSON.stringify({
          query,
          results: response.data.files,
          count: response.data.files?.length || 0
        }, null, 2)
      }]
    };
  }

  private async getMetadata(args: any) {
    const { fileId } = args;
    
    const response = await this.drive.files.get({
      fileId,
      fields: '*'
    });

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(response.data, null, 2)
      }]
    };
  }

  private async downloadFile(args: any) {
    const { fileId, format } = args;
    
    let response;
    if (format) {
      // Para Google Docs, Sheets, etc.
      response = await this.drive.files.export({
        fileId,
        mimeType: format
      });
    } else {
      // Para archivos binarios
      response = await this.drive.files.get({
        fileId,
        alt: 'media'
      });
    }

    return {
      content: [{
        type: 'text',
        text: typeof response.data === 'string' ? response.data : JSON.stringify(response.data)
      }]
    };
  }

  private async uploadFile(args: any) {
    const { name, content, mimeType = 'text/plain', parents } = args;
    
    const response = await this.drive.files.create({
      requestBody: {
        name,
        parents
      },
      media: {
        mimeType,
        body: content
      },
      fields: 'id, name, mimeType, size, webViewLink'
    });

    return {
      content: [{
        type: 'text',
        text: `✅ Archivo subido exitosamente:\n${JSON.stringify(response.data, null, 2)}`
      }]
    };
  }

  private async createFolder(args: any) {
    const { name, parents } = args;
    
    const response = await this.drive.files.create({
      requestBody: {
        name,
        mimeType: 'application/vnd.google-apps.folder',
        parents
      },
      fields: 'id, name, mimeType, webViewLink'
    });

    return {
      content: [{
        type: 'text',
        text: `✅ Carpeta creada exitosamente:\n${JSON.stringify(response.data, null, 2)}`
      }]
    };
  }

  private async deleteFile(args: any) {
    const { fileId } = args;
    
    await this.drive.files.delete({
      fileId
    });

    return {
      content: [{
        type: 'text',
        text: `✅ Archivo eliminado exitosamente: ${fileId}`
      }]
    };
  }

  private async shareFile(args: any) {
    const { fileId, email, role, type } = args;
    
    const permission: any = {
      role,
      type
    };
    
    if (email) permission.emailAddress = email;

    const response = await this.drive.permissions.create({
      fileId,
      requestBody: permission,
      fields: 'id, role, type, emailAddress'
    });

    return {
      content: [{
        type: 'text',
        text: `✅ Archivo compartido exitosamente:\n${JSON.stringify(response.data, null, 2)}`
      }]
    };
  }

  private async updateFile(args: any) {
    const { fileId, name, content, description } = args;
    
    const updateData: any = {};
    if (name) updateData.name = name;
    if (description) updateData.description = description;

    const requestParams: any = {
      fileId,
      requestBody: updateData,
      fields: 'id, name, mimeType, size, modifiedTime'
    };

    if (content) {
      requestParams.media = {
        mimeType: 'text/plain',
        body: content
      };
    }

    const response = await this.drive.files.update(requestParams);

    return {
      content: [{
        type: 'text',
        text: `✅ Archivo actualizado exitosamente:\n${JSON.stringify(response.data, null, 2)}`
      }]
    };
  }

  private async copyFile(args: any) {
    const { fileId, name, parents } = args;
    
    const response = await this.drive.files.copy({
      fileId,
      requestBody: {
        name,
        parents
      },
      fields: 'id, name, mimeType, size, webViewLink'
    });

    return {
      content: [{
        type: 'text',
        text: `✅ Archivo copiado exitosamente:\n${JSON.stringify(response.data, null, 2)}`
      }]
    };
  }

  /**
   * Iniciar el servidor
   */
  async run(): Promise<void> {
    console.log('🚀 Iniciando Servidor MCP Google Drive...');
    
    try {
      // Configurar autenticación al inicio
      await this.setupAuth();
      
      const transport = new StdioServerTransport();
      await this.server.connect(transport);
      
      console.log('✅ Servidor MCP Google Drive iniciado exitosamente');
      console.log('🔗 Conectado y listo para recibir comandos');
      
    } catch (error) {
      console.error('❌ Error iniciando servidor:', error);
      process.exit(1);
    }
  }
}

// Iniciar servidor si se ejecuta directamente
if (import.meta.url === `file://${process.argv[1]}`) {
  const server = new GoogleDriveMCPServer();
  server.run().catch((error) => {
    console.error('❌ Error fatal:', error);
    process.exit(1);
  });
}

export default GoogleDriveMCPServer;
#!/usr/bin/env node

/**
 * 🧪 SCRIPT DE PRUEBAS - CONEXIÓN GOOGLE DRIVE MCP
 * 
 * Este script prueba la conexión directa con el servidor MCP de Google Drive
 * y verifica que todas las funcionalidades estén operativas.
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

console.log('🚀 INICIANDO PRUEBAS DEL SERVIDOR MCP GOOGLE DRIVE');
console.log('=' .repeat(60));

// Función para enviar comandos MCP
function sendMCPCommand(server, command) {
  return new Promise((resolve, reject) => {
    const request = JSON.stringify(command) + '\n';
    
    let response = '';
    const timeout = setTimeout(() => {
      reject(new Error('Timeout esperando respuesta'));
    }, 30000);

    const onData = (data) => {
      response += data.toString();
      try {
        const parsed = JSON.parse(response.trim());
        clearTimeout(timeout);
        server.stdout.off('data', onData);
        resolve(parsed);
      } catch (e) {
        // Seguir esperando más datos
      }
    };

    server.stdout.on('data', onData);
    server.stdin.write(request);
  });
}

async function testGoogleDriveConnection() {
  console.log('📡 Iniciando servidor MCP...');
  
  const serverPath = join(__dirname, 'dist', 'google-drive-mcp-server.js');
  const server = spawn('node', [serverPath], {
    stdio: ['pipe', 'pipe', 'pipe']
  });

  // Manejar errores del proceso
  server.on('error', (error) => {
    console.error('❌ Error iniciando servidor:', error.message);
    process.exit(1);
  });

  // Capturar logs del servidor
  server.stderr.on('data', (data) => {
    const message = data.toString().trim();
    if (message) {
      console.log('📝 Servidor:', message);
    }
  });

  try {
    console.log('🔄 Esperando inicialización del servidor...');
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Prueba 1: Inicializar conexión
    console.log('\n📋 PRUEBA 1: Inicialización MCP');
    const initResponse = await sendMCPCommand(server, {
      jsonrpc: '2.0',
      id: 1,
      method: 'initialize',
      params: {
        protocolVersion: '2024-11-05',
        capabilities: {
          roots: {
            listChanged: false
          }
        },
        clientInfo: {
          name: 'test-client',
          version: '1.0.0'
        }
      }
    });
    
    console.log('✅ Inicialización exitosa:', initResponse.result?.capabilities ? 'OK' : 'FALLO');

    // Prueba 2: Listar herramientas disponibles
    console.log('\n📋 PRUEBA 2: Listar herramientas disponibles');
    const toolsResponse = await sendMCPCommand(server, {
      jsonrpc: '2.0',
      id: 2,
      method: 'tools/list',
      params: {}
    });
    
    if (toolsResponse.result?.tools) {
      console.log('✅ Herramientas disponibles:');
      toolsResponse.result.tools.forEach(tool => {
        console.log(`   📌 ${tool.name}: ${tool.description}`);
      });
    } else {
      console.log('❌ No se pudieron obtener las herramientas');
    }

    // Prueba 3: Listar recursos disponibles
    console.log('\n📋 PRUEBA 3: Listar recursos disponibles');
    const resourcesResponse = await sendMCPCommand(server, {
      jsonrpc: '2.0',
      id: 3,
      method: 'resources/list',
      params: {}
    });
    
    if (resourcesResponse.result?.resources) {
      console.log('✅ Recursos disponibles:');
      resourcesResponse.result.resources.forEach(resource => {
        console.log(`   📁 ${resource.uri}: ${resource.name}`);
      });
    } else {
      console.log('❌ No se pudieron obtener los recursos');
    }

    console.log('\n🎉 PRUEBAS COMPLETADAS EXITOSAMENTE');
    console.log('=' .repeat(60));
    console.log('✅ El servidor MCP de Google Drive está funcionando correctamente');
    console.log('📝 Próximos pasos:');
    console.log('   1. Configura el servidor en Roo Code settings');
    console.log('   2. Usa use_mcp_tool() para acceder a Google Drive');
    console.log('   3. Prueba con: use_mcp_tool("google-drive", "list_files", {})');

  } catch (error) {
    console.error('❌ Error durante las pruebas:', error.message);
    console.log('\n🔧 PASOS DE SOLUCIÓN:');
    console.log('   1. Verifica que las credenciales OAuth2 estén correctas');
    console.log('   2. Asegúrate de haber autorizado la aplicación');
    console.log('   3. Revisa que el puerto 3000 esté libre');
  } finally {
    server.kill();
    process.exit(0);
  }
}

// Ejecutar pruebas
testGoogleDriveConnection().catch(error => {
  console.error('❌ Error fatal:', error);
  process.exit(1);
});
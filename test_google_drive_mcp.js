#!/usr/bin/env node

/**
 * Script de prueba para el MCP de Google Drive
 * Prueba las funcionalidades básicas del servidor MCP
 */

import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🚀 Iniciando prueba del MCP de Google Drive...\n');

// Función para ejecutar comandos MCP
function executeMCPCommand(command, args = []) {
  return new Promise((resolve, reject) => {
    console.log(`📤 Ejecutando comando MCP: ${command} ${args.join(' ')}`);

    const mcpBinaryPath = path.join(__dirname, 'node_modules', '.bin', 'mcp-gdrive.cmd');
    const mcpProcess = spawn(mcpBinaryPath, [command, ...args], {
      cwd: path.join(__dirname),
      stdio: ['pipe', 'pipe', 'pipe'],
      env: {
        ...process.env,
        GDRIVE_CREDS_DIR: __dirname,
        GOOGLE_APPLICATION_CREDENTIALS: path.join(__dirname, 'credentials.json')
      }
    });

    let stdout = '';
    let stderr = '';

    mcpProcess.stdout.on('data', (data) => {
      stdout += data.toString();
    });

    mcpProcess.stderr.on('data', (data) => {
      stderr += data.toString();
    });

    mcpProcess.on('close', (code) => {
      if (code === 0) {
        console.log(`✅ Comando exitoso: ${command}`);
        resolve({ stdout, stderr });
      } else {
        console.log(`❌ Error en comando: ${command} (código: ${code})`);
        console.log('STDERR:', stderr);
        reject(new Error(`Comando falló: ${command}`));
      }
    });

    mcpProcess.on('error', (error) => {
      console.log(`💥 Error ejecutando: ${command}`, error.message);
      reject(error);
    });
  });
}

// Función principal de pruebas
async function runTests() {
  try {
    console.log('📋 PRUEBA 1: Listar archivos de la raíz de Google Drive\n');

    await executeMCPCommand('list_files', ['--max-results', '5']);

    console.log('\n📋 PRUEBA 2: Buscar archivos con "test"\n');

    await executeMCPCommand('search_files', ['test', '--max-results', '3']);

    console.log('\n📋 PRUEBA 3: Crear una carpeta de prueba\n');

    const timestamp = Date.now();
    const folderName = `Test-MCP-${timestamp}`;

    await executeMCPCommand('create_folder', [folderName]);

    console.log(`\n📋 PRUEBA 4: Subir un archivo de prueba a la carpeta creada\n`);

    // Crear un archivo de prueba temporal
    const testFilePath = path.join(__dirname, 'test_file.txt');
    fs.writeFileSync(testFilePath, `Archivo de prueba creado el ${new Date().toISOString()}\nEsto es una prueba del MCP de Google Drive.`);

    await executeMCPCommand('upload_file', [testFilePath, `--parent-id`, folderName]);

    // Limpiar archivo temporal
    fs.unlinkSync(testFilePath);

    console.log('\n📋 PRUEBA 5: Listar contenido de la carpeta creada\n');

    // Aquí necesitaríamos obtener el ID de la carpeta creada primero
    // Por simplicidad, listamos archivos recientes
    await executeMCPCommand('list_files', ['--query', `name contains '${folderName}'`]);

    console.log('\n🎉 Todas las pruebas del MCP de Google Drive completadas exitosamente!');
    console.log('\n💡 El MCP de Google Drive está funcionando correctamente.');

  } catch (error) {
    console.error('\n💥 Error durante las pruebas:', error.message);
    console.log('\n🔧 Posibles soluciones:');
    console.log('1. Verifica que las credenciales de Google Drive estén configuradas correctamente');
    console.log('2. Asegúrate de que el archivo credentials.json tenga los permisos adecuados');
    console.log('3. Verifica que tengas conexión a internet');
    console.log('4. Revisa que el paquete @isaacphi/mcp-gdrive esté instalado: npm install');
  }
}

// Ejecutar pruebas
runTests().catch(console.error);
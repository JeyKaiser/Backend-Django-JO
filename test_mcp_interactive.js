#!/usr/bin/env node

/**
 * Script interactivo para probar el MCP de Google Drive
 * Maneja la autenticación OAuth de manera más controlada
 */

import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🚀 Prueba Interactiva del MCP de Google Drive\n');

// Verificar archivos de configuración
console.log('📋 Verificando configuración...');
const credsPath = path.join(__dirname, 'credentials.json');
const tokensDir = path.join(__dirname, 'tokens');

if (!fs.existsSync(credsPath)) {
  console.error('❌ No se encuentra credentials.json');
  process.exit(1);
}

if (!fs.existsSync(tokensDir)) {
  console.log('📁 Creando directorio de tokens...');
  fs.mkdirSync(tokensDir);
}

console.log('✅ Configuración verificada\n');

// Función para ejecutar comando MCP
function executeMCPCommand(command, args = []) {
  return new Promise((resolve, reject) => {
    console.log(`📤 Ejecutando: mcp-gdrive ${command} ${args.join(' ')}\n`);

    const mcpProcess = spawn(
      path.join(__dirname, 'node_modules', '.bin', 'mcp-gdrive.cmd'),
      [command, ...args],
      {
        cwd: __dirname,
        stdio: ['inherit', 'pipe', 'pipe'],
        env: {
          ...process.env,
          GDRIVE_CREDS_DIR: __dirname,
          GOOGLE_APPLICATION_CREDENTIALS: credsPath
        }
      }
    );

    let stdout = '';
    let stderr = '';

    mcpProcess.stdout.on('data', (data) => {
      const output = data.toString();
      stdout += output;
      console.log('📄 Salida:', output.trim());
    });

    mcpProcess.stderr.on('data', (data) => {
      const error = data.toString();
      stderr += error;
      console.log('⚠️  Error:', error.trim());
    });

    mcpProcess.on('close', (code) => {
      console.log(`\n🏁 Comando terminado con código: ${code}`);
      if (code === 0) {
        resolve({ stdout, stderr });
      } else {
        reject(new Error(`Código de salida: ${code}`));
      }
    });

    mcpProcess.on('error', (error) => {
      console.error('💥 Error del proceso:', error.message);
      reject(error);
    });

    // Timeout después de 60 segundos
    setTimeout(() => {
      console.log('\n⏰ Timeout alcanzado, terminando proceso...');
      mcpProcess.kill();
      reject(new Error('Timeout'));
    }, 60000);
  });
}

// Función principal
async function runTest() {
  try {
    console.log('🔐 Si es la primera vez, se abrirá el navegador para autenticación OAuth\n');

    // Intentar listar archivos
    console.log('📂 Intentando listar archivos de Google Drive...\n');
    const result = await executeMCPCommand('list_files', ['--max-results', '5']);

    console.log('\n🎉 ¡Éxito! El MCP de Google Drive está funcionando correctamente.');
    console.log('📊 Resultados obtenidos:', result.stdout.length, 'caracteres');

  } catch (error) {
    console.error('\n💥 Error en la prueba:', error.message);

    if (error.message.includes('Timeout')) {
      console.log('\n💡 El proceso tardó demasiado. Posibles causas:');
      console.log('   - Primera ejecución requiere autenticación OAuth');
      console.log('   - Problemas de conexión a internet');
      console.log('   - Credenciales OAuth expiradas');
    }

    console.log('\n🔧 Verifica:');
    console.log('   1. Que tienes conexión a internet');
    console.log('   2. Que las credenciales OAuth son válidas');
    console.log('   3. Que has completado el flujo de autenticación OAuth');
  }
}

// Ejecutar prueba
runTest().catch(console.error);
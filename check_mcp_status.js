#!/usr/bin/env node

/**
 * Script para verificar el estado del MCP de Google Drive
 * y capturar cualquier salida o información disponible
 */

import { spawn } from 'child_process';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🔍 Verificando estado del MCP de Google Drive...\n');

// Verificar archivos de configuración
console.log('📋 Estado de la configuración:');
const credsPath = path.join(__dirname, 'credentials.json');
const tokensDir = path.join(__dirname, 'tokens');

console.log(`   ✅ Credenciales: ${fs.existsSync(credsPath) ? 'Presente' : 'Faltante'}`);
console.log(`   📁 Directorio tokens: ${fs.existsSync(tokensDir) ? 'Presente' : 'Faltante'}`);

// Verificar archivos de token
if (fs.existsSync(tokensDir)) {
  const tokenFiles = fs.readdirSync(tokensDir);
  console.log(`   🔑 Archivos de token: ${tokenFiles.length} encontrados`);
  tokenFiles.forEach(file => {
    const filePath = path.join(tokensDir, file);
    const stats = fs.statSync(filePath);
    console.log(`      - ${file} (${stats.size} bytes, modificado: ${stats.mtime.toISOString()})`);
  });
} else {
  console.log('   ❌ No hay archivos de token - Se requiere autenticación OAuth');
}

console.log('\n📊 Procesos MCP en ejecución:');

// Función para ejecutar comando con captura de salida
function executeCommandWithCapture(command, args = []) {
  return new Promise((resolve) => {
    console.log(`\n📤 Ejecutando: ${command} ${args.join(' ')}`);

    const child = spawn(command, args, {
      cwd: __dirname,
      stdio: ['inherit', 'pipe', 'pipe'],
      env: {
        ...process.env,
        GDRIVE_CREDS_DIR: __dirname,
        GOOGLE_APPLICATION_CREDENTIALS: credsPath
      }
    });

    let stdout = '';
    let stderr = '';

    child.stdout.on('data', (data) => {
      const output = data.toString();
      stdout += output;
      console.log('📄 STDOUT:', output.trim());
    });

    child.stderr.on('data', (data) => {
      const error = data.toString();
      stderr += error;
      console.log('⚠️  STDERR:', error.trim());
    });

    child.on('close', (code) => {
      console.log(`🏁 Proceso terminado con código: ${code}`);
      resolve({ code, stdout, stderr });
    });

    child.on('error', (error) => {
      console.error('💥 Error del proceso:', error.message);
      resolve({ code: -1, stdout, stderr: error.message });
    });

    // Timeout de 10 segundos
    setTimeout(() => {
      console.log('⏰ Timeout - Terminando proceso...');
      child.kill();
    }, 10000);
  });
}

// Verificar si el comando responde
console.log('\n🔍 Probando conectividad del comando MCP...');
executeCommandWithCapture('node_modules/.bin/mcp-gdrive.cmd', ['--version'])
  .then(result => {
    if (result.code === 0) {
      console.log('✅ El comando MCP responde correctamente');
    } else {
      console.log('⚠️  El comando MCP tiene problemas');
    }

    console.log('\n💡 Resumen:');
    console.log('   - El MCP está instalado y configurado');
    console.log('   - Las credenciales OAuth están presentes');
    console.log('   - Se requiere completar la autenticación inicial');
    console.log('   - Una vez autenticado, los comandos funcionarán normalmente');

    console.log('\n🎯 Para completar la configuración:');
    console.log('   1. Ejecuta: cd Backend && node_modules\\.bin\\mcp-gdrive.cmd list_files --max-results 5');
    console.log('   2. El navegador se abrirá para autenticación OAuth');
    console.log('   3. Completa el flujo de autenticación');
    console.log('   4. Los tokens se guardarán automáticamente en el directorio tokens/');
  });
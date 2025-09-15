#!/usr/bin/env node

/**
 * Prueba simple del MCP de Google Drive
 */

import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

console.log('🚀 Prueba simple del MCP de Google Drive\n');

// Ejecutar comando simple
const mcpBinaryPath = path.join(__dirname, 'node_modules', '.bin', 'mcp-gdrive.cmd');

console.log('📤 Ejecutando: mcp-gdrive list_files --max-results 3');
console.log('Ruta del binario:', mcpBinaryPath);
console.log('Directorio actual:', __dirname);

const child = spawn(mcpBinaryPath, ['list_files', '--max-results', '3'], {
  cwd: __dirname,
  stdio: 'inherit',
  env: {
    ...process.env,
    GDRIVE_CREDS_DIR: __dirname,
    GOOGLE_APPLICATION_CREDENTIALS: path.join(__dirname, 'credentials.json')
  }
});

child.on('close', (code) => {
  console.log(`\n✅ Proceso terminado con código: ${code}`);
});

child.on('error', (error) => {
  console.error('❌ Error:', error.message);
});
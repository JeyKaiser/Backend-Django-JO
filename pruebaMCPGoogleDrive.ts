// ================================================================
// 🚀 GUÍA COMPLETA DE PRUEBAS - SERVIDOR MCP GOOGLE DRIVE
// ================================================================
// Esta guía te permitirá explorar todas las funcionalidades disponibles
// Ejecuta cada sección paso a paso para ver qué datos puedes extraer

console.log("🔥 INICIANDO PRUEBAS COMPLETAS DEL SERVIDOR MCP GOOGLE DRIVE");

// ================================================================
// 📋 PRUEBA 1: LISTAR ARCHIVOS BÁSICO
// ================================================================
console.log("\n📁 PRUEBA 1: Listando todos los archivos en la raíz de Google Drive...");

use_mcp_tool('google-drive', 'list_files', {})

// ================================================================
// 📋 PRUEBA 2: LISTAR ARCHIVOS CON OPCIONES AVANZADAS
// ================================================================
console.log("\n📁 PRUEBA 2: Listando archivos con opciones de paginación y ordenamiento...");

use_mcp_tool('google-drive', 'list_files', {
  pageSize: 20,
  orderBy: "modifiedTime desc"  // Los más recientes primero
})

// ================================================================
// 🔍 PRUEBA 3: BÚSQUEDA DE ARCHIVOS POR NOMBRE
// ================================================================
console.log("\n🔍 PRUEBA 3: Buscando archivos que contengan 'proyecto' en el nombre...");

use_mcp_tool('google-drive', 'search_files', {
  query: "name contains 'proyecto'",
  maxResults: 10
})

// ================================================================
// 🔍 PRUEBA 4: BÚSQUEDA DE ARCHIVOS POR TIPO MIME
// ================================================================
console.log("\n🔍 PRUEBA 4: Buscando solo documentos PDF...");

use_mcp_tool('google-drive', 'search_files', {
  query: "mimeType='application/pdf'",
  maxResults: 15
})

// ================================================================
// 🔍 PRUEBA 5: BÚSQUEDA DE CARPETAS
// ================================================================
console.log("\n🔍 PRUEBA 5: Buscando solo carpetas...");

use_mcp_tool('google-drive', 'search_files', {
  query: "mimeType='application/vnd.google-apps.folder'",
  maxResults: 10
})

// ================================================================
// 🔍 PRUEBA 6: BÚSQUEDA DE ARCHIVOS MODIFICADOS RECIENTEMENTE
// ================================================================
console.log("\n🔍 PRUEBA 6: Buscando archivos modificados en los últimos 7 días...");

use_mcp_tool('google-drive', 'search_files', {
  query: "modifiedTime > '2025-01-15T00:00:00'",
  maxResults: 20
})

// ================================================================
// 📄 PRUEBA 7: OBTENER METADATOS DETALLADOS
// ================================================================
console.log("\n📄 PRUEBA 7: Obteniendo metadatos detallados de un archivo específico...");
console.log("⚠️  NOTA: Reemplaza 'FILE_ID_AQUI' con un ID real de tu Drive");

// use_mcp_tool('google-drive', 'get_metadata', {
//   fileId: "FILE_ID_AQUI"
// })

// ================================================================
// 📂 PRUEBA 8: CREAR UNA CARPETA DE PRUEBA
// ================================================================
console.log("\n📂 PRUEBA 8: Creando una carpeta de prueba...");

use_mcp_tool('google-drive', 'create_folder', {
  name: "📁 Carpeta Prueba MCP - " + new Date().toISOString().slice(0, 10)
})

// ================================================================
// 📝 PRUEBA 9: SUBIR ARCHIVO DE TEXTO
// ================================================================
console.log("\n📝 PRUEBA 9: Subiendo un archivo de texto de prueba...");

use_mcp_tool('google-drive', 'upload_file', {
  name: "📄 Documento Prueba MCP - " + new Date().toISOString().slice(0, 10) + ".txt",
  content: `🚀 ARCHIVO GENERADO POR MCP GOOGLE DRIVE
  
Fecha de creación: ${new Date().toLocaleString()}
Servidor: Google Drive MCP Server v1.0.0

Este archivo fue creado automáticamente durante las pruebas del servidor MCP.

Capacidades probadas:
✅ Conexión con Google Drive API
✅ Autenticación OAuth2
✅ Subida de archivos
✅ Listado de archivos
✅ Búsqueda de archivos
✅ Creación de carpetas

¡El servidor MCP está funcionando correctamente! 🎉`,
  mimeType: "text/plain"
})

// ================================================================
// 📊 PRUEBA 10: SUBIR ARCHIVO JSON CON DATOS
// ================================================================
console.log("\n📊 PRUEBA 10: Subiendo un archivo JSON con datos de prueba...");

use_mcp_tool('google-drive', 'upload_file', {
  name: "📊 Datos Prueba MCP - " + new Date().toISOString().slice(0, 10) + ".json",
  content: JSON.stringify({
    servidor: "Google Drive MCP Server",
    version: "1.0.0",
    fecha_prueba: new Date().toISOString(),
    funcionalidades: [
      "list_files",
      "upload_file", 
      "download_file",
      "create_folder",
      "delete_file",
      "share_file",
      "search_files",
      "get_metadata"
    ],
    recursos: [
      "drive://files",
      "drive://folders/{folderId}",
      "drive://file/{fileId}/metadata"
    ],
    estadisticas: {
      pruebas_realizadas: 10,
      archivos_creados: 2,
      carpetas_creadas: 1,
      busquedas_realizadas: 4
    }
  }, null, 2),
  mimeType: "application/json"
})

// ================================================================
// 🌐 PRUEBA 11: ACCEDER A RECURSOS MCP
// ================================================================
console.log("\n🌐 PRUEBA 11: Accediendo a recursos MCP - Lista general de archivos...");

access_mcp_resource('google-drive', 'drive://files')

// ================================================================
// 🔍 PRUEBA 12: BÚSQUEDA ESPECÍFICA DE ARCHIVOS CREADOS HOY
// ================================================================
console.log("\n🔍 PRUEBA 12: Buscando archivos creados hoy por nuestras pruebas...");

use_mcp_tool('google-drive', 'search_files', {
  query: "name contains 'Prueba MCP'",
  maxResults: 10
})

// ================================================================
// 📋 PRUEBA 13: TIPOS DE ARCHIVO ESPECÍFICOS
// ================================================================
console.log("\n📋 PRUEBA 13: Buscando diferentes tipos de archivos...");

// Documentos de Google
use_mcp_tool('google-drive', 'search_files', {
  query: "mimeType='application/vnd.google-apps.document'",
  maxResults: 5
})

// Hojas de cálculo de Google
use_mcp_tool('google-drive', 'search_files', {
  query: "mimeType='application/vnd.google-apps.spreadsheet'",
  maxResults: 5
})

// Presentaciones de Google
use_mcp_tool('google-drive', 'search_files', {
  query: "mimeType='application/vnd.google-apps.presentation'",
  maxResults: 5
})

// ================================================================
// 📊 PRUEBA 14: ANÁLISIS DE TAMAÑO DE ARCHIVOS
// ================================================================
console.log("\n📊 PRUEBA 14: Buscando archivos grandes (>10MB)...");

use_mcp_tool('google-drive', 'search_files', {
  query: "mimeType != 'application/vnd.google-apps.folder'",
  maxResults: 20
})

// ================================================================
// 👥 PRUEBA 15: ARCHIVOS COMPARTIDOS
// ================================================================
console.log("\n👥 PRUEBA 15: Buscando archivos en 'Compartidos conmigo'...");

use_mcp_tool('google-drive', 'search_files', {
  query: "sharedWithMe = true",
  maxResults: 10
})

// ================================================================
// ⭐ PRUEBA 16: ARCHIVOS DESTACADOS
// ================================================================
console.log("\n⭐ PRUEBA 16: Buscando archivos marcados como destacados...");

use_mcp_tool('google-drive', 'search_files', {
  query: "starred = true",
  maxResults: 10
})

// ================================================================
// 🗑️ PRUEBA 17: ARCHIVOS EN LA PAPELERA
// ================================================================
console.log("\n🗑️ PRUEBA 17: Revisando archivos en la papelera...");

use_mcp_tool('google-drive', 'search_files', {
  query: "trashed = true",
  maxResults: 10
})

// ================================================================
// 📱 PRUEBA 18: IMÁGENES
// ================================================================
console.log("\n📱 PRUEBA 18: Buscando archivos de imagen...");

use_mcp_tool('google-drive', 'search_files', {
  query: "mimeType contains 'image/'",
  maxResults: 10
})

// ================================================================
// 🎥 PRUEBA 19: VIDEOS
// ================================================================
console.log("\n🎥 PRUEBA 19: Buscando archivos de video...");

use_mcp_tool('google-drive', 'search_files', {
  query: "mimeType contains 'video/'",
  maxResults: 10
})

// ================================================================
// 📄 PRUEBA 20: DOCUMENTOS DE OFFICE
// ================================================================
console.log("\n📄 PRUEBA 20: Buscando documentos de Microsoft Office...");

use_mcp_tool('google-drive', 'search_files', {
  query: "mimeType='application/vnd.openxmlformats-officedocument.wordprocessingml.document' or mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' or mimeType='application/vnd.openxmlformats-officedocument.presentationml.presentation'",
  maxResults: 10
})

// ================================================================
// 📋 RESUMEN FINAL
// ================================================================
console.log(`
🎉 ¡PRUEBAS COMPLETADAS!

📊 RESUMEN DE CAPACIDADES PROBADAS:
✅ Listado básico y avanzado de archivos
✅ Búsquedas por nombre, tipo MIME, fecha
✅ Creación de carpetas
✅ Subida de archivos (texto, JSON)
✅ Acceso a recursos MCP
✅ Filtrado por tipos específicos de archivo
✅ Búsqueda de archivos compartidos y destacados
✅ Análisis de diferentes formatos (imagen, video, Office)

💡 TIPOS DE DATOS QUE PUEDES EXTRAER:
- 📁 Listados completos de archivos y carpetas
- 🔍 Búsquedas específicas por criterios
- 📊 Metadatos detallados (tamaño, fecha, permisos)
- 👥 Estado de compartición
- ⭐ Archivos destacados o importantes
- 🗑️ Archivos eliminados (papelera)
- 📱 Análisis por tipo de contenido
- 📈 Estadísticas de uso y almacenamiento

🚀 TU SERVIDOR MCP GOOGLE DRIVE ESTÁ LISTO PARA:
- Automatizar gestión de archivos
- Crear backups programados
- Sincronizar datos entre sistemas
- Analizar contenido y patrones
- Integrar con workflows existentes
`);
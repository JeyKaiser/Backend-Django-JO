import { GoogleDriveMCPServer } from '@isaacphi/mcp-gdrive';

async function testGoogleDrive() {
    try {
        console.log('🚀 Iniciando prueba de Google Drive MCP...');

        const server = new GoogleDriveMCPServer();

        console.log('✅ Servidor MCP creado correctamente');

        // Intentar listar archivos
        console.log('📁 Listando archivos de Google Drive...');
        const files = await server.listFiles();

        console.log(`✅ Archivos encontrados: ${files.length}`);

        if (files.length > 0) {
            console.log('\n📋 Primeros 10 archivos:');
            files.slice(0, 10).forEach((file, index) => {
                console.log(`${index + 1}. ${file.name || 'Sin nombre'} (${file.id})`);
            });
        }

        console.log('\n✅ Prueba completada exitosamente');

    } catch (error) {
        console.error('❌ Error durante la prueba:', error.message);
        console.error('Stack:', error.stack);
    }
}

testGoogleDrive();
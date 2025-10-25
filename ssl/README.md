# Certificados SSL para JO System

## Estado Actual
- ✅ `key.pem` - Clave privada generada
- ✅ `cert.pem` - Certificado autofirmado creado (temporal)
- ⚠️ Requiere certificados válidos para producción

## Para Producción Real
1. Obtener certificado válido de una CA (Let's Encrypt, etc.)
2. O generar certificado autofirmado válido con OpenSSL

## Firewall
- Requiere permisos de administrador para configurar
- Comando sugerido: `netsh advfirewall firewall add rule name="JO System Backend" dir=in action=allow protocol=TCP localport=8000 remoteip=192.168.0.0/24`

## Notas de Seguridad
- Certificado actual es solo para desarrollo/testing
- No usar en producción sin certificado válido
- Configurar renovación automática de certificados
# Informe para Frontend - Modal de Creación de Parámetros

## Objetivo
Crear un modal con formulario de opciones múltiples en la URL `http://localhost:3000/modules/categorias` que permita al usuario crear registros en la tabla PARAMETROS de SAP HANA.

## Endpoints Backend Disponibles

### Endpoints para Obtener Opciones (GET)
```
- GET /api/sap/base_textil/     → Lista de BASE_TEXTIL
- GET /api/sap/tela/           → Lista de TELA  
- GET /api/sap/print/          → Lista de PRINT
- GET /api/sap/hilo_tela/      → Lista de HILO_DE_TELA
- GET /api/sap/hilo_molde/     → Lista de HILO_DE_MOLDE
- GET /api/sap/canal_tela/     → Lista de CANAL_TELA
- GET /api/sap/sentido_sesgos/ → Lista de SENTIDO_SESGOS
- GET /api/sap/rotacion_molde/ → Lista de ROTACION_MOLDE
- GET /api/sap/restricciones_tela/ → Lista de RESTRICCIONES_TELA
```

### Endpoint para Crear Parámetro (POST)
```
POST /api/sap/parametros/
```

## Estructura del Modal

### 1. Botón de Activación
```javascript
// Crear botón en la página http://localhost:3000/modules/categorias
<button 
  className="btn btn-primary" 
  onClick={() => setShowParametrosModal(true)}
>
  + Crear Parámetro
</button>
```

### 2. Campos del Formulario
El modal debe contener los siguientes campos como **select/dropdown**:

| Campo | Endpoint para Options | Campo en BD | Requerido |
|-------|---------------------|-------------|-----------|
| Código | Input manual | CODIGO | ✅ |
| Base Textil | `/api/sap/base_textil/` | BASE_TEXTIL_ID | ✅ |
| Tela | `/api/sap/tela/` | TELA_ID | ✅ |
| Print | `/api/sap/print/` | PRINT_ID | ✅ |
| Hilo de Tela | `/api/sap/hilo_tela/` | HILO_DE_TELA_ID | ✅ |
| Hilo de Molde | `/api/sap/hilo_molde/` | HILO_DE_MOLDE_ID | ✅ |
| Canal Tela | `/api/sap/canal_tela/` | CANAL_TELA_ID | ✅ |
| Sentido Sesgos | `/api/sap/sentido_sesgos/` | SENTIDO_SESGOS_ID | ✅ |
| Rotación Molde | `/api/sap/rotacion_molde/` | ROTACION_MOLDE_ID | ✅ |
| Restricciones | `/api/sap/restricciones_tela/` | RESTRICCIONES_ID | ✅ |

### 3. Ejemplo de Estructura del Modal (React)

```jsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ParametrosModal = ({ isOpen, onClose }) => {
  const [formData, setFormData] = useState({
    codigo: '',
    baseTextilId: '',
    telaId: '',
    printId: '',
    hiloTelaId: '',
    hiloMoldeId: '',
    canalTelaId: '',
    sentidoSesgosId: '',
    rotacionMoldeId: '',
    restriccionesId: ''
  });

  const [options, setOptions] = useState({
    baseTextil: [],
    tela: [],
    print: [],
    hiloTela: [],
    hiloMolde: [],
    canalTela: [],
    sentidoSesgos: [],
    rotacionMolde: [],
    restriccionesTela: []
  });

  const [loading, setLoading] = useState(true);

  // Cargar todas las opciones al abrir el modal
  useEffect(() => {
    if (isOpen) {
      loadAllOptions();
    }
  }, [isOpen]);

  const loadAllOptions = async () => {
    try {
      const endpoints = [
        { key: 'baseTextil', url: '/api/sap/base_textil/' },
        { key: 'tela', url: '/api/sap/tela/' },
        { key: 'print', url: '/api/sap/print/' },
        { key: 'hiloTela', url: '/api/sap/hilo_tela/' },
        { key: 'hiloMolde', url: '/api/sap/hilo_molde/' },
        { key: 'canalTela', url: '/api/sap/canal_tela/' },
        { key: 'sentidoSesgos', url: '/api/sap/sentido_sesgos/' },
        { key: 'rotacionMolde', url: '/api/sap/rotacion_molde/' },
        { key: 'restriccionesTela', url: '/api/sap/restricciones_tela/' }
      ];

      const promises = endpoints.map(endpoint => 
        axios.get(`http://localhost:8000${endpoint.url}`)
      );
      
      const responses = await Promise.all(promises);
      
      const newOptions = {};
      endpoints.forEach((endpoint, index) => {
        newOptions[endpoint.key] = responses[index].data;
      });
      
      setOptions(newOptions);
      setLoading(false);
    } catch (error) {
      console.error('Error cargando opciones:', error);
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      const payload = {
        CODIGO: formData.codigo,
        BASE_TEXTIL_ID: parseInt(formData.baseTextilId),
        TELA_ID: parseInt(formData.telaId),
        PRINT_ID: parseInt(formData.printId),
        HILO_DE_TELA_ID: parseInt(formData.hiloTelaId),
        HILO_DE_MOLDE_ID: parseInt(formData.hiloMoldeId),
        CANAL_TELA_ID: parseInt(formData.canalTelaId),
        SENTIDO_SESGOS_ID: parseInt(formData.sentidoSesgosId),
        ROTACION_MOLDE_ID: parseInt(formData.rotacionMoldeId),
        RESTRICCIONES_ID: parseInt(formData.restriccionesId)
      };

      await axios.post('http://localhost:8000/api/sap/parametros/', payload);
      
      alert('Parámetro creado exitosamente!');
      onClose();
      
      // Resetear formulario
      setFormData({
        codigo: '', baseTextilId: '', telaId: '', printId: '',
        hiloTelaId: '', hiloMoldeId: '', canalTelaId: '',
        sentidoSesgosId: '', rotacionMoldeId: '', restriccionesId: ''
      });
      
    } catch (error) {
      console.error('Error creando parámetro:', error);
      alert('Error al crear parámetro: ' + error.response?.data?.error);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Crear Nuevo Parámetro</h2>
          <button onClick={onClose} className="close-btn">×</button>
        </div>
        
        {loading ? (
          <div className="loading">Cargando opciones...</div>
        ) : (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>Código *</label>
              <input
                type="text"
                value={formData.codigo}
                onChange={(e) => setFormData({...formData, codigo: e.target.value})}
                required
                placeholder="Ejemplo: 001"
              />
            </div>

            <div className="form-group">
              <label>Base Textil *</label>
              <select
                value={formData.baseTextilId}
                onChange={(e) => setFormData({...formData, baseTextilId: e.target.value})}
                required
              >
                <option value="">Seleccione...</option>
                {options.baseTextil.map(item => (
                  <option key={item.ID} value={item.ID}>
                    {item.DESCRIPCION || item.NOMBRE || `ID: ${item.ID}`}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Tela *</label>
              <select
                value={formData.telaId}
                onChange={(e) => setFormData({...formData, telaId: e.target.value})}
                required
              >
                <option value="">Seleccione...</option>
                {options.tela.map(item => (
                  <option key={item.ID} value={item.ID}>
                    {item.DESCRIPCION || item.NOMBRE || `ID: ${item.ID}`}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Print *</label>
              <select
                value={formData.printId}
                onChange={(e) => setFormData({...formData, printId: e.target.value})}
                required
              >
                <option value="">Seleccione...</option>
                {options.print.map(item => (
                  <option key={item.ID} value={item.ID}>
                    {item.DESCRIPCION || item.NOMBRE || `ID: ${item.ID}`}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Hilo de Tela *</label>
              <select
                value={formData.hiloTelaId}
                onChange={(e) => setFormData({...formData, hiloTelaId: e.target.value})}
                required
              >
                <option value="">Seleccione...</option>
                {options.hiloTela.map(item => (
                  <option key={item.ID} value={item.ID}>
                    {item.DESCRIPCION || item.NOMBRE || `ID: ${item.ID}`}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Hilo de Molde *</label>
              <select
                value={formData.hiloMoldeId}
                onChange={(e) => setFormData({...formData, hiloMoldeId: e.target.value})}
                required
              >
                <option value="">Seleccione...</option>
                {options.hiloMolde.map(item => (
                  <option key={item.ID} value={item.ID}>
                    {item.DESCRIPCION || item.NOMBRE || `ID: ${item.ID}`}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Canal Tela *</label>
              <select
                value={formData.canalTelaId}
                onChange={(e) => setFormData({...formData, canalTelaId: e.target.value})}
                required
              >
                <option value="">Seleccione...</option>
                {options.canalTela.map(item => (
                  <option key={item.ID} value={item.ID}>
                    {item.DESCRIPCION || item.NOMBRE || `ID: ${item.ID}`}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Sentido Sesgos *</label>
              <select
                value={formData.sentidoSesgosId}
                onChange={(e) => setFormData({...formData, sentidoSesgosId: e.target.value})}
                required
              >
                <option value="">Seleccione...</option>
                {options.sentidoSesgos.map(item => (
                  <option key={item.ID} value={item.ID}>
                    {item.DESCRIPCION || item.NOMBRE || `ID: ${item.ID}`}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Rotación Molde *</label>
              <select
                value={formData.rotacionMoldeId}
                onChange={(e) => setFormData({...formData, rotacionMoldeId: e.target.value})}
                required
              >
                <option value="">Seleccione...</option>
                {options.rotacionMolde.map(item => (
                  <option key={item.ID} value={item.ID}>
                    {item.DESCRIPCION || item.NOMBRE || `ID: ${item.ID}`}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-group">
              <label>Restricciones *</label>
              <select
                value={formData.restriccionesId}
                onChange={(e) => setFormData({...formData, restriccionesId: e.target.value})}
                required
              >
                <option value="">Seleccione...</option>
                {options.restriccionesTela.map(item => (
                  <option key={item.ID} value={item.ID}>
                    {item.DESCRIPCION || item.NOMBRE || `ID: ${item.ID}`}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-actions">
              <button type="button" onClick={onClose} className="btn btn-secondary">
                Cancelar
              </button>
              <button type="submit" className="btn btn-primary">
                Crear Parámetro
              </button>
            </div>
          </form>
        )}
      </div>
    </div>
  );
};

export default ParametrosModal;
```

### 4. CSS Sugerido

```css
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 0;
}

.modal-header {
  padding: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #999;
}

.form-group {
  margin: 15px 20px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
}

.form-actions {
  padding: 20px;
  border-top: 1px solid #eee;
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
}

.btn-primary {
  background-color: #007bff;
  color: white;
}

.btn-secondary {
  background-color: #6c757d;
  color: white;
}

.loading {
  padding: 40px;
  text-align: center;
  color: #666;
}
```

### 5. Integración en la Página Categorías

```jsx
// En la página http://localhost:3000/modules/categorias
import React, { useState } from 'react';
import ParametrosModal from './components/ParametrosModal';

const CategoriasPage = () => {
  const [showParametrosModal, setShowParametrosModal] = useState(false);

  return (
    <div>
      <h1>Categorías</h1>
      
      <div className="page-actions">
        <button 
          className="btn btn-primary"
          onClick={() => setShowParametrosModal(true)}
        >
          + Crear Parámetro
        </button>
      </div>

      {/* Contenido existente de la página */}

      <ParametrosModal 
        isOpen={showParametrosModal}
        onClose={() => setShowParametrosModal(false)}
      />
    </div>
  );
};

export default CategoriasPage;
```

## Notas Importantes

1. **IDs de Base de Datos**: Los IDs son generados automáticamente por la base de datos
2. **Validaciones**: El backend validará que todos los IDs existan en sus respectivas tablas
3. **Estructura de Response**: Cada endpoint devuelve un array de objetos con estructura `{ID: number, ...otros campos}`
4. **Error Handling**: Implementar manejo de errores tanto para la carga de opciones como para el envío del formulario

Este modal permitirá al usuario seleccionar de manera intuitiva todas las opciones necesarias para crear un nuevo parámetro en la tabla PARAMETROS de SAP HANA.
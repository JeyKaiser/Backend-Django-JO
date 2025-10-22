-- Script de inicialización para Supabase
-- Ejecutar este script en Supabase SQL Editor para crear el esquema consumo_textil

-- Crear esquema
DROP SCHEMA IF EXISTS consumo_textil CASCADE;
CREATE SCHEMA consumo_textil;
SET search_path TO consumo_textil;

-- Tabla: DIM_PRENDA
CREATE TABLE consumo_textil.dim_prenda (
    prenda_id BIGSERIAL PRIMARY KEY,
    tipo_prenda_nombre VARCHAR(100) NOT NULL
);

-- Tabla: DIM_CANTIDAD_TELAS
CREATE TABLE consumo_textil.dim_cantidad_telas (
    cantidad_telas_id BIGSERIAL PRIMARY KEY,
    cantidad_telas_numero INTEGER NOT NULL
);

-- Tabla: DIM_USO_TELA
CREATE TABLE consumo_textil.dim_uso_tela (
    uso_tela_id BIGSERIAL PRIMARY KEY,
    uso_tela_nombre VARCHAR(50) NOT NULL
);

-- Tabla: DIM_BASE_TEXTIL
CREATE TABLE consumo_textil.dim_base_textil (
    base_textil_id BIGSERIAL PRIMARY KEY,
    base_textil_nombre VARCHAR(100) NOT NULL
);

-- Tabla: DIM_CARACTERISTICA_COLOR
CREATE TABLE consumo_textil.dim_caracteristica_color (
    caracteristica_color_id BIGSERIAL PRIMARY KEY,
    caracteristica_nombre VARCHAR(50) NOT NULL
);

-- Tabla: DIM_ANCHO_UTIL
CREATE TABLE consumo_textil.dim_ancho_util (
    ancho_util_id BIGSERIAL PRIMARY KEY,
    ancho_util_metros DECIMAL(5,2) NOT NULL
);

-- Tabla: DIM_FOTOS
CREATE TABLE consumo_textil.dim_fotos (
    foto_id BIGSERIAL PRIMARY KEY,
    prenda_id BIGINT,
    foto_bytea BYTEA,
    nombre_archivo VARCHAR(255)
);

-- Tabla: DIM_PROPIEDADES_TELA
CREATE TABLE consumo_textil.dim_propiedades_tela (
    propiedades_tela_id BIGSERIAL PRIMARY KEY,
    al_hilo_flag BOOLEAN DEFAULT FALSE,
    al_sesgo_flag BOOLEAN DEFAULT FALSE,
    noventa_grados_flag BOOLEAN DEFAULT FALSE,
    peine_flag BOOLEAN DEFAULT FALSE,
    brilloviz_flag BOOLEAN DEFAULT FALSE,
    grabado_flag BOOLEAN DEFAULT FALSE,
    sentido_moldes_flag VARCHAR(50),
    canal_tela_flag BOOLEAN DEFAULT FALSE
);

-- Tabla: DIM_VARIANTE
CREATE TABLE consumo_textil.dim_variante (
    variante_id BIGSERIAL PRIMARY KEY,
    numero_variante INTEGER NOT NULL
);

-- Tabla: DIM_DESCRIPCION
CREATE TABLE consumo_textil.dim_descripcion (
    descripcion_id BIGSERIAL PRIMARY KEY,
    detalle_descripcion VARCHAR(500) NOT NULL
);

-- Tabla: DIM_TERMINACION
CREATE TABLE consumo_textil.dim_terminacion (
    terminacion_id BIGSERIAL PRIMARY KEY,
    categoria_terminacion VARCHAR(50) NOT NULL,
    tipo_terminacion VARCHAR(50) NOT NULL,
    fecha_creacion DATE DEFAULT CURRENT_DATE
);

-- Tabla: FACT_CONSUMO
CREATE TABLE consumo_textil.fact_consumo (
    consumo_id BIGSERIAL PRIMARY KEY,
    prenda_id BIGINT NOT NULL,
    cantidad_telas_id BIGINT NOT NULL,
    uso_tela_id BIGINT NOT NULL,
    base_textil_id BIGINT NOT NULL,
    caracteristica_color_id BIGINT NOT NULL,
    ancho_util_id BIGINT NOT NULL,
    propiedades_tela_id BIGINT NOT NULL,
    consumo_mtr DECIMAL(10,4) NOT NULL,
    variante_id BIGINT,
    descripcion_id BIGINT,
    terminacion_id BIGINT,
    FOREIGN KEY (prenda_id) REFERENCES consumo_textil.dim_prenda(prenda_id),
    FOREIGN KEY (cantidad_telas_id) REFERENCES consumo_textil.dim_cantidad_telas(cantidad_telas_id),
    FOREIGN KEY (uso_tela_id) REFERENCES consumo_textil.dim_uso_tela(uso_tela_id),
    FOREIGN KEY (base_textil_id) REFERENCES consumo_textil.dim_base_textil(base_textil_id),
    FOREIGN KEY (caracteristica_color_id) REFERENCES consumo_textil.dim_caracteristica_color(caracteristica_color_id),
    FOREIGN KEY (ancho_util_id) REFERENCES consumo_textil.dim_ancho_util(ancho_util_id),
    FOREIGN KEY (propiedades_tela_id) REFERENCES consumo_textil.dim_propiedades_tela(propiedades_tela_id),
    FOREIGN KEY (variante_id) REFERENCES consumo_textil.dim_variante(variante_id),
    FOREIGN KEY (descripcion_id) REFERENCES consumo_textil.dim_descripcion(descripcion_id),
    FOREIGN KEY (terminacion_id) REFERENCES consumo_textil.dim_terminacion(terminacion_id)
);

-- Insertar datos básicos (primeras filas de cada dimensión)
INSERT INTO consumo_textil.dim_prenda (tipo_prenda_nombre) VALUES
('BIKINI BOTTOM - ALTO'),
('BIKINI BOTTOM - PANTY'),
('BIKINI TOP - TIRAS');

INSERT INTO consumo_textil.dim_cantidad_telas (cantidad_telas_numero) VALUES (1), (2), (3);

INSERT INTO consumo_textil.dim_uso_tela (uso_tela_nombre) VALUES
('LUCIR'), ('FORRO'), ('FUSIONABLE');

INSERT INTO consumo_textil.dim_base_textil (base_textil_nombre) VALUES
('LYCRA VITA'), ('LYCRA BAHIA'), ('FUSIONABLE');

INSERT INTO consumo_textil.dim_caracteristica_color (caracteristica_nombre) VALUES
('SOLIDO'), ('MODIFICACION'), ('UBICACION');

INSERT INTO consumo_textil.dim_ancho_util (ancho_util_metros) VALUES (1.20), (1.45), (1.50);

INSERT INTO consumo_textil.dim_propiedades_tela (al_hilo_flag, al_sesgo_flag, sentido_moldes_flag, canal_tela_flag) VALUES
(TRUE, FALSE, 'A TRAVEZ', TRUE),
(FALSE, TRUE, 'AL HILO', TRUE);

INSERT INTO consumo_textil.dim_variante (numero_variante) VALUES (1), (2), (3);

INSERT INTO consumo_textil.dim_descripcion (detalle_descripcion) VALUES
('LUCIR Y FORRO'),
('LUCIR, SESGO, ENTREPIERNA Y FUSIONABLE');

INSERT INTO consumo_textil.dim_terminacion (categoria_terminacion, tipo_terminacion) VALUES
('ACABADO', 'EMBONADO'),
('COSTURA', 'PANUELO');

-- Insertar algunos datos de ejemplo en fact_consumo
INSERT INTO consumo_textil.fact_consumo (
    prenda_id, cantidad_telas_id, uso_tela_id, base_textil_id,
    caracteristica_color_id, ancho_util_id, propiedades_tela_id,
    consumo_mtr, variante_id, descripcion_id, terminacion_id
) VALUES
(1, 2, 1, 1, 1, 1, 1, 0.17, 1, 1, 1),
(2, 1, 1, 1, 1, 2, 1, 0.19, 1, 1, 1),
(3, 2, 1, 2, 1, 3, 2, 0.15, 1, 2, 2);
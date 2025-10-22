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
    foto_bytea BYTEA, -- reemplazo de BLOB
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

-- =====================================================================================
-- 3. DEFINICIÓN DE RELACIONES (CLAVES FORÁNEAS)
-- =====================================================================================

-- Relaciones básicas
ALTER TABLE consumo_textil.fact_consumo 
ADD CONSTRAINT fk_fact_prenda 
FOREIGN KEY (prenda_id) 
REFERENCES consumo_textil.dim_prenda (prenda_id);

ALTER TABLE consumo_textil.fact_consumo 
ADD CONSTRAINT fk_fact_cantidad_telas 
FOREIGN KEY (cantidad_telas_id) 
REFERENCES consumo_textil.dim_cantidad_telas (cantidad_telas_id);

ALTER TABLE consumo_textil.fact_consumo 
ADD CONSTRAINT fk_fact_uso_tela 
FOREIGN KEY (uso_tela_id) 
REFERENCES consumo_textil.dim_uso_tela (uso_tela_id);

ALTER TABLE consumo_textil.fact_consumo 
ADD CONSTRAINT fk_fact_base_textil 
FOREIGN KEY (base_textil_id) 
REFERENCES consumo_textil.dim_base_textil (base_textil_id);

ALTER TABLE consumo_textil.fact_consumo 
ADD CONSTRAINT fk_fact_caracteristica_color 
FOREIGN KEY (caracteristica_color_id) 
REFERENCES consumo_textil.dim_caracteristica_color (caracteristica_color_id);

ALTER TABLE consumo_textil.fact_consumo 
ADD CONSTRAINT fk_fact_ancho_util 
FOREIGN KEY (ancho_util_id) 
REFERENCES consumo_textil.dim_ancho_util (ancho_util_id);

ALTER TABLE consumo_textil.fact_consumo 
ADD CONSTRAINT fk_fact_propiedades_tela 
FOREIGN KEY (propiedades_tela_id) 
REFERENCES consumo_textil.dim_propiedades_tela (propiedades_tela_id);

-- Nuevas relaciones para entidades adicionales
ALTER TABLE consumo_textil.fact_consumo 
ADD CONSTRAINT fk_fact_variante 
FOREIGN KEY (variante_id) 
REFERENCES consumo_textil.dim_variante (variante_id);

ALTER TABLE consumo_textil.fact_consumo 
ADD CONSTRAINT fk_fact_descripcion 
FOREIGN KEY (descripcion_id) 
REFERENCES consumo_textil.dim_descripcion (descripcion_id);

ALTER TABLE consumo_textil.fact_consumo 
ADD CONSTRAINT fk_fact_terminacion 
FOREIGN KEY (terminacion_id) 
REFERENCES consumo_textil.dim_terminacion (terminacion_id);

-- =====================================================================================
-- 4. INSERCIÓN DE DATOS EN TABLAS DE DIMENSIONES (PostgreSQL)
-- =====================================================================================

-- Datos DIM_PRENDA
INSERT INTO consumo_textil.dim_prenda (tipo_prenda_nombre)
VALUES
 ('BIKINI BOTTOM - ALTO'),
 ('BIKINI BOTTOM - PANTY'),
 ('BIKINI TOP - TIRAS'),
 ('BIKINI TOP - TIRAS - U'),
 ('BIKINI TOP - TIRAS - NUDO'),
 ('BIKINI TOP - STRAPLESS'),
 ('BIKINI TOP - STRAPLESS - U'),
 ('BIKINI TOP - STRAPLESS - ENTORCHE');

-- Datos DIM_CANTIDAD_TELAS
INSERT INTO consumo_textil.dim_cantidad_telas (cantidad_telas_numero)
VALUES
 (1),
 (2),
 (3),
 (4);

-- Datos DIM_USO_TELA
INSERT INTO consumo_textil.dim_uso_tela (uso_tela_nombre)
VALUES
 ('LUCIR'),
 ('LUCIR 2'),
 ('LUCIR 3'),
 ('LUCIR Y FORRO'),
 ('FORRO'),
 ('FORRO 2'),
 ('FORRO 3'),
 ('FUSIONABLE'),
 ('FUSIONABLE 2'),
 ('SESGO LUCIR'),
 ('SESGO LUCIR 2'),
 ('SESGO LUCIR 3'),
 ('SESGO FORRO'),
 ('SESGO FORRO 1'),
 ('SESGO FORRO 2'),
 ('SESGO FUSIONABLE'),
 ('SESGO FUSIONABLE 2');

-- Datos DIM_BASE_TEXTIL
INSERT INTO consumo_textil.dim_base_textil (base_textil_nombre)
VALUES
 ('LYCRA VITA'),
 ('LYCRA BAHIA'),
 ('LYCRA CRINKLE'),
 ('LYCRA SUMATRA'),
 ('FUSIONABLE'),
 ('LYCRA SHIMMERING'),
 ('LYCRA TABITA'),
 ('LYCRA TERRY'),
 ('COTTON VOILE');

-- Datos DIM_CARACTERISTICA_COLOR
INSERT INTO consumo_textil.dim_caracteristica_color (caracteristica_nombre)
VALUES
 ('SOLIDO'),
 ('MODIFICACION'),
 ('UBICACION');

-- Datos DIM_ANCHO_UTIL
INSERT INTO consumo_textil.dim_ancho_util (ancho_util_metros)
VALUES
 (1.20),
 (1.45),
 (1.46),
 (1.48),
 (1.50),
 (1.52),
 (1.54),
 (1.56),
 (1.42),
 (1.51),
 (1.53),
 (1.35);
-- =====================================================================================
-- 4. INSERCIÓN DE DATOS EN TABLAS DE DIMENSIONES (PostgreSQL)
-- =====================================================================================

-- Datos DIM_PROPIEDADES_TELA
INSERT INTO consumo_textil.dim_propiedades_tela (
    al_hilo_flag, 
    al_sesgo_flag, 
    noventa_grados_flag,    
    peine_flag, 
    brilloviz_flag, 
    grabado_flag, 
    sentido_moldes_flag,
    canal_tela_flag)
VALUES
 (TRUE,  FALSE, FALSE, FALSE, FALSE, FALSE, 'A TRAVEZ', TRUE),
 (FALSE, TRUE,  FALSE, FALSE, FALSE, FALSE, 'AL HILO',  TRUE),
 (TRUE,  FALSE, TRUE,  FALSE, FALSE, FALSE, 'AL HILO',  TRUE),
 (FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 'AL HILO',  TRUE),
 (FALSE, FALSE, FALSE, FALSE, FALSE, FALSE, 'SESGO',    TRUE);

-- Datos DIM_VARIANTE
INSERT INTO consumo_textil.dim_variante (numero_variante)
VALUES
 (1),
 (2),
 (3),
 (4),
 (5),
 (6);

-- Datos DIM_DESCRIPCION
INSERT INTO consumo_textil.dim_descripcion (detalle_descripcion)
VALUES
 ('LUCIR Y FORRO'),
 ('LUCIR, SESGO, ENTREPIERNA Y FUSIONABLE'),
 ('LUCIR, FORRO Y SESGO TIRAS. EN LA MISMA TELA'),
 ('LUCIR SHIMMERING Y FORRO (TIRAS EN FORRO)'),
 ('LUCIR LYCRA Y FORRO (TIRAS EN FORRO)'),
 ('LUCIR Y FORRO (SESGO EN FORRO)'),
 ('LUCIR SHIMMERING, FORRO Y FUS (TIRAS EN FORRO)'),
 ('LUCIR LYCRA, FORRO Y FUS (TIRAS EN LUCIR)'),
 ('LUCIR Y FORRO (TIRAS EN LUCIR)'),
 ('LUCIR Y TIRAS EN FORRO'),
 ('LUCIR, FORRO Y FUS'),
 ('LUCIR, FORRO, FUS Y TIRAS EN LUCIR 2'),
 ('LUCIR + FORRO Y FUS');

-- Datos DIM_TERMINACION
INSERT INTO consumo_textil.dim_terminacion (categoria_terminacion, tipo_terminacion)
VALUES
 ('ACABADO', 'EMBONADO'),
 ('ACABADO', 'SESGADO'),
 ('ACABADO', 'EMBONADO Y SESGADO'),
 ('COSTURA', 'PANUELO'),
 ('COSTURA', 'DOBLADILLO');

-- =====================================================================================
-- 5. INSERCIÓN DE DATOS EN TABLA DE HECHOS (FACT_CONSUMO)
-- =====================================================================================

INSERT INTO consumo_textil.fact_consumo (
 prenda_id, cantidad_telas_id, uso_tela_id, base_textil_id, caracteristica_color_id, ancho_util_id, 
 propiedades_tela_id, consumo_mtr, variante_id, descripcion_id, terminacion_id)
VALUES
-- BIKINI BOTTOM (ALTO) 2 TELAS VARIANTE 1
 (1, 2, 1, 1, 1, 2, 1, 0.17, 1, 1, 1),
 (1, 2, 1, 1, 1, 3, 1, 0.17, 1, 1, 1),
 (1, 2, 1, 1, 1, 4, 1, 0.17, 1, 1, 1),
 (1, 2, 1, 1, 1, 5, 1, 0.16, 1, 1, 1),
 (1, 2, 1, 1, 2, 2, 1, 0.36, 1, 1, 1),
 (1, 2, 1, 1, 2, 3, 1, 0.35, 1, 1, 1),
 (1, 2, 1, 1, 2, 4, 1, 0.35, 1, 1, 1),
 (1, 2, 1, 1, 2, 5, 1, 0.35, 1, 1, 1),
 (1, 2, 5, 2, 1, 4, 2, 0.18, 1, 1, 1),
 (1, 2, 5, 2, 1, 5, 2, 0.17, 1, 1, 1),
 (1, 2, 5, 2, 1, 7, 3, 0.17, 1, 1, 1),
 (1, 2, 5, 2, 1, 8, 4, 0.17, 1, 1, 1),
-- BIKINI BOTTOM (ALTO) 4 TELAS VARIANTE 1
 (1, 4, 1, 3, 1, 1, 2, 0.19, 1, 2, 2),
 (1, 4, 1, 3, 2, 1, 2, 0.75, 1, 2, 2),
 (1, 4, 1, 3, 3, 1, 2, 0.00, 1, 2, 2),
 (1, 4, 5, 2, 1, 4, 5, 0.02, 1, 2, 2),
 (1, 4, 5, 2, 1, 5, 5, 0.02, 1, 2, 2),
 (1, 4, 5, 2, 1, 7, 5, 0.02, 1, 2, 2),
 (1, 4, 5, 2, 1, 8, 5, 0.02, 1, 2, 2),
 (1, 4, 11, 2, 1, 4, 5, 0.06, 1, 2, 2),
 (1, 4, 11, 2, 1, 5, 5, 0.06, 1, 2, 2),
 (1, 4, 11, 2, 1, 7, 5, 0.05, 1, 2, 2),
 (1, 4, 11, 2, 1, 8, 5, 0.05, 1, 2, 2),
 (1, 4, 8, 5, 1, 5, 5, 0.01, 1, 2, 2),
-- BIKINI BOTTOM (PANTY) 1 TELA VARIANTE 1
 (2, 1, 4, 2, 1, 4, 1, 0.19, 1, 3, 1),
 (2, 1, 4, 2, 1, 5, 1, 0.18, 1, 3, 1),
 (2, 1, 4, 2, 1, 7, 1, 0.18, 1, 3, 1),
 (2, 1, 4, 2, 1, 8, 1, 0.18, 1, 3, 1),
-- BIKINI BOTTOM (PANTY) 2 TELAS VARIANTE 1
 (2, 2, 1, 6, 1, 1, 1, 0.15, 1, 4, 1),
 (2, 2, 1, 6, 2, 1, 1, 0.37, 1, 4, 1),
 (2, 2, 5, 2, 1, 4, 1, 0.09, 1, 4, 1),
 (2, 2, 5, 2, 1, 5, 1, 0.09, 1, 4, 1),
 (2, 2, 5, 2, 1, 7, 1, 0.09, 1, 4, 1),
 (2, 2, 5, 2, 1, 8, 1, 0.09, 1, 4, 1),
 (2, 2, 5, 7, 1, 5, 1, 0.09, 1, 4, 1),
 (2, 2, 5, 7, 1, 2, 1, 0.09, 1, 4, 1),
 (2, 2, 5, 7, 1, 4, 1, 0.09, 1, 4, 1),
-- BIKINI BOTTOM (PANTY) 2 TELAS VARIANTE 2
 (2, 2, 1, 4, 1, 9, 1, 0.10, 2, 5, 1),
 (2, 2, 1, 4, 1, 1, 1, 0.10, 2, 5, 1),
 (2, 2, 1, 4, 1, 2, 1, 0.09, 2, 5, 1),
 (2, 2, 1, 4, 1, 4, 1, 0.09, 2, 5, 1),
 (2, 2, 1, 4, 1, 10, 1, 0.09, 2, 5, 1),
 (2, 2, 1, 4, 1, 11, 1, 0.09, 2, 5, 1),
 (2, 2, 1, 1, 1, 2, 1, 0.10, 2, 5, 1),
 (2, 2, 1, 1, 1, 3, 1, 0.10, 2, 5, 1),
 (2, 2, 1, 1, 1, 4, 1, 0.09, 2, 5, 1),
 (2, 2, 1, 1, 1, 5, 1, 0.09, 2, 5, 1),
 (2, 2, 1, 2, 1, 4, 1, 0.10, 2, 5, 1),
 (2, 2, 1, 2, 1, 5, 1, 0.10, 2, 5, 1),
 (2, 2, 1, 2, 1, 7, 1, 0.09, 2, 5, 1),
 (2, 2, 1, 2, 1, 8, 1, 0.09, 2, 5, 1),
 (2, 2, 5, 2, 1, 4, 1, 0.09, 2, 5, 1),
 (2, 2, 5, 2, 1, 5, 1, 0.09, 2, 5, 1),
 (2, 2, 5, 2, 1, 7, 1, 0.09, 2, 5, 1),
 (2, 2, 5, 2, 1, 8, 1, 0.09, 2, 5, 1);

-- Consultas de tablas de dimensiones
SELECT * FROM consumo_textil.dim_prenda;
SELECT * FROM consumo_textil.dim_cantidad_telas;
SELECT * FROM consumo_textil.dim_uso_tela;
SELECT * FROM consumo_textil.dim_base_textil;
SELECT * FROM consumo_textil.dim_caracteristica_color;
SELECT * FROM consumo_textil.dim_ancho_util;
SELECT * FROM consumo_textil.dim_fotos;              -- pendiente de implementar servidor
SELECT * FROM consumo_textil.dim_propiedades_tela;
SELECT * FROM consumo_textil.dim_variante;
SELECT * FROM consumo_textil.dim_descripcion;
SELECT * FROM consumo_textil.dim_terminacion;

-- Tabla de hechos (ordenada)
SELECT * FROM consumo_textil.fact_consumo ORDER BY consumo_id ASC;

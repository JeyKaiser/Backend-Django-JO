from datetime import datetime, timezone


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


PRENDAS = [
    {'prenda_id': 1, 'tipo_prenda_nombre': 'Blusa'},
    {'prenda_id': 2, 'tipo_prenda_nombre': 'Vestido'},
    {'prenda_id': 3, 'tipo_prenda_nombre': 'Pantalon'},
    {'prenda_id': 4, 'tipo_prenda_nombre': 'Falda'},
]

DIM_CANTIDAD_TELAS = [
    {'cantidad_telas_id': 1, 'cantidad_telas_numero': 1},
    {'cantidad_telas_id': 2, 'cantidad_telas_numero': 2},
    {'cantidad_telas_id': 3, 'cantidad_telas_numero': 3},
]

DIM_USO_TELA = [
    {'uso_tela_id': 1, 'uso_tela_nombre': 'Principal'},
    {'uso_tela_id': 2, 'uso_tela_nombre': 'Forro'},
    {'uso_tela_id': 3, 'uso_tela_nombre': 'Contraste'},
]

DIM_BASE_TEXTIL = [
    {'base_textil_id': 1, 'base_textil_nombre': 'Algodon'},
    {'base_textil_id': 2, 'base_textil_nombre': 'Lino'},
    {'base_textil_id': 3, 'base_textil_nombre': 'Satin'},
]

DIM_CARACTERISTICA_COLOR = [
    {'caracteristica_color_id': 1, 'caracteristica_nombre': 'Solido'},
    {'caracteristica_color_id': 2, 'caracteristica_nombre': 'Estampado'},
    {'caracteristica_color_id': 3, 'caracteristica_nombre': 'Texturizado'},
]

DIM_ANCHO_UTIL = [
    {'ancho_util_id': 1, 'ancho_util_metros': 1.40},
    {'ancho_util_id': 2, 'ancho_util_metros': 1.50},
    {'ancho_util_id': 3, 'ancho_util_metros': 1.60},
]

DIM_PROPIEDADES_TELA = [
    {'propiedades_tela_id': 1, 'nombre': 'Al hilo'},
    {'propiedades_tela_id': 2, 'nombre': 'Con brillo'},
    {'propiedades_tela_id': 3, 'nombre': 'Con canal'},
]

DIM_VARIANTE = [
    {'variante_id': 1, 'numero_variante': 'V1'},
    {'variante_id': 2, 'numero_variante': 'V2'},
    {'variante_id': 3, 'numero_variante': 'V3'},
]

DIM_DESCRIPCION = [
    {'descripcion_id': 1, 'detalle_descripcion': 'Base principal'},
    {'descripcion_id': 2, 'detalle_descripcion': 'Complemento'},
]

DIM_TERMINACION = [
    {'terminacion_id': 1, 'categoria_terminacion': 'Lavado'},
    {'terminacion_id': 2, 'categoria_terminacion': 'Estampado'},
    {'terminacion_id': 3, 'categoria_terminacion': 'Tejido'},
]

PARAMETER_OPTIONS = {
    'base_textil': [
        {'ID': 1, 'NOMBRE': 'Algodon'},
        {'ID': 2, 'NOMBRE': 'Lino'},
        {'ID': 3, 'NOMBRE': 'Satin'},
    ],
    'tela': [
        {'ID': 1, 'NOMBRE': 'Popelina'},
        {'ID': 2, 'NOMBRE': 'Twill'},
        {'ID': 3, 'NOMBRE': 'Crepe'},
    ],
    'print': [
        {'ID': 1, 'NOMBRE': 'NINGUNO'},
        {'ID': 2, 'NOMBRE': 'FLORAL'},
        {'ID': 3, 'NOMBRE': 'GEOMETRICO'},
    ],
    'hilo_tela': [
        {'ID': 1, 'NOMBRE': 'Normal'},
        {'ID': 2, 'NOMBRE': 'Bordado'},
    ],
    'hilo_molde': [
        {'ID': 1, 'NOMBRE': 'Vertical'},
        {'ID': 2, 'NOMBRE': 'Horizontal'},
    ],
    'canal_tela': [
        {'ID': 1, 'NOMBRE': 'No'},
        {'ID': 2, 'NOMBRE': 'Si'},
    ],
    'sentido_sesgos': [
        {'ID': 1, 'NOMBRE': 'Unico'},
        {'ID': 2, 'NOMBRE': 'Doble'},
    ],
    'rotacion_molde': [
        {'ID': 1, 'NOMBRE': 'Permitida'},
        {'ID': 2, 'NOMBRE': 'No permitida'},
    ],
    'restricciones_tela': [
        {'ID': 1, 'NOMBRE': 'NINGUNA'},
        {'ID': 2, 'NOMBRE': 'No vapor'},
        {'ID': 3, 'NOMBRE': 'No sesgo'},
    ],
}

PARAMETERS_VIEW = [
    {
        'CODIGO': 'PAR-001',
        'BASE_TEXTIL': 'Algodon',
        'TELA': 'Popelina',
        'ANCHO': 1.50,
        'PRINT': 'NINGUNO',
        'HILO_DE_TELA': 'Normal',
        'HILO_DE_MOLDE': 'Vertical',
        'CANAL_TELA': 'No',
        'SENTIDO_SESGOS': 'Unico',
        'ROTACION_MOLDE': 'Permitida',
        'RESTRICCIONES_TELA': 'NINGUNA',
        'CREATED_AT': _now_iso(),
    }
]

CONSUMOS_BY_REFERENCE = {
    'PT03708': [
        {
            'COLECCION': 'SUMMER 2026',
            'NOMBRE_REF': 'Vestido estructurado',
            'USO_EN_PRENDA': 'Principal',
            'COD_TELA': 'TELA-001',
            'NOMBRE_TELA': 'Popelina',
            'CONSUMO': 2.35,
        },
        {
            'COLECCION': 'SUMMER 2026',
            'NOMBRE_REF': 'Vestido estructurado',
            'USO_EN_PRENDA': 'Forro',
            'COD_TELA': 'TELA-002',
            'NOMBRE_TELA': 'Satin liviano',
            'CONSUMO': 1.15,
        },
    ]
}

CONSUMO_TEXTIL = [
    {
        'indice': 1,
        'uso_tela': 'Principal',
        'base_textil': 'Algodon',
        'caracteristica_color': 'Solido',
        'consumo_mtr': 2.35,
        'ancho_util_metros': 1.50,
        'cantidad_telas': 1,
        'numero_variante': 'V1',
        'tipo_prenda': 'Vestido',
        'descripcion_variante': 'Base principal',
    },
    {
        'indice': 2,
        'uso_tela': 'Forro',
        'base_textil': 'Satin',
        'caracteristica_color': 'Solido',
        'consumo_mtr': 1.15,
        'ancho_util_metros': 1.40,
        'cantidad_telas': 2,
        'numero_variante': 'V2',
        'tipo_prenda': 'Vestido',
        'descripcion_variante': 'Complemento',
    },
]


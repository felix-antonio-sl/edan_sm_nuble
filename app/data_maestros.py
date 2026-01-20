# === DATOS MAESTROS ===
# Fuente: establecimientos_nuble.csv (DEIS)
# Filtro: Todos los CESFAM y Hospitales de la región + Postas solo de El Carmen y Coelemu

COMUNAS_POR_PROVINCIA = {
    "Diguillín": [
        "Bulnes",
        "Chillán",
        "Chillán Viejo",
        "El Carmen",
        "Pemuco",
        "Pinto",
        "Quillón",
        "San Ignacio",
        "Yungay",
    ],
    "Punilla": ["Coihueco", "Ñiquén", "San Carlos", "San Fabián", "San Nicolás"],
    "Itata": [
        "Cobquecura",
        "Coelemu",
        "Ninhue",
        "Portezuelo",
        "Quirihue",
        "Ránquil",
        "Treguaco",
    ],
}

COMUNA_A_PROVINCIA = {
    "Bulnes": "Diguillín",
    "Chillán": "Diguillín",
    "Chillán Viejo": "Diguillín",
    "El Carmen": "Diguillín",
    "Pemuco": "Diguillín",
    "Pinto": "Diguillín",
    "Quillón": "Diguillín",
    "San Ignacio": "Diguillín",
    "Yungay": "Diguillín",
    "Coihueco": "Punilla",
    "Ñiquén": "Punilla",
    "San Carlos": "Punilla",
    "San Fabián": "Punilla",
    "San Nicolás": "Punilla",
    "Cobquecura": "Itata",
    "Coelemu": "Itata",
    "Ninhue": "Itata",
    "Portezuelo": "Itata",
    "Quirihue": "Itata",
    "Ránquil": "Itata",
    "Treguaco": "Itata",
}

ESTABLECIMIENTOS = [
    # === HOSPITALES (Toda la región) ===
    {
        "codigo": "117103",
        "nombre": "Hospital Comunitario de Salud Familiar de Bulnes",
        "comuna": "Bulnes",
    },
    {
        "codigo": "117104",
        "nombre": "Hospital Comunitario de Salud Familiar Pedro Morales Campos (Yungay)",
        "comuna": "Yungay",
    },
    {
        "codigo": "117106",
        "nombre": "Hospital Comunitario de Salud Familiar de Quirihue",
        "comuna": "Quirihue",
    },
    {
        "codigo": "117107",
        "nombre": "Hospital Comunitario de Salud Familiar de El Carmen",
        "comuna": "El Carmen",
    },
    {
        "codigo": "117108",
        "nombre": "Hospital Comunitario de Salud Familiar Dr. Eduardo Contreras Trabucco de Coelemu",
        "comuna": "Coelemu",
    },
    # === CESFAM (Toda la región) ===
    # Bulnes
    {
        "codigo": "117326",
        "nombre": "Centro de Salud Familiar Santa Clara",
        "comuna": "Bulnes",
    },
    # Chillán
    {
        "codigo": "117301",
        "nombre": "Centro de Salud Familiar Violeta Parra",
        "comuna": "Chillán",
    },
    {
        "codigo": "117302",
        "nombre": "Centro de Salud Familiar San Ramón Nonato",
        "comuna": "Chillán",
    },
    {
        "codigo": "117303",
        "nombre": "Centro de Salud Familiar Ultraestación Dr. Raúl San Martín González",
        "comuna": "Chillán",
    },
    {
        "codigo": "117304",
        "nombre": "Centro de Salud Familiar Isabel Riquelme",
        "comuna": "Chillán",
    },
    {
        "codigo": "117322",
        "nombre": "Centro de Salud Familiar Quinchamalí",
        "comuna": "Chillán",
    },
    {
        "codigo": "117324",
        "nombre": "Centro de Salud Familiar Los Volcanes",
        "comuna": "Chillán",
    },
    {
        "codigo": "117330",
        "nombre": "Centro de Salud Familiar Sol de Oriente",
        "comuna": "Chillán",
    },
    # Chillán Viejo
    {
        "codigo": "117328",
        "nombre": "Centro de Salud Familiar Dr. Federico Puga",
        "comuna": "Chillán Viejo",
    },
    {
        "codigo": "117331",
        "nombre": "Centro de Salud Familiar Dra. Michelle Bachelet Jeria",
        "comuna": "Chillán Viejo",
    },
    # Cobquecura
    {
        "codigo": "117307",
        "nombre": "Centro de Salud Familiar Cobquecura",
        "comuna": "Cobquecura",
    },
    # Coihueco
    {
        "codigo": "117318",
        "nombre": "Centro de Salud Familiar Michelle Chandía Alarcón",
        "comuna": "Coihueco",
    },
    {
        "codigo": "117325",
        "nombre": "Centro de Salud Familiar Luis Montecinos",
        "comuna": "Coihueco",
    },
    # Ninhue
    {
        "codigo": "117314",
        "nombre": "Centro de Salud Familiar Dr. David Benavente de Ninhue",
        "comuna": "Ninhue",
    },
    # Ñiquén
    {
        "codigo": "117313",
        "nombre": "Centro de Salud Familiar Ñiquén",
        "comuna": "Ñiquén",
    },
    # Pemuco
    {
        "codigo": "117310",
        "nombre": "Centro de Salud Familiar Pemuco",
        "comuna": "Pemuco",
    },
    # Pinto
    {"codigo": "117317", "nombre": "Centro de Salud Familiar Pinto", "comuna": "Pinto"},
    # Portezuelo
    {
        "codigo": "117305",
        "nombre": "Centro de Salud Familiar Portezuelo",
        "comuna": "Portezuelo",
    },
    # Quillón
    {
        "codigo": "117306",
        "nombre": "Centro de Salud Familiar Dr. Alberto Gyhra Soto (Quillón)",
        "comuna": "Quillón",
    },
    # Ránquil
    {
        "codigo": "117316",
        "nombre": "Centro de Salud Familiar Ñipas",
        "comuna": "Ránquil",
    },
    # San Carlos
    {
        "codigo": "117311",
        "nombre": "Centro de Salud Familiar Dr. José Duran Trujillo",
        "comuna": "San Carlos",
    },
    {
        "codigo": "117329",
        "nombre": "Centro de Salud Familiar Teresa Baldechi",
        "comuna": "San Carlos",
    },
    # San Fabián
    {
        "codigo": "117309",
        "nombre": "Centro de Salud Familiar San Fabián",
        "comuna": "San Fabián",
    },
    # San Ignacio
    {
        "codigo": "117308",
        "nombre": "CESFAM DR. ALFONSO PARRA CARRIEL",
        "comuna": "San Ignacio",
    },
    {
        "codigo": "117319",
        "nombre": "Centro de Salud Familiar Quiriquina",
        "comuna": "San Ignacio",
    },
    {
        "codigo": "117455",
        "nombre": "Centro de Salud Familiar Pueblo Seco",
        "comuna": "San Ignacio",
    },
    # San Nicolás
    {
        "codigo": "117312",
        "nombre": "Centro de Salud Familiar San Nicolás",
        "comuna": "San Nicolás",
    },
    # Treguaco
    {
        "codigo": "117327",
        "nombre": "Centro de Salud Familiar Treguaco",
        "comuna": "Treguaco",
    },
    # Yungay
    {
        "codigo": "117315",
        "nombre": "Centro de Salud Familiar Campanario",
        "comuna": "Yungay",
    },
    # === POSTAS (Solo El Carmen y Coelemu) ===
    # El Carmen
    {
        "codigo": "117477",
        "nombre": "Posta de Salud Rural Chamizal",
        "comuna": "El Carmen",
    },
    {
        "codigo": "117475",
        "nombre": "Posta de Salud Rural Castañal",
        "comuna": "El Carmen",
    },
    {
        "codigo": "117473",
        "nombre": "Posta de Salud Rural Capilla Sur",
        "comuna": "El Carmen",
    },
    {
        "codigo": "117435",
        "nombre": "Posta de Salud Rural Trehualemu",
        "comuna": "El Carmen",
    },
    {
        "codigo": "117457",
        "nombre": "Posta de Salud Rural Capilla Norte",
        "comuna": "El Carmen",
    },
    {
        "codigo": "117438",
        "nombre": "Posta de Salud Rural Huemul",
        "comuna": "El Carmen",
    },
    {
        "codigo": "117474",
        "nombre": "Posta de Salud Rural Agua Santa",
        "comuna": "El Carmen",
    },
    {
        "codigo": "117476",
        "nombre": "Posta de Salud Rural Las Hormigas",
        "comuna": "El Carmen",
    },
    {
        "codigo": "117437",
        "nombre": "Posta de Salud Rural San Vicente (El Carmen)",
        "comuna": "El Carmen",
    },
    {
        "codigo": "117436",
        "nombre": "Posta de Salud Rural Pedregal de Zapallar",
        "comuna": "El Carmen",
    },
    # Coelemu
    {
        "codigo": "117439",
        "nombre": "Posta de Salud Rural Ranguelmo",
        "comuna": "Coelemu",
    },
    {
        "codigo": "117442",
        "nombre": "Posta de Salud Rural Guarilihue",
        "comuna": "Coelemu",
    },
    {
        "codigo": "117445",
        "nombre": "Posta de Salud Rural Vegas de Itata",
        "comuna": "Coelemu",
    },
]

"""
This module serves as the entry point for executing the Apify Actor. It handles the configuration of logging
settings. The `main()` coroutine is then executed using `asyncio.run()`.

Feel free to modify this file to suit your specific needs.
"""

import asyncio
import logging

from apify.log import ActorLogFormatter

from .main import main

# Configure loggers
handler = logging.StreamHandler()
handler.setFormatter(ActorLogFormatter())

apify_client_logger = logging.getLogger('apify_client')
apify_client_logger.setLevel(logging.INFO)
apify_client_logger.addHandler(handler)

apify_logger = logging.getLogger('apify')
apify_logger.setLevel(logging.DEBUG)
apify_logger.addHandler(handler)

# Execute the Actor main coroutine
#asyncio.run(main())

# PISOS
# FILTRES APLICATS
    # 2 hab
    # 2 lavabos
    # aire acondicionat

    # EIXAMPLE
        # COMPRA
page_url = f'https://www.idealista.com/venta-viviendas/barcelona/eixample/con-metros-cuadrados-menos-de_100,solo-pisos,de-dos-dormitorios,dos-banos,ascensor,exterior,aireacondicionado,plantas-intermedias,buen-estado/'
filename = 'pisos-eixample-2hab-2lav-con_aire-compra'
    #main(page_url,filename)
        # LLOGUER
page_url2 = 'https://www.idealista.com/alquiler-viviendas/barcelona/eixample/con-metros-cuadrados-menos-de_100,solo-pisos,de-dos-dormitorios,dos-banos,amueblado_amueblados,ascensor,exterior,aireacondicionado,plantas-intermedias,buen-estado/?ordenado-por=precios-asc'
filename2 = 'pisos-eixample-2hab-2lav-con_aire-lloguer'
    #main(page_url2,filename2)
    # SAGRADA FAMILIA
        # COMPRA
page_url3 = 'https://www.idealista.com/venta-viviendas/barcelona/eixample/la-sagrada-familia/con-metros-cuadrados-menos-de_100,solo-pisos,de-dos-dormitorios,dos-banos,ascensor,exterior,aireacondicionado,plantas-intermedias,buen-estado/'
filename3 = 'pisos-sagrada_familia-2hab-2lav-con_aire-compra'
asyncio.run(main(page_url3, filename3))

        # LLOGUER
page_url4 = 'https://www.idealista.com/alquiler-viviendas/barcelona/eixample/la-sagrada-familia/con-metros-cuadrados-menos-de_100,solo-pisos,de-dos-dormitorios,dos-banos,amueblado_amueblados,ascensor,exterior,aireacondicionado,plantas-intermedias,buen-estado/?ordenado-por=precio-metro-cuadrado-asc'
filename4 = 'pisos-sagrada_familia-2hab-2lav-con_aire-lloguer'
    #main(page_url4,filename4)

# FILTRES APLICATS
    # 2 hab
    # 1 lavabo
    # aire acondicionat
        # COMPRA
page_url5 = f'https://www.idealista.com/venta-viviendas/barcelona/eixample/con-metros-cuadrados-menos-de_100,solo-pisos,de-dos-dormitorios,un-bano,ascensor,exterior,aireacondicionado,plantas-intermedias,buen-estado/'
filename5 = 'pisos-eixample-2hab-1lav-con_aire-compra'
    #main(page_url5,filename5)
        # LLOGUER
page_url6 = 'https://www.idealista.com/alquiler-viviendas/barcelona/eixample/con-metros-cuadrados-menos-de_100,solo-pisos,de-dos-dormitorios,un-bano,amueblado_amueblados,ascensor,exterior,aireacondicionado,plantas-intermedias,buen-estado/?ordenado-por=precio-metro-cuadrado-asc'

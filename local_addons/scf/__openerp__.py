{
    'name':'System Client Facturing',
    'version': '1.0',
    'depends': ['base_setup'],
    'author': 'Victor Pino victopin0@gmail.com',
    'category': '',
    'description': """
    App to manage a system client of facturing
    """,
    'update_xml': [],
    "data" : [
        "views/client_view.xml",
        "views/res_company_view.xml",
        "views/country_view.xml",
        "views/city_view.xml",
        "views/cell_phone_view.xml",
        "views/provider_view.xml",
        ],
    'installable': True,
    'auto_install': False,
}
from django.db import connections


def _check_mysql() -> tuple[bool, str]:
    try:
        connection = connections['default']
        connection.ensure_connection()
        with connection.cursor() as cursor:
            cursor.execute('SELECT 1')
            cursor.fetchone()
        return True, 'MYSQL OK'
    except Exception as exc:
        return False, f'MYSQL ERROR: {exc}'


def _check_sap() -> tuple[bool, str]:
    try:
        from sap.services import get_provider

        provider = get_provider()
        ok, message = provider.is_available()
        if ok:
            return True, f'SAP OK ({message})'
        return False, f'SAP ERROR: {message}'
    except Exception as exc:
        return False, f'SAP ERROR: {exc}'


def print_startup_status() -> None:
    mysql_ok, mysql_message = _check_mysql()
    sap_ok, sap_message = _check_sap()

    if mysql_ok and sap_ok:
        print('SISTEMA CONECTADO CORRECTAMENTE A MYSQL Y SAP')
        print(f'{mysql_message} | {sap_message}')
    else:
        print('SISTEMA NO CONECTADO COMPLETAMENTE')
        print(f'{mysql_message} | {sap_message}')

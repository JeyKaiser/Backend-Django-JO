from django.conf import settings
from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    help = "Create the MySQL database if possible and run Django migrations."

    def handle(self, *args, **options):
        db_settings = settings.DATABASES["default"]
        engine = db_settings.get("ENGINE", "")
        if "mysql" not in engine:
            self.stdout.write(self.style.WARNING("Default database is not MySQL. Skipping bootstrap."))
            return

        database_name = db_settings.get("NAME") or "diseno"
        user = db_settings.get("USER") or "root"
        password = db_settings.get("PASSWORD") or ""
        host = db_settings.get("HOST") or "127.0.0.1"
        port = int(db_settings.get("PORT") or 3306)

        self.stdout.write(f"Connecting to MySQL server at {host}:{port} as {user!r}")

        try:
            import pymysql
        except ImportError as exc:
            raise RuntimeError("PyMySQL is not installed in this environment.") from exc

        try:
            connection = pymysql.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                charset="utf8mb4",
                autocommit=True,
            )
        except Exception as exc:
            raise RuntimeError(
                "Could not connect to MySQL server. Verify MYSQL_HOST, MYSQL_PORT, MYSQL_USER and MYSQL_PASSWORD."
            ) from exc

        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    f"CREATE DATABASE IF NOT EXISTS `{database_name}` "
                    "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
                )
                self.stdout.write(self.style.SUCCESS(f"Database ready: {database_name}"))
        finally:
            connection.close()

        self.stdout.write("Applying Django migrations...")
        call_command("migrate", interactive=False, verbosity=1)
        self.stdout.write(self.style.SUCCESS("MySQL bootstrap completed successfully."))

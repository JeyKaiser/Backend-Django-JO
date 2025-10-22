2025-10-22T04:53:38.560542027Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/registry.py", line 89, in run_checks
2025-10-22T04:53:38.560567239Z     new_errors = check(app_configs=app_configs, databases=databases)
2025-10-22T04:53:38.560573299Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/urls.py", line 16, in check_url_config
2025-10-22T04:53:38.560577119Z     return check_resolver(resolver)
2025-10-22T04:53:38.56058087Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/urls.py", line 26, in check_resolver
2025-10-22T04:53:38.56058503Z     return check_method()
2025-10-22T04:53:38.56058938Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 531, in check
2025-10-22T04:53:38.560596131Z     for pattern in self.url_patterns:
2025-10-22T04:53:38.560600061Z                    ^^^^^^^^^^^^^^^^^
2025-10-22T04:53:38.560603871Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/utils/functional.py", line 47, in __get__
2025-10-22T04:53:38.560607941Z     res = instance.__dict__[self.name] = self.func(instance)
2025-10-22T04:53:38.560611882Z                                          ~~~~~~~~~^^^^^^^^^^
2025-10-22T04:53:38.560615812Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 718, in url_patterns
2025-10-22T04:53:38.560633993Z     patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
2025-10-22T04:53:38.560636643Z                        ^^^^^^^^^^^^^^^^^^^
2025-10-22T04:53:38.560639014Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/utils/functional.py", line 47, in __get__
2025-10-22T04:53:38.560641184Z     res = instance.__dict__[self.name] = self.func(instance)
2025-10-22T04:53:38.560643764Z                                          ~~~~~~~~~^^^^^^^^^^
2025-10-22T04:53:38.560646114Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 711, in urlconf_module
2025-10-22T04:53:38.560648454Z     return import_module(self.urlconf_name)
2025-10-22T04:53:38.560650774Z   File "/opt/render/project/python/Python-3.13.4/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-10-22T04:53:38.560653224Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-10-22T04:53:38.560655625Z            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-10-22T04:53:38.560658085Z   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-10-22T04:53:38.560660525Z   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-10-22T04:53:38.560662935Z   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-10-22T04:53:38.560665135Z   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-10-22T04:53:38.560669746Z   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-10-22T04:53:38.560672346Z   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-10-22T04:53:38.560674716Z   File "/opt/render/project/src/JO_System_Project/urls.py", line 35, in <module>
2025-10-22T04:53:38.560677306Z     path('api/consumos/', include('consumos.urls')),
2025-10-22T04:53:38.560679516Z                           ~~~~~~~^^^^^^^^^^^^^^^^^
2025-10-22T04:53:38.560682077Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/conf.py", line 39, in include
2025-10-22T04:53:38.560684547Z     urlconf_module = import_module(urlconf_module)
2025-10-22T04:53:38.560686797Z   File "/opt/render/project/python/Python-3.13.4/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-10-22T04:53:38.560689047Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-10-22T04:53:38.560691327Z            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-10-22T04:53:38.560700148Z   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-10-22T04:53:38.560702738Z   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-10-22T04:53:38.560705048Z   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-10-22T04:53:38.560707348Z   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-10-22T04:53:38.560709548Z   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-10-22T04:53:38.560711708Z   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-10-22T04:53:38.560714089Z   File "/opt/render/project/src/consumos/urls.py", line 2, in <module>
2025-10-22T04:53:38.560716619Z     from .views import ConsumosAPIView
2025-10-22T04:53:38.560718849Z   File "/opt/render/project/src/consumos/views.py", line 5, in <module>
2025-10-22T04:53:38.560721099Z     from sap.views import execute_hana_query
2025-10-22T04:53:38.560723329Z ModuleNotFoundError: No module named 'sap'
2025-10-22T04:53:41.178322324Z ==> Exited with status 1
2025-10-22T04:53:41.197083002Z ==> Common ways to troubleshoot your deploy: https://render.com/docs/troubleshooting-deploys
2025-10-22T04:53:48.420033719Z ==> Running 'python manage.py migrate && python manage.py collectstatic --noinput && gunicorn JO_System_Project.wsgi:application --bind 0.0.0.0:$PORT'
2025-10-22T04:53:57.004693677Z Traceback (most recent call last):
2025-10-22T04:53:57.008052307Z   File "/opt/render/project/src/manage.py", line 21, in <module>
2025-10-22T04:53:57.008075068Z     main()
2025-10-22T04:53:57.00809187Z     ~~~~^^
2025-10-22T04:53:57.00809644Z   File "/opt/render/project/src/manage.py", line 18, in main
2025-10-22T04:53:57.00810146Z     execute_from_command_line(sys.argv)
2025-10-22T04:53:57.008105561Z     ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^
2025-10-22T04:53:57.008110161Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/__init__.py", line 442, in execute_from_command_line
2025-10-22T04:53:57.008115171Z     utility.execute()
2025-10-22T04:53:57.008118951Z     ~~~~~~~~~~~~~~~^^
2025-10-22T04:53:57.008123252Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/__init__.py", line 436, in execute
2025-10-22T04:53:57.008127052Z     self.fetch_command(subcommand).run_from_argv(self.argv)
2025-10-22T04:53:57.008131002Z     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^
2025-10-22T04:53:57.008134823Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/base.py", line 416, in run_from_argv
2025-10-22T04:53:57.008138803Z     self.execute(*args, **cmd_options)
2025-10-22T04:53:57.008142523Z     ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^
2025-10-22T04:53:57.008152134Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/base.py", line 457, in execute
2025-10-22T04:53:57.008156894Z     self.check(**check_kwargs)
2025-10-22T04:53:57.008160754Z     ~~~~~~~~~~^^^^^^^^^^^^^^^^
2025-10-22T04:53:57.008164854Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/management/base.py", line 492, in check
2025-10-22T04:53:57.008168755Z     all_issues = checks.run_checks(
2025-10-22T04:53:57.008172595Z         app_configs=app_configs,
2025-10-22T04:53:57.008176215Z     ...<2 lines>...
2025-10-22T04:53:57.008180046Z         databases=databases,
2025-10-22T04:53:57.008183936Z     )
2025-10-22T04:53:57.008187986Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/registry.py", line 89, in run_checks
2025-10-22T04:53:57.008192496Z     new_errors = check(app_configs=app_configs, databases=databases)
2025-10-22T04:53:57.008196447Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/urls.py", line 16, in check_url_config
2025-10-22T04:53:57.008200387Z     return check_resolver(resolver)
2025-10-22T04:53:57.008204147Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/core/checks/urls.py", line 26, in check_resolver
2025-10-22T04:53:57.008208208Z     return check_method()
2025-10-22T04:53:57.008217748Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 531, in check
2025-10-22T04:53:57.008221929Z     for pattern in self.url_patterns:
2025-10-22T04:53:57.008225829Z                    ^^^^^^^^^^^^^^^^^
2025-10-22T04:53:57.008229639Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/utils/functional.py", line 47, in __get__
2025-10-22T04:53:57.008233349Z     res = instance.__dict__[self.name] = self.func(instance)
2025-10-22T04:53:57.00823729Z                                          ~~~~~~~~~^^^^^^^^^^
2025-10-22T04:53:57.00824113Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 718, in url_patterns
2025-10-22T04:53:57.008257551Z     patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
2025-10-22T04:53:57.008260271Z                        ^^^^^^^^^^^^^^^^^^^
2025-10-22T04:53:57.008266721Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/utils/functional.py", line 47, in __get__
2025-10-22T04:53:57.008269492Z     res = instance.__dict__[self.name] = self.func(instance)
2025-10-22T04:53:57.008271852Z                                          ~~~~~~~~~^^^^^^^^^^
2025-10-22T04:53:57.008274502Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/resolvers.py", line 711, in urlconf_module
2025-10-22T04:53:57.008277092Z     return import_module(self.urlconf_name)
2025-10-22T04:53:57.008282593Z   File "/opt/render/project/python/Python-3.13.4/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-10-22T04:53:57.008285363Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-10-22T04:53:57.008287943Z            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-10-22T04:53:57.008293623Z   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-10-22T04:53:57.008314115Z   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-10-22T04:53:57.008340846Z   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-10-22T04:53:57.008384489Z   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-10-22T04:53:57.00838804Z   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-10-22T04:53:57.00839419Z   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-10-22T04:53:57.008431743Z   File "/opt/render/project/src/JO_System_Project/urls.py", line 35, in <module>
2025-10-22T04:53:57.008435463Z     path('api/consumos/', include('consumos.urls')),
2025-10-22T04:53:57.008438403Z                           ~~~~~~~^^^^^^^^^^^^^^^^^
2025-10-22T04:53:57.008447994Z   File "/opt/render/project/src/.venv/lib/python3.13/site-packages/django/urls/conf.py", line 39, in include
2025-10-22T04:53:57.008450674Z     urlconf_module = import_module(urlconf_module)
2025-10-22T04:53:57.008521509Z   File "/opt/render/project/python/Python-3.13.4/lib/python3.13/importlib/__init__.py", line 88, in import_module
2025-10-22T04:53:57.008525489Z     return _bootstrap._gcd_import(name[level:], package, level)
2025-10-22T04:53:57.008528059Z            ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
2025-10-22T04:53:57.0085335Z   File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
2025-10-22T04:53:57.008655648Z   File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
2025-10-22T04:53:57.008663599Z   File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
2025-10-22T04:53:57.008666539Z   File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
2025-10-22T04:53:57.008669159Z   File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
2025-10-22T04:53:57.008671849Z   File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
2025-10-22T04:53:57.00867825Z   File "/opt/render/project/src/consumos/urls.py", line 2, in <module>
2025-10-22T04:53:57.00868141Z     from .views import ConsumosAPIView
2025-10-22T04:53:57.00868683Z   File "/opt/render/project/src/consumos/views.py", line 5, in <module>
2025-10-22T04:53:57.008689941Z     from sap.views import execute_hana_query
2025-10-22T04:53:57.008740354Z ModuleNotFoundError: No module named 'sap'
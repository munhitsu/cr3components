Philosophy
----------
KISS



Usage
-----
update settings.py with
CR3SETTINGS = {
    'ASK.EXPERT.EMAIL':'cr3@example.com',
}



Superuser editable key value store for settings
At this point only django db backend is available

However following steps are planned:
1. Django independent admin interface to simple key value store
   - seamles part of standard django admin
   - quick way to drop django admin connections
2. implement redis backend
3. mongo backend
4. other backends
5. ACL


It shall not evolve into nosql abstract layer


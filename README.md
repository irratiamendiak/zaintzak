# Zaintzak eta itzaltzeak

Web app para organizar y liquidar las guardias de retenes y uraskas y las horas de extinción en incendios forestales, con consultas y certificados bilingües en PDF.

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `index.html` | La aplicación (interfaz en euskera). |
| `config.js` | Datos de conexión con Supabase. |
| `data.json` | Datos iniciales: recursos, guardias, incendios e intervenciones. |
| `supabase.sql` | Crea la base de datos en Supabase (se ejecuta una vez). |

## 1. Crear la base de datos (Supabase, gratuito)

1. Crea una cuenta en https://supabase.com y un proyecto nuevo (región Europa).
2. En **SQL Editor → New query**, pega el contenido de `supabase.sql` y pulsa **Run**.
3. En **Authentication → Sign In / Providers**, desactiva *Allow new users to sign up*, para que nadie pueda crearse una cuenta por su cuenta.
4. En **Authentication → Users → Add user**, crea un usuario (correo y contraseña) para cada persona que vaya a usar la web.
5. En **Project Settings → API** copia la **Project URL** y la clave **anon public**.

## 2. Configurar y publicar en GitHub Pages

1. Abre `config.js` y pega la URL y la clave en `supabaseUrl` y `supabaseKey`.
2. Crea un repositorio en GitHub y sube los cuatro archivos (*Add file → Upload files*).
3. En **Settings → Pages**: *Deploy from a branch*, rama `main`, carpeta `/ (root)`.
4. La web estará en `https://TU-USUARIO.github.io/NOMBRE-DEL-REPO/`.

## 3. Primer uso

1. Abre la web e inicia sesión con uno de los usuarios creados.
2. Como la base de datos está vacía, aparecerá el botón **Hasierako datuak kargatu (data.json)**. Púlsalo una sola vez para cargar el historial.
3. A partir de ahí, todo lo que registre cualquier usuario se guarda en la base de datos y lo ven los demás al momento.

## Qué se guarda

En la base de datos se guardan los recursos, las guardias (planificadas y confirmadas), los incendios, las intervenciones, las reglas y tarifas, y el registro de los certificados y documentos de liquidación emitidos.

## Consultas

- **Desde la web**: pestaña **Kontsultak**, con filtros por retén o uraska, tipo de recurso, guardia, práctica o extinción, rango de fechas y número de incendio. Muestra los totales, un resumen por recurso y exporta a CSV. Los certificados emitidos están en **Likidazioa eta ziurtagiriak → Emandakoak**.
- **Desde Supabase**: en **Table Editor** o **SQL Editor**, usa las vistas `v_zaintzak`, `v_eskuhartzeak`, `v_suteak` y `v_ziurtagiriak`. Por ejemplo:

```sql
select baliabidea, sum(orduak * kideak) as ordu_pertsonak
from v_zaintzak
where hasiera >= '2026-06-01' and hasiera < '2026-07-01' and egoera = 'egiaztatua'
group by baliabidea order by baliabidea;
```

## Copias de seguridad

En **Arauak → Babeskopia** puedes exportar todos los datos a JSON e importarlos de nuevo. Supabase también hace copias diarias del proyecto.

## Sin Supabase

Si dejas `config.js` vacío, la web funciona igual, pero los datos se guardan solo en el navegador de cada dispositivo.

# Ejemplo — input (jarvis-os)

Escenario real de entrada al pack paraguas. El operador lanza Jarvis OS con un input externo ambiguo sobre dónde vive el trabajo.

```
jarvis: llegó un email de un cliente pidiendo definir el alcance del proyecto Atlas
para la próxima fase. No estoy seguro si Atlas ya tiene carpeta o si arranco de cero.
Working dir actual: ~/Cosas con IA (raíz, sin estar dentro de ningún proyecto).
```

## Señales presentes
- Input externo: **email** con intención de **definir alcance**.
- Nombre candidato de proyecto: **Atlas**.
- Working dir: raíz, **fuera** de `02_Proyectos/`.
- Ambigüedad declarada: ¿existe ya `02_Proyectos/atlas/`?

## Lo que se espera del pack
- Aplicar COOL (Clarify → Organize → Optimize → Liberate).
- Correr la cascada de ruteo y resolver el sector (se anticipa **III Core / N2**).
- Si la carpeta no existe → derivar a `project-create`; si existe → derivar a la cadencia/skill del proyecto.
- No producir el documento de alcance aquí: solo enrutar.
- Marcar verification tags de una sola familia.

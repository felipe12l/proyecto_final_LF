# 🧩 Proyecto Final LF 2025-2: Analizador y Validador de JSON Web Tokens (JWT)

## 📘 Descripción General

Este proyecto implementa un **analizador y validador completo para JSON Web Tokens (JWT)**, abarcando todas las fases clásicas de un compilador: **análisis léxico, sintáctico y semántico**, además de las funcionalidades de **codificación, decodificación y verificación criptográfica**.

El objetivo principal es aplicar los conocimientos de **Lenguajes Formales y Autómatas** al diseño e implementación de un sistema capaz de reconocer, validar y generar tokens JWT conforme a las especificaciones estándar.

---

## 🎯 Objetivos

- Definir la **gramática formal** del lenguaje JWT.  
- Implementar un **analizador léxico** que identifique los tokens válidos.  
- Construir un **parser sintáctico** (descendente o ascendente).  
- Desarrollar el **análisis semántico**, validando estructura, tipos y claims.  
- Implementar la **codificación y decodificación** del JWT.  
- Aplicar **conceptos de criptografía** para la verificación de firmas.

---

## ⚙️ Fases del Proyecto

| Fase | Descripción |
|------|--------------|
| **1. Análisis Léxico** | Definición del alfabeto, delimitadores, tokens y estructura JSON del header y payload. |
| **2. Análisis Sintáctico** | Creación de la gramática libre de contexto (GLC) para el JWT. |
| **3. Análisis Semántico** | Validación de campos obligatorios, claims estándar y tipos de datos. |
| **4. Decodificación** | Implementación del decodificador Base64URL y parser JSON. |
| **5. Codificación** | Generación de nuevos tokens a partir de estructuras JSON. |
| **6. Verificación Criptográfica** | Validación de la firma digital del token (HS256 / HS384). |

---

## 🧪 Casos de Prueba

- ✅ Tokens válidos con diferentes algoritmos  
- ⚠️ Tokens expirados o con firma inválida  
- ❌ Tokens malformados o con claims faltantes  
- 🔍 Tokens con tipos de datos incorrectos  

---

## 🛠️ Requerimientos Técnicos

- Decodificar y visualizar la estructura del JWT.  
- Validar la sintaxis y semántica del token.  
- Verificar la integridad mediante la firma criptográfica.  
- Codificar nuevos JWT desde estructuras JSON.  
- Validar expiración y claims temporales.

import random
import math
from collections import defaultdict

class Validador:
    def ejecutar_bootstrap(self, algoritmo, lista_datos, k_iteraciones, n_train, n_test, idx_in, idx_out, k_vecinos=1, usar_manhattan=False):
        
        if not lista_datos:
            return {"error": "No hay datos para procesar."}

        n_total = len(lista_datos)
        indices_totales = range(n_total)
        
        historial_metricas = []
        for i in range(k_iteraciones):
            #obtiene indices de entrenamiento
            indices_train = random.choices(indices_totales, k=n_train)
            
            # Se buscan los q estan fuera de los indices
            set_train_usados = set(indices_train)
            candidatos_test = [idx for idx in indices_totales if idx not in set_train_usados]
            
            # Crearemos la lista de indices de test
            indices_test = []
            # Si es que hay mas candidatos de los q requirio el usuario
            if len(candidatos_test) >= n_test:
                indices_test = random.sample(candidatos_test, n_test)
            else:
                # Si no alcanzan usamos los que queden
                indices_test = candidatos_test
            # Y si de plano no hay pasamos a la siguiente iteracion
            if not indices_test:
                continue

            # Se construyen los sets de entrenamiento
            set_entrenamiento = [lista_datos[idx] for idx in indices_train]
            set_prueba = [lista_datos[idx] for idx in indices_test]

            # Se entrena con el conjutno de entrenamiento
            algoritmo.entrenar(set_entrenamiento, idx_in, idx_out)

            # PASO D: Probar y Desglosar por Clase (Punto 4)
            aciertos_globales = 0
            
            # Diccionario para contar: {'Manzana': {'ok': 5, 'total': 10}, ...}
            conteo_clases = defaultdict(lambda: {'ok': 0, 'total': 0})
            
            for patron in set_prueba:
                # 1. Preparar datos
                vector_in = [patron.valores[j] for j in idx_in]
                
                # Obtener clase real limpia (string)
                clase_real_raw = [patron.valores[j] for j in idx_out]
                clase_real = str(clase_real_raw[0]) if len(clase_real_raw) == 1 else str(clase_real_raw)
                
                # 2. Predecir
                prediccion = ""
                if hasattr(algoritmo, 'base_conocimiento'): # Es KNN
                    res = algoritmo.clasificar(vector_in, k=k_vecinos, usar_manhattan=usar_manhattan)
                    prediccion = str(res[0]) if isinstance(res, list) else str(res)
                else: # Es Mínima Distancia
                    res = algoritmo.clasificar(vector_in, usar_manhattan=usar_manhattan)
                    prediccion = str(res)
                
                # 3. Evaluar
                es_acierto = (prediccion == clase_real)
                
                # Contar Global
                if es_acierto:
                    aciertos_globales += 1
                
                # Contar por Clase (Punto 4)
                conteo_clases[clase_real]['total'] += 1
                if es_acierto:
                    conteo_clases[clase_real]['ok'] += 1

            # --- FIN DE PRUEBAS DE ESTA ITERACIÓN ---
            
            # Calcular porcentajes de ESTA vuelta
            eficiencia_iteracion = (aciertos_globales / len(set_prueba)) * 100
            
            # Calcular eficiencia por clase de ESTA vuelta
            dict_eficiencias_clase = {}
            for clase, valores in conteo_clases.items():
                if valores['total'] > 0:
                    pct = (valores['ok'] / valores['total']) * 100
                else:
                    pct = 0.0
                dict_eficiencias_clase[clase] = pct
            
            # Guardamos todo en el historial
            historial_metricas.append({
                'eficiencia': eficiencia_iteracion,
                'por_clase': dict_eficiencias_clase
            })

        # --- FIN DEL CICLO (K VECES) ---
        
        if not historial_metricas:
            return {"error": "Error: No se pudieron generar conjuntos de prueba válidos."}

        # PASO E: Calcular Estadísticas Finales (Punto 5)
        
        # 1. Promedio General
        suma_eficiencias = sum(h['eficiencia'] for h in historial_metricas)
        promedio_general = suma_eficiencias / len(historial_metricas)
        error_general = 100 - promedio_general
        
        # 2. Desviación Estándar (Fórmula Matemática)
        suma_diff_cuadrada = sum((h['eficiencia'] - promedio_general) ** 2 for h in historial_metricas)
        
        if len(historial_metricas) > 1:
            desviacion = math.sqrt(suma_diff_cuadrada / (len(historial_metricas) - 1))
        else:
            desviacion = 0.0

        # 3. Promedios por Clase (Consolidar los K experimentos)
        # Primero buscamos todas las clases que existieron
        todas_las_clases = set()
        for h in historial_metricas:
            todas_las_clases.update(h['por_clase'].keys())
            
        reporte_clases = {}
        for clase in todas_las_clases:
            # Recolectamos la eficiencia de esa clase en cada experimento donde apareció
            vals = [h['por_clase'][clase] for h in historial_metricas if clase in h['por_clase']]
            if vals:
                prom = sum(vals) / len(vals)
                reporte_clases[clase] = round(prom, 2)
            else:
                reporte_clases[clase] = 0.0

        return {
            "promedio_eficiencia": round(promedio_general, 2),
            "promedio_error": round(error_general, 2),
            "desviacion_estandar": round(desviacion, 2),
            "detalles_clase": reporte_clases, # Diccionario {'A': 90%, 'B': 50%}
            "k_reales": len(historial_metricas)
        }
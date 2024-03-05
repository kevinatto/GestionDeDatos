from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
import pandas as pd
from datetime import datetime

pd.options.mode.copy_on_write = True

# Create your views here.
# @login_required
def proceso(request):
    return render(request, "diners/proceso.html")


def carga(request):
    if request.method == "POST":
        archivos = request.FILES
        df_unificado = pd.read_excel(archivos["base_unificado"], sheet_name=0)
        df_excluido_sistema = pd.read_excel(archivos["base_excluido"], sheet_name = "CANCELADOS SISTEMA")
        df_excluido_queja = pd.read_excel(archivos["base_excluido"], sheet_name = "CANCELADOS QUEJAS")
        df_excluido_evicertia = pd.read_excel(archivos["base_excluido"], sheet_name = "EVICERTIA")

        json_unificado = df_unificado.head(20).to_json(orient='records')
        json_excluido_sistema = df_excluido_sistema.head(20).to_json(orient='records')
        json_excluido_queja = df_excluido_queja.head(20).to_json(orient='records')
        json_excluido_evicertia = df_excluido_evicertia.head(20).to_json(orient='records')

        html = """
            <!-- Custom tabs (Charts with tabs)-->
                <div class="card">
                    <div class="card-header">
                        <h3 class="card-title">
                            <i class="fas fa-table mr-1"></i>
                            Vista Previa
                        </h3>
                        <div class="card-tools">
                            <ul class="nav nav-pills ml-auto">
                                <li class="nav-item">
                                    <a class="nav-link active" href="#baseunificada" data-toggle="tab">Base Unificada</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#baseexcluidos1" data-toggle="tab">Base Excluidos | Sistema</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#baseexcluidos2" data-toggle="tab">Base Excluidos | Quejas</a>
                                </li>
                                <li class="nav-item">
                                    <a class="nav-link" href="#baseexcluidos3" data-toggle="tab">Base Excluidos | Evicertia</a>
                                </li>
                            </ul>
                        </div>
                    </div><!-- /.card-header -->
                    <div class="card-body">
                        <div class="tab-content p-0">
                            <!-- Morris chart - Sales -->
                            <div class="chart tab-pane active" id="baseunificada">
                                <table id="baseunificada_vp" class="table table-bordered table-hover" style="overflow-x:scroll;white-space:nowrap;">                                
                                </table>
                            </div>
                            <div class="chart tab-pane" id="baseexcluidos1">
                                <table id="baseexcluidos1_vp" class="table table-bordered table-hover" style="overflow-x:scroll;white-space:nowrap;">                              
                                </table>
                            </div>
                            <div class="chart tab-pane" id="baseexcluidos2">
                                <table id="baseexcluidos2_vp" class="table table-bordered table-hover" style="overflow-x:scroll;white-space:nowrap;">                              
                                </table>
                            </div>
                            <div class="chart tab-pane" id="baseexcluidos3">
                                <table id="baseexcluidos3_vp" class="table table-bordered table-hover" style="overflow-x:scroll;white-space:nowrap;">                              
                                </table>
                            </div>
                        </div>
                    </div><!-- /.card-body -->
                </div>
            <!-- /.card -->
        """

        return JsonResponse({
            "status": "Success", 
            "json_unificado": json_unificado, 
            "json_excluido_sistema": json_excluido_sistema, 
            "json_excluido_queja": json_excluido_queja, 
            "json_excluido_evicertia": json_excluido_evicertia, 
            "html": html
        })
    return JsonResponse({"status": "Invalid request"}, status=400)

def procesa(request):
    if request.method == "POST":
        archivos = request.FILES
        resultados = calculo_diners(archivos)
        
        html = """
            <table id="entregable" class="table table-bordered table-hover">
                    <thead>
                        <tr>
                            <th>Productos</th>
                            <th>Marcas</th>
                            <th>Pólizas</th>
                            <th>Entregables</th>
                            <th>Acción</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>Desgravamen Saldos, Plan Deuda Asegurada y Plan Deuda Asegurada Plus</td>
                            <td>Diners, Mastercard, Visa y Discover</td>
                            <td>5754, 7279, 5756, 5755, 6849, 7280, 6850, 6848, 7506, 7509, 7508 y 7507</td>
                            <td>Bases de Emisión</td>
                            <td style="text-align: center;"><i class="fas fa-download" aria-hidden="true"></i><a href="">Descargar</a></td>
                        </tr>
                        <tr>
                            <td>Desgravamen Saldos, Plan Deuda Asegurada y Plan Deuda Asegurada Plus</td>
                            <td>Diners, Mastercard, Visa y Discover</td>
                            <td>5754, 7279, 5756, 5755, 6849, 7280, 6850, 6848, 7506, 7509, 7508 y 7507</td>
                            <td>Bases de Control</td>
                            <td style="text-align: center;"><i class="fas fa-download" aria-hidden="true"></i><a href="">Descargar</a></td>
                        </tr>
                    </tbody>
            </table>
        """

        return JsonResponse({
            "status": "Success",
            "html": html
        })
    return JsonResponse({"status": "Invalid request"}, status=400)

def historico(request):
    return render(request, "diners/historico.html")

def calculo_diners(archivos):
    base = pd.read_excel(archivos["base_unificado"], sheet_name=0)
    base2_1 = pd.read_excel(archivos["base_excluido"], sheet_name = "CANCELADOS SISTEMA")
    base2_2 = pd.read_excel(archivos["base_excluido"], sheet_name = "CANCELADOS QUEJAS")
    base2_3 = pd.read_excel(archivos["base_excluido"], sheet_name = "EVICERTIA")
    config = pd.read_excel(settings.MEDIA_ROOT + "/config.xlsx", sheet_name=0)
    
    datos_df = base.rename(str.upper, axis='columns')
    datos2_1_df = base2_1.rename(str.upper, axis='columns')
    datos2_2_df = base2_2.rename(str.upper, axis='columns')
    datos2_3_df = base2_3.rename(str.upper, axis='columns')
    config_df = config

    def convert_to_int(value):
        try:
            return f"{int(value):010d}" 
        except (ValueError, TypeError):
            return value

    datos_df['CEDULA_SOCIO'] = datos_df['CEDULA_SOCIO'].apply(convert_to_int)
    datos2_1_df['CEDULA'] = datos2_1_df['CEDULA1'].apply(convert_to_int)
    datos2_2_df['CEDULA'] = datos2_2_df['CEDULA'].apply(convert_to_int)
    datos2_3_df['CEDULA'] = datos2_3_df['CEDULA'].apply(convert_to_int)
    
    # Se separa la base y configuracion por producto
    datos_sss = datos_df[datos_df['BASE'] == "SSS"]
    datos_sda = datos_df[datos_df['BASE'] == "SDA"]
    datos_pda = datos_df[datos_df['BASE'] == "PDA"]

    config_sss = config_df[config_df['PRODUCTO'] == "SSS"]
    config_sda = config_df[config_df['PRODUCTO'] == "SDA"]
    config_pda = config_df[config_df['PRODUCTO'] == "PDA"]
    
    # Se valida los valores netos por marca y producto
    datos_sss.loc[:, 'NETO_DC'] = round(datos_sss['TOTAL_FACTURADO_DC'] + datos_sss['DIF_X_FACTURAR_DC'], 2)
    datos_sss.loc[:, 'NETO_DI'] = round(datos_sss['TOTAL_FACTURADO_DI'] + datos_sss['DIF_X_FACTURAR_DI'], 2)
    datos_sss.loc[:, 'NETO_MC'] = round(datos_sss['TOTAL_FACTURADO_MC'] + datos_sss['DIF_X_FACTURAR_MC'], 2)
    datos_sss.loc[:, 'NETO_VS'] = round(datos_sss['TOTAL_FACTURADO_VS'] + datos_sss['DIF_X_FACTURAR_VS'], 2)

    datos_sda.loc[:, 'NETO_DC'] = round(datos_sda['TOTAL_FACTURADO_DC'] + datos_sda['DIF_X_FACTURAR_DC'], 2)
    datos_sda.loc[:, 'NETO_DI'] = round(datos_sda['TOTAL_FACTURADO_DI'] + datos_sda['DIF_X_FACTURAR_DI'], 2)
    datos_sda.loc[:, 'NETO_MC'] = round(datos_sda['TOTAL_FACTURADO_MC'] + datos_sda['DIF_X_FACTURAR_MC'], 2)
    datos_sda.loc[:, 'NETO_VS'] = round(datos_sda['TOTAL_FACTURADO_VS'] + datos_sda['DIF_X_FACTURAR_VS'], 2)

    datos_pda.loc[:, 'NETO_DC'] = round(datos_pda['TOTAL_FACTURADO_DC'] + datos_pda['DIF_X_FACTURAR_DC'], 2)
    datos_pda.loc[:, 'NETO_DI'] = round(datos_pda['TOTAL_FACTURADO_DI'] + datos_pda['DIF_X_FACTURAR_DI'], 2)
    datos_pda.loc[:, 'NETO_MC'] = round(datos_pda['TOTAL_FACTURADO_MC'] + datos_pda['DIF_X_FACTURAR_MC'], 2)
    datos_pda.loc[:, 'NETO_VS'] = round(datos_pda['TOTAL_FACTURADO_VS'] + datos_pda['DIF_X_FACTURAR_VS'], 2)
    
    # Se pasa a 0 cuando los valores netos son negativos
    datos_sss.loc[datos_sss['NETO_DC'] < 0, ['TOTAL_FACTURADO_DC', 'DIF_X_FACTURAR_DC', 'TOTAL_FACTURADO_DI', 'DIF_X_FACTURAR_DI', 'TOTAL_FACTURADO_MC', 'DIF_X_FACTURAR_MC', 'TOTAL_FACTURADO_VS', 'DIF_X_FACTURAR_VS']] = 0
    datos_sda.loc[datos_sda['NETO_DC'] < 0, ['TOTAL_FACTURADO_DC', 'DIF_X_FACTURAR_DC', 'TOTAL_FACTURADO_DI', 'DIF_X_FACTURAR_DI', 'TOTAL_FACTURADO_MC', 'DIF_X_FACTURAR_MC', 'TOTAL_FACTURADO_VS', 'DIF_X_FACTURAR_VS']] = 0
    datos_pda.loc[datos_pda['NETO_DC'] < 0, ['TOTAL_FACTURADO_DC', 'DIF_X_FACTURAR_DC', 'TOTAL_FACTURADO_DI', 'DIF_X_FACTURAR_DI', 'TOTAL_FACTURADO_MC', 'DIF_X_FACTURAR_MC', 'TOTAL_FACTURADO_VS', 'DIF_X_FACTURAR_VS']] = 0
    
    # Se vuelve a colocar los valores netos por marca y producto
    datos_sss.loc[:, 'NETO_DC'] = round(datos_sss['TOTAL_FACTURADO_DC'] + datos_sss['DIF_X_FACTURAR_DC'], 2)
    datos_sss.loc[:, 'NETO_DI'] = round(datos_sss['TOTAL_FACTURADO_DI'] + datos_sss['DIF_X_FACTURAR_DI'], 2)
    datos_sss.loc[:, 'NETO_MC'] = round(datos_sss['TOTAL_FACTURADO_MC'] + datos_sss['DIF_X_FACTURAR_MC'], 2)
    datos_sss.loc[:, 'NETO_VS'] = round(datos_sss['TOTAL_FACTURADO_VS'] + datos_sss['DIF_X_FACTURAR_VS'], 2)

    datos_sda.loc[:, 'NETO_DC'] = round(datos_sda['TOTAL_FACTURADO_DC'] + datos_sda['DIF_X_FACTURAR_DC'], 2)
    datos_sda.loc[:, 'NETO_DI'] = round(datos_sda['TOTAL_FACTURADO_DI'] + datos_sda['DIF_X_FACTURAR_DI'], 2)
    datos_sda.loc[:, 'NETO_MC'] = round(datos_sda['TOTAL_FACTURADO_MC'] + datos_sda['DIF_X_FACTURAR_MC'], 2)
    datos_sda.loc[:, 'NETO_VS'] = round(datos_sda['TOTAL_FACTURADO_VS'] + datos_sda['DIF_X_FACTURAR_VS'], 2)

    datos_pda.loc[:, 'NETO_DC'] = round(datos_pda['TOTAL_FACTURADO_DC'] + datos_pda['DIF_X_FACTURAR_DC'], 2)
    datos_pda.loc[:, 'NETO_DI'] = round(datos_pda['TOTAL_FACTURADO_DI'] + datos_pda['DIF_X_FACTURAR_DI'], 2)
    datos_pda.loc[:, 'NETO_MC'] = round(datos_pda['TOTAL_FACTURADO_MC'] + datos_pda['DIF_X_FACTURAR_MC'], 2)
    datos_pda.loc[:, 'NETO_VS'] = round(datos_pda['TOTAL_FACTURADO_VS'] + datos_pda['DIF_X_FACTURAR_VS'], 2)
    
    # Creación de Suma Asegurada, Prima Neta y Prima Total
    datos_sss.loc[:, 'SUMA_ASEGURADA'] = round(datos_sss[['NETO_DC', 'NETO_DI', 'NETO_MC', 'NETO_VS']].sum(axis=1), 2)
    datos_sda.loc[:, 'SUMA_ASEGURADA'] = round(datos_sda[['NETO_DC', 'NETO_DI', 'NETO_MC', 'NETO_VS']].sum(axis=1), 2)
    datos_pda.loc[:, 'SUMA_ASEGURADA'] = round(datos_pda[['NETO_DC', 'NETO_DI', 'NETO_MC', 'NETO_VS']].sum(axis=1), 2)

    datos_sss.loc[:, 'PRIMA_NETA'] = round(datos_sss['SUMA_ASEGURADA'] * config_sss['TASA_PN'][0], 2)
    datos_sda.loc[:, 'PRIMA_NETA'] = round(datos_sda['SUMA_ASEGURADA'] * config_sda['TASA_PN'][1], 2)
    datos_pda.loc[:, 'PRIMA_NETA'] = round(datos_pda['SUMA_ASEGURADA'] * config_pda['TASA_PN'][2], 2)

    datos_sss.loc[:, 'PRIMA_TOTAL'] = round(datos_sss['SUMA_ASEGURADA'] * config_sss['TASA_PT'][0], 2)
    datos_sda.loc[:, 'PRIMA_TOTAL'] = round(datos_sda['SUMA_ASEGURADA'] * config_sda['TASA_PT'][1], 2)
    datos_pda.loc[:, 'PRIMA_TOTAL'] = round(datos_pda['SUMA_ASEGURADA'] * config_pda['TASA_PT'][2], 2)
    
    # Aplicacion de limites y techos en sumas aseguradas y primas
    datos_sss.loc[datos_sss['SUMA_ASEGURADA'] >= config_sss['LIMITE_TA'][0], 'PRIMA_NETA'] = config_sss['LIMITE_S_PN'][0]
    datos_sda.loc[datos_sda['SUMA_ASEGURADA'] >= config_sda['LIMITE_TA'][1], 'PRIMA_NETA'] = config_sda['LIMITE_S_PN'][1]
    datos_pda.loc[datos_pda['SUMA_ASEGURADA'] >= config_pda['LIMITE_TA'][2], 'PRIMA_NETA'] = config_pda['LIMITE_S_PN'][2]

    datos_sss.loc[datos_sss['SUMA_ASEGURADA'] >= config_sss['LIMITE_TA'][0], 'PRIMA_TOTAL'] = config_sss['LIMITE_S_PT'][0]
    datos_sda.loc[datos_sda['SUMA_ASEGURADA'] >= config_sda['LIMITE_TA'][1], 'PRIMA_TOTAL'] = config_sda['LIMITE_S_PT'][1]
    datos_pda.loc[datos_pda['SUMA_ASEGURADA'] >= config_pda['LIMITE_TA'][2], 'PRIMA_TOTAL'] = config_pda['LIMITE_S_PT'][2]

    datos_sss.loc[datos_sss['SUMA_ASEGURADA'] > config_sss['LIMITE_S_SA'][0], 'SUMA_ASEGURADA'] = config_sss['LIMITE_S_SA'][0]
    datos_sda.loc[datos_sda['SUMA_ASEGURADA'] > config_sda['LIMITE_S_SA'][1], 'SUMA_ASEGURADA'] = config_sda['LIMITE_S_SA'][1]
    datos_pda.loc[datos_pda['SUMA_ASEGURADA'] > config_pda['LIMITE_S_SA'][2], 'SUMA_ASEGURADA'] = config_pda['LIMITE_S_SA'][2]

    datos_sda.loc[(datos_sda['SUMA_ASEGURADA'] > 0) & (datos_sda['SUMA_ASEGURADA'] <= config_sda['LIMITE_I_SA'][1]), 'PRIMA_NETA'] = config_sda['LIMITE_I_PN'][1]
    datos_pda.loc[(datos_pda['SUMA_ASEGURADA'] > 0) & (datos_pda['SUMA_ASEGURADA'] <= config_pda['LIMITE_I_SA'][2]), 'PRIMA_NETA'] = config_pda['LIMITE_I_PN'][2]

    datos_sda.loc[(datos_sda['SUMA_ASEGURADA'] > 0) & (datos_sda['SUMA_ASEGURADA'] <= config_sda['LIMITE_I_SA'][1]), 'PRIMA_TOTAL'] = config_sda['LIMITE_I_PT'][1]
    datos_pda.loc[(datos_pda['SUMA_ASEGURADA'] > 0) & (datos_pda['SUMA_ASEGURADA'] <= config_pda['LIMITE_I_SA'][2]), 'PRIMA_TOTAL'] = config_pda['LIMITE_I_PT'][2]
    
    # Se quitan los registros con prima en cero
    datos_sss_cero = datos_sss[datos_sss['PRIMA_NETA'] == 0]
    datos_sss_sincero = datos_sss[datos_sss['PRIMA_NETA'] != 0]

    datos_sda_cero = datos_sda[datos_sda['PRIMA_NETA'] == 0]
    datos_sda_sincero = datos_sda[datos_sda['PRIMA_NETA'] != 0]

    datos_pda_cero = datos_pda[datos_pda['PRIMA_NETA'] == 0]
    datos_pda_sincero = datos_pda[datos_pda['PRIMA_NETA'] != 0]
    
    # Se quitan los registros duplicados de cada base
    clientes_sss = datos_sss_sincero.groupby('CEDULA_SOCIO').size().reset_index(name='NUM_TARJETAS')
    clientes_sda = datos_sda_sincero.groupby('CEDULA_SOCIO').size().reset_index(name='NUM_TARJETAS')
    clientes_pda = datos_pda_sincero.groupby('CEDULA_SOCIO').size().reset_index(name='NUM_TARJETAS')

    def determine_priority(row):
        if row['NETO_DC'] == row['VALOR_MAXIMO']:
            return 'DN'
        elif row['NETO_VS'] == row['VALOR_MAXIMO']:
            return 'VI'
        elif row['NETO_MC'] == row['VALOR_MAXIMO']:
            return 'MC'
        elif row['NETO_DI'] == row['VALOR_MAXIMO']:
            return 'DI'

    # Calcular VALOR_MAXIMO
    datos_sss_sincero.loc[:, 'VALOR_MAXIMO'] = datos_sss_sincero[['NETO_DC', 'NETO_VS', 'NETO_MC', 'NETO_DI']].max(axis=1)
    datos_sss_sincero.loc[:, 'PRIORIDAD'] = None
    datos_sda_sincero.loc[:, 'VALOR_MAXIMO'] = datos_sda_sincero[['NETO_DC', 'NETO_VS', 'NETO_MC', 'NETO_DI']].max(axis=1)
    datos_sda_sincero.loc[:, 'PRIORIDAD'] = None
    datos_pda_sincero.loc[:, 'VALOR_MAXIMO'] = datos_pda_sincero[['NETO_DC', 'NETO_VS', 'NETO_MC', 'NETO_DI']].max(axis=1)
    datos_pda_sincero.loc[:, 'PRIORIDAD'] = None

    # Asignar PRIORIDAD
    datos_sss_sincero.loc[:, 'PRIORIDAD'] = datos_sss_sincero.apply(determine_priority, axis=1)
    datos_sda_sincero.loc[:, 'PRIORIDAD'] = datos_sda_sincero.apply(determine_priority, axis=1)
    datos_pda_sincero.loc[:, 'PRIORIDAD'] = datos_pda_sincero.apply(determine_priority, axis=1)
    
    # Filtrar registros con cobro cero
    cobro_cero_sss = datos_sss_sincero[datos_sss_sincero['CEDULA_SOCIO'].isna()]
    cobro_cero_sda = datos_sda_sincero[datos_sda_sincero['CEDULA_SOCIO'].isna()]
    cobro_cero_pda = datos_pda_sincero[datos_pda_sincero['CEDULA_SOCIO'].isna()]
    
    # Filtrar registros sin duplicados y con la misma prioridad
    datos_sss_sin_duplicados = datos_sss_sincero[datos_sss_sincero['D8FAXT'] == datos_sss_sincero['PRIORIDAD']]
    datos_sss_duplicados = datos_sss_sincero[datos_sss_sincero['D8FAXT'] != datos_sss_sincero['PRIORIDAD']]
    datos_sss_duplicados.loc[:, 'D8FAXT'] = pd.Categorical(datos_sss_duplicados['D8FAXT'], categories=["DN", "VI", "MC", "DI"], ordered=True)
    datos_sss_duplicados = datos_sss_duplicados.sort_values('D8FAXT')

    for index, row in datos_sss_duplicados.iterrows():
        if row['CEDULA_SOCIO'] not in datos_sss_sin_duplicados['CEDULA_SOCIO'].values:
            if row['D8FAXT'] == 'DN' and row['NETO_DC'] > 0:
                datos_sss_sin_duplicados = pd.concat([datos_sss_sin_duplicados, pd.DataFrame([row])], ignore_index=True)
            elif row['D8FAXT'] == 'VI' and row['NETO_VS'] > 0:
                datos_sss_sin_duplicados = pd.concat([datos_sss_sin_duplicados, pd.DataFrame([row])], ignore_index=True)
            elif row['D8FAXT'] == 'MC' and row['NETO_MC'] > 0:
                datos_sss_sin_duplicados = pd.concat([datos_sss_sin_duplicados, pd.DataFrame([row])], ignore_index=True)
            elif row['D8FAXT'] == 'DI' and row['NETO_DI'] > 0:
                datos_sss_sin_duplicados = pd.concat([datos_sss_sin_duplicados, pd.DataFrame([row])], ignore_index=True)
            else:
                cobro_cero_sss = pd.concat([cobro_cero_sss, pd.DataFrame([row])], ignore_index=True)

    datos_sss_sin_duplicados = datos_sss_sin_duplicados.drop_duplicates(subset='CEDULA_SOCIO', keep='first')

    datos_sda_sin_duplicados = datos_sda_sincero[datos_sda_sincero['D8FAXT'] == datos_sda_sincero['PRIORIDAD']]
    datos_sda_duplicados = datos_sda_sincero[datos_sda_sincero['D8FAXT'] != datos_sda_sincero['PRIORIDAD']]
    datos_sda_duplicados.loc[:, 'D8FAXT'] = pd.Categorical(datos_sda_duplicados['D8FAXT'], categories=["DN", "VI", "MC", "DI"], ordered=True)
    datos_sda_duplicados = datos_sda_duplicados.sort_values('D8FAXT')

    for index, row in datos_sda_duplicados.iterrows():
        if row['CEDULA_SOCIO'] not in datos_sda_sin_duplicados['CEDULA_SOCIO'].values:
            if row['D8FAXT'] == 'DN' and row['NETO_DC'] > 0:
                datos_sda_sin_duplicados = pd.concat([datos_sda_sin_duplicados, pd.DataFrame([row])], ignore_index=True)
            elif row['D8FAXT'] == 'VI' and row['NETO_VS'] > 0:
                datos_sda_sin_duplicados = pd.concat([datos_sda_sin_duplicados, pd.DataFrame([row])], ignore_index=True)
            elif row['D8FAXT'] == 'MC' and row['NETO_MC'] > 0:
                datos_sda_sin_duplicados = pd.concat([datos_sda_sin_duplicados, pd.DataFrame([row])], ignore_index=True)
            elif row['D8FAXT'] == 'DI' and row['NETO_DI'] > 0:
                datos_sda_sin_duplicados = pd.concat([datos_sda_sin_duplicados, pd.DataFrame([row])], ignore_index=True)
            else:
                cobro_cero_sda = pd.concat([cobro_cero_sda, pd.DataFrame([row])], ignore_index=True)

    datos_sda_sin_duplicados = datos_sda_sin_duplicados.drop_duplicates(subset='CEDULA_SOCIO', keep='first')

    datos_pda_sin_duplicados = datos_pda_sincero[datos_pda_sincero['D8FAXT'] == datos_pda_sincero['PRIORIDAD']]
    datos_pda_duplicados = datos_pda_sincero[datos_pda_sincero['D8FAXT'] != datos_pda_sincero['PRIORIDAD']]
    datos_pda_duplicados.loc[:, 'D8FAXT'] = pd.Categorical(datos_pda_duplicados['D8FAXT'], categories=["DN", "VI", "MC", "DI"], ordered=True)
    datos_pda_duplicados = datos_pda_duplicados.sort_values('D8FAXT')

    for index, row in datos_pda_duplicados.iterrows():
        if row['CEDULA_SOCIO'] not in datos_pda_sin_duplicados['CEDULA_SOCIO'].values:
            if row['D8FAXT'] == 'DN' and row['NETO_DC'] > 0:
                datos_pda_sin_duplicados = pd.concat([datos_pda_sin_duplicados, pd.DataFrame([row])], ignore_index=True)
            elif row['D8FAXT'] == 'VI' and row['NETO_VS'] > 0:
                datos_pda_sin_duplicados = pd.concat([datos_pda_sin_duplicados, pd.DataFrame([row])], ignore_index=True)
            elif row['D8FAXT'] == 'MC' and row['NETO_MC'] > 0:
                datos_pda_sin_duplicados = pd.concat([datos_pda_sin_duplicados, pd.DataFrame([row])], ignore_index=True)
            elif row['D8FAXT'] == 'DI' and row['NETO_DI'] > 0:
                datos_pda_sin_duplicados = pd.concat([datos_pda_sin_duplicados, pd.DataFrame([row])], ignore_index=True)
            else:
                cobro_cero_pda = pd.concat([cobro_cero_pda, pd.DataFrame([row])], ignore_index=True)

    datos_pda_sin_duplicados = datos_pda_sin_duplicados.drop_duplicates(subset='CEDULA_SOCIO', keep='first')
    
    # Se excluyen los clientes en base a los cancelados, quejas y evicertia
    bd_cancelados_sss = datos2_1_df[(datos2_1_df['POLIZA'].isin([5754, 7279, 5756, 5755]))]
    bd_cancelados_sda = datos2_1_df[(datos2_1_df['POLIZA'].isin([6849, 7280, 6850, 6848]))]
    bd_cancelados_pda = datos2_1_df[(datos2_1_df['POLIZA'].isin([7506, 7509, 7508, 7507]))]

    cancelados_sss = datos_sss_sin_duplicados[datos_sss_sin_duplicados['CEDULA_SOCIO'].isin(bd_cancelados_sss['CEDULA'])]
    datos_sss_final = datos_sss_sin_duplicados[~datos_sss_sin_duplicados['CEDULA_SOCIO'].isin(bd_cancelados_sss['CEDULA'])]
    cancelados_sda = datos_sda_sin_duplicados[datos_sda_sin_duplicados['CEDULA_SOCIO'].isin(bd_cancelados_sda['CEDULA'])]
    datos_sda_final = datos_sda_sin_duplicados[~datos_sda_sin_duplicados['CEDULA_SOCIO'].isin(bd_cancelados_sda['CEDULA'])]
    cancelados_pda = datos_pda_sin_duplicados[datos_pda_sin_duplicados['CEDULA_SOCIO'].isin(bd_cancelados_pda['CEDULA'])]
    datos_pda_final = datos_pda_sin_duplicados[~datos_pda_sin_duplicados['CEDULA_SOCIO'].isin(bd_cancelados_pda['CEDULA'])]

    bd_quejas_sss = datos2_2_df[datos2_2_df['PRODUCTO'] == "SSS"]
    bd_quejas_sda = datos2_2_df[datos2_2_df['PRODUCTO'] == "PDA"]
    bd_quejas_pda = datos2_2_df[datos2_2_df['PRODUCTO'] == "PDAP"]

    quejas_sss = datos_sss_final[datos_sss_final['CEDULA_SOCIO'].isin(bd_quejas_sss['CEDULA'])]
    datos_sss_final = datos_sss_final[~datos_sss_final['CEDULA_SOCIO'].isin(bd_quejas_sss['CEDULA'])]
    quejas_sda = datos_sda_final[datos_sda_final['CEDULA_SOCIO'].isin(bd_quejas_sda['CEDULA'])]
    datos_sda_final = datos_sda_final[~datos_sda_final['CEDULA_SOCIO'].isin(bd_quejas_sda['CEDULA'])]
    quejas_pda = datos_pda_final[datos_pda_final['CEDULA_SOCIO'].isin(bd_quejas_pda['CEDULA'])]
    datos_pda_final = datos_pda_final[~datos_pda_final['CEDULA_SOCIO'].isin(bd_quejas_pda['CEDULA'])]

    bd_evicertia_sss = datos2_3_df[datos2_3_df['PRODUCTO'] == "SSS"]
    bd_evicertia_sda = datos2_3_df[datos2_3_df['PRODUCTO'] == "PDA"]
    bd_evicertia_pda = datos2_3_df[datos2_3_df['PRODUCTO'] == "PDAP"]

    evicertia_sss = datos_sss_final[datos_sss_final['CEDULA_SOCIO'].isin(bd_evicertia_sss['CEDULA'])]
    datos_sss_final = datos_sss_final[~datos_sss_final['CEDULA_SOCIO'].isin(bd_evicertia_sss['CEDULA'])]
    evicertia_sda = datos_sda_final[datos_sda_final['CEDULA_SOCIO'].isin(bd_evicertia_sda['CEDULA'])]
    datos_sda_final = datos_sda_final[~datos_sda_final['CEDULA_SOCIO'].isin(bd_evicertia_sda['CEDULA'])]
    evicertia_pda = datos_pda_final[datos_pda_final['CEDULA_SOCIO'].isin(bd_evicertia_pda['CEDULA'])]
    datos_pda_final = datos_pda_final[~datos_pda_final['CEDULA_SOCIO'].isin(bd_evicertia_pda['CEDULA'])]
    
    # Se crean los DataFrames separados por producto y marca
    SSS_DINERS_5754 = datos_sss_final[datos_sss_final['D8FAXT'] == 'DN'].copy()
    SSS_MASTERCARD_7279 = datos_sss_final[datos_sss_final['D8FAXT'] == 'MC'].copy()
    SSS_VISA_5756 = datos_sss_final[datos_sss_final['D8FAXT'] == 'VI'].copy()
    SSS_DISCOVER_5755 = datos_sss_final[datos_sss_final['D8FAXT'] == 'DI'].copy()

    SDA_DINERS_6849 = datos_sda_final[datos_sda_final['D8FAXT'] == 'DN'].copy()
    SDA_MASTERCARD_7280 = datos_sda_final[datos_sda_final['D8FAXT'] == 'MC'].copy()
    SDA_VISA_6850 = datos_sda_final[datos_sda_final['D8FAXT'] == 'VI'].copy()
    SDA_DISCOVER_6848 = datos_sda_final[datos_sda_final['D8FAXT'] == 'DI'].copy()

    PDA_DINERS_7506 = datos_pda_final[datos_pda_final['D8FAXT'] == 'DN'].copy()
    PDA_MASTERCARD_7509 = datos_pda_final[datos_pda_final['D8FAXT'] == 'MC'].copy()
    PDA_VISA_7508 = datos_pda_final[datos_pda_final['D8FAXT'] == 'VI'].copy()
    PDA_DISCOVER_7507 = datos_pda_final[datos_pda_final['D8FAXT'] == 'DI'].copy()
    
    # Se agrega la fecha y hora del proceso para el historico
    fecha_proceso = datetime.now()

    # Base de Emision
    bases_emision = [SSS_DINERS_5754, SSS_MASTERCARD_7279, SSS_VISA_5756, SSS_DISCOVER_5755,
                    SDA_DINERS_6849, SDA_MASTERCARD_7280, SDA_VISA_6850, SDA_DISCOVER_6848,
                    PDA_DINERS_7506, PDA_MASTERCARD_7509, PDA_VISA_7508, PDA_DISCOVER_7507]

    for base in bases_emision:
        if not base.empty:
            base.loc[:, 'PROCESADO_EL'] = fecha_proceso
            
    # Base de Primas Cero
    bases_primascero = [datos_sss_cero, datos_sda_cero, datos_pda_cero]

    for base in bases_primascero:
        if not base.empty:
            base.loc[:, 'PROCESADO_EL'] = fecha_proceso
            
    # Base de Cobros Cero
    cobro_cero_sss_final = cobro_cero_sss[cobro_cero_sss['CEDULA_SOCIO'].isna()]
    cobro_cero_sda_final = cobro_cero_sda[cobro_cero_sda['CEDULA_SOCIO'].isna()]
    cobro_cero_pda_final = cobro_cero_pda[cobro_cero_pda['CEDULA_SOCIO'].isna()]

    if not cobro_cero_sss.empty:
        for i in range(len(cobro_cero_sss)):
            if cobro_cero_sss.iloc[i, :]['CEDULA_SOCIO'] not in datos_sss_final['CEDULA_SOCIO'].values:
                if cobro_cero_sss.iloc[i, :]['D8FAXT'] == "DN" and cobro_cero_sss.iloc[i, :]['NETO_DC'] == 0:
                    cobro_cero_sss_final = pd.concat([cobro_cero_sss_final, cobro_cero_sss.iloc[i, :]], ignore_index=True)
                elif cobro_cero_sss.iloc[i, :]['D8FAXT'] == "VI" and cobro_cero_sss.iloc[i, :]['NETO_VS'] == 0:
                    cobro_cero_sss_final = pd.concat([cobro_cero_sss_final, cobro_cero_sss.iloc[i, :]], ignore_index=True)
                elif cobro_cero_sss.iloc[i, :]['D8FAXT'] == "MC" and cobro_cero_sss.iloc[i, :]['NETO_MC'] == 0:
                    cobro_cero_sss_final = pd.concat([cobro_cero_sss_final, cobro_cero_sss.iloc[i, :]], ignore_index=True)
                elif cobro_cero_sss.iloc[i, :]['D8FAXT'] == "DI" and cobro_cero_sss.iloc[i, :]['NETO_DI'] == 0:
                    cobro_cero_sss_final = pd.concat([cobro_cero_sss_final, cobro_cero_sss.iloc[i, :]], ignore_index=True)

    if not cobro_cero_sss_final.empty:
        cobro_cero_sss_final.loc[:, 'PROCESADO_EL'] = fecha_proceso

    if not cobro_cero_sda.empty:
        for i in range(len(cobro_cero_sda)):
            if cobro_cero_sda.iloc[i, :]['CEDULA_SOCIO'] not in datos_sda_final['CEDULA_SOCIO'].values:
                if cobro_cero_sda.iloc[i, :]['D8FAXT'] == "DN" and cobro_cero_sda.iloc[i, :]['NETO_DC'] == 0:
                    cobro_cero_sda_final = pd.concat([cobro_cero_sda_final, cobro_cero_sda.iloc[i, :]], ignore_index=True)
                elif cobro_cero_sda.iloc[i, :]['D8FAXT'] == "VI" and cobro_cero_sda.iloc[i, :]['NETO_VS'] == 0:
                    cobro_cero_sda_final = pd.concat([cobro_cero_sda_final, cobro_cero_sda.iloc[i, :]], ignore_index=True)
                elif cobro_cero_sda.iloc[i, :]['D8FAXT'] == "MC" and cobro_cero_sda.iloc[i, :]['NETO_MC'] == 0:
                    cobro_cero_sda_final = pd.concat([cobro_cero_sda_final, cobro_cero_sda.iloc[i, :]], ignore_index=True)
                elif cobro_cero_sda.iloc[i, :]['D8FAXT'] == "DI" and cobro_cero_sda.iloc[i, :]['NETO_DI'] == 0:
                    cobro_cero_sda_final = pd.concat([cobro_cero_sda_final, cobro_cero_sda.iloc[i, :]], ignore_index=True)

    if not cobro_cero_sda_final.empty:
        cobro_cero_sda_final.loc[:, 'PROCESADO_EL'] = fecha_proceso

    if not cobro_cero_pda.empty:
        for i in range(len(cobro_cero_pda)):
            if cobro_cero_pda.iloc[i, :]['CEDULA_SOCIO'] not in datos_pda_final['CEDULA_SOCIO'].values:
                if cobro_cero_pda.iloc[i, :]['D8FAXT'] == "DN" and cobro_cero_pda.iloc[i, :]['NETO_DC'] == 0:
                    cobro_cero_pda_final = pd.concat([cobro_cero_pda_final, cobro_cero_pda.iloc[i, :]], ignore_index=True)
                elif cobro_cero_pda.iloc[i, :]['D8FAXT'] == "VI" and cobro_cero_pda.iloc[i, :]['NETO_VS'] == 0:
                    cobro_cero_pda_final = pd.concat([cobro_cero_pda_final, cobro_cero_pda.iloc[i, :]], ignore_index=True)
                elif cobro_cero_pda.iloc[i, :]['D8FAXT'] == "MC" and cobro_cero_pda.iloc[i, :]['NETO_MC'] == 0:
                    cobro_cero_pda_final = pd.concat([cobro_cero_pda_final, cobro_cero_pda.iloc[i, :]], ignore_index=True)
                elif cobro_cero_pda.iloc[i, :]['D8FAXT'] == "DI" and cobro_cero_pda.iloc[i, :]['NETO_DI'] == 0:
                    cobro_cero_pda_final = pd.concat([cobro_cero_pda_final, cobro_cero_pda.iloc[i, :]], ignore_index=True)

    if not cobro_cero_pda_final.empty:
        cobro_cero_pda_final.loc[:, 'PROCESADO_EL'] = fecha_proceso

    if not cobro_cero_sss_final.empty:
        indices_to_remove = []
        for i in range(len(cobro_cero_sss_final)):
            if cobro_cero_sss_final.iloc[i, :]['CEDULA_SOCIO'] in datos_sss_final['CEDULA_SOCIO'].values:
                indices_to_remove.append(i)
            elif cobro_cero_sss_final.iloc[i, :]['CEDULA_SOCIO'] in cancelados_sss['CEDULA_SOCIO'].values:
                indices_to_remove.append(i)
            elif cobro_cero_sss_final.iloc[i, :]['CEDULA_SOCIO'] in quejas_sss['CEDULA_SOCIO'].values:
                indices_to_remove.append(i)
            elif cobro_cero_sss_final.iloc[i, :]['CEDULA_SOCIO'] in evicertia_sss['CEDULA_SOCIO'].values:
                indices_to_remove.append(i)
        cobro_cero_sss_final = cobro_cero_sss_final.drop(indices_to_remove)

    if not cobro_cero_sda_final.empty:
        indices_to_remove = []
        for i in range(len(cobro_cero_sda_final)):
            if cobro_cero_sda_final.iloc[i, :]['CEDULA_SOCIO'] in datos_sda_final['CEDULA_SOCIO'].values:
                indices_to_remove.append(i)
            elif cobro_cero_sda_final.iloc[i, :]['CEDULA_SOCIO'] in cancelados_sda['CEDULA_SOCIO'].values:
                indices_to_remove.append(i)
            elif cobro_cero_sda_final.iloc[i, :]['CEDULA_SOCIO'] in quejas_sda['CEDULA_SOCIO'].values:
                indices_to_remove.append(i)
            elif cobro_cero_sda_final.iloc[i, :]['CEDULA_SOCIO'] in evicertia_sda['CEDULA_SOCIO'].values:
                indices_to_remove.append(i)
        cobro_cero_sda_final = cobro_cero_sda_final.drop(indices_to_remove)

    if not cobro_cero_pda_final.empty:
        indices_to_remove = []
        for i in range(len(cobro_cero_pda_final)):
            if cobro_cero_pda_final.iloc[i, :]['CEDULA_SOCIO'] in datos_pda_final['CEDULA_SOCIO'].values:
                indices_to_remove.append(i)
            elif cobro_cero_pda_final.iloc[i, :]['CEDULA_SOCIO'] in cancelados_pda['CEDULA_SOCIO'].values:
                indices_to_remove.append(i)
            elif cobro_cero_pda_final.iloc[i, :]['CEDULA_SOCIO'] in quejas_pda['CEDULA_SOCIO'].values:
                indices_to_remove.append(i)
            elif cobro_cero_pda_final.iloc[i, :]['CEDULA_SOCIO'] in evicertia_pda['CEDULA_SOCIO'].values:
                indices_to_remove.append(i)
        cobro_cero_pda_final = cobro_cero_pda_final.drop(indices_to_remove)
        
    bases_cobrocero = [cobro_cero_sss_final, cobro_cero_sda_final, cobro_cero_pda_final]
    
    # Base de Excluidos
    bases_excluidos = [cancelados_sss, quejas_sss, evicertia_sss,
                       cancelados_sda, quejas_sda, evicertia_sda,
                       cancelados_pda, quejas_pda, evicertia_pda]

    for base in bases_excluidos:
        if not base.empty:
            base.loc[:, 'PROCESADO_EL'] = fecha_proceso
            
    bases_resultado = [bases_emision, bases_primascero,  bases_cobrocero, bases_excluidos]
            
    return bases_resultado
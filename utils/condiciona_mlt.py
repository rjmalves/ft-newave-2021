import pandas as pd
import numpy as np

from inewave.newave import EafPast
from inewave.newave import Confhd


MLT_2021_REE = {
                "SUDESTE": [10278.76, 10370.89, 9781.91, 7311.49, 4603.59, 3539.94,
                            2912.37, 2460.93, 2442.94, 3129.49, 5014.24, 8233.79],
                "MADEIRA": [8104.98, 10517.57, 12125.31, 11620.15, 8850.95, 6078.95,
                            3865.90, 2395.98, 1798.85, 2134.76, 3365.01, 5462.44],
                "TPIRES": [3271.28, 3809.95, 3960.35, 3179.26, 2054.03, 1355.04,
                           985.84, 776.87, 686.20, 847.17, 1367.87, 2320.10],
                "ITAIPU": [3360.44, 4018.46, 3793.44, 3566.06, 3495.00, 3618.37,
                           3119.56, 2617.68, 2666.77, 3295.64, 3076.48, 3062.69],
                "PARANA": [37228.24, 38234.08, 36129.87, 26690.08, 18611.54, 15453.82,
                           12564.81, 10495.17, 10127.40, 11801.86, 16248.64, 26291.92],
                "PRNPANEMA": [3694.05, 3813.69, 3159.80, 2380.87, 2357.90, 2586.80,
                              2287.59, 1881.04, 2072.90, 2557.78, 2370.97, 2640.47],
                "SUL": [3386.41, 3905.38, 3152.62, 3250.87, 4408.62, 5250.86,
                        5962.02, 5982.82, 6991.91, 7097.22, 4640.71, 3509.05],
                "IGUACU": [4191.86, 4448.64, 3940.66, 3342.48, 4164.95, 5186.68,
                           5020.20, 4096.86, 4805.36, 6344.45, 4784.93, 3944.37],
                "NORDESTE": [13660.20, 14372.20, 14224.00, 11604.25, 7021.04, 4639.29,
                             3827.41, 3338.15, 2984.78, 3257.82, 5297.44, 9873.41],
                "NORTE": [9549.13, 12861.12, 14873.94, 14568.11, 9302.27, 4430.02,
                          2603.13, 1847.60, 1486.73, 1706.65, 2845.87, 5552.80],
                "BMONTE": [5643.96, 9052.94, 10609.23, 10855.65, 9370.99, 4796.32,
                           1622.73, 674.55, 378.98, 431.91, 972.25, 2478.90],
                "MAN-AP": [501.45, 867.17, 1231.38, 1571.12, 1745.64, 1478.67,
                           1061.03, 701.44, 430.47, 270.83, 210.55, 263.53]
               }


def condiciona_ena_mlt(df_entrada: pd.DataFrame,
                       p: float) -> pd.DataFrame:
    df = df_entrada.copy(deep=True)
    colunas_meses = df.columns[2:]
    rees = list(MLT_2021_REE.keys())
    for ree in rees:
        df.loc[df["REE"] == ree,
               colunas_meses] = p * np.array(MLT_2021_REE[ree])
    return df


def condiciona_earm_earmax(df_entrada: pd.DataFrame,
                           p: float) -> pd.DataFrame:
    df = df_entrada.copy(deep=True)
    df.loc[df["Volume Inicial"] != 0, "Volume Inicial"] = p
    return df


DIRETORIO = "C:\\Users\\roger\\Operador Nacional do Sistema Eletrico\\ONS\\NEWAVE\\CPAMP\\condicionado"
VALORES_ENA = [0.5, 1.0, 1.5, 2.0]
VALORES_EARM = [40.0, 60.0, 80.0]

e = EafPast.le_arquivo(DIRETORIO)
t_original = e.tendencia
for ena in VALORES_ENA:
    e.tendencia = condiciona_ena_mlt(t_original, ena)
    e.escreve_arquivo(DIRETORIO, f"eafpast_ena{ena}.dat")

c = Confhd.le_arquivo(DIRETORIO)
a_original = c.usinas
for earm in VALORES_EARM:
    c.usinas = condiciona_earm_earmax(a_original, earm)
    c.escreve_arquivo(DIRETORIO, f"confhd_earm{earm}.dat")

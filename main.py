
import pandas as pd
import matplotlib.pyplot as plt
from twilio.rest import Client
from dotenv import load_dotenv # type: ignore
import os

# === CARGAR VARIABLES DE ENTORNO ===
load_dotenv()

account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_to = os.getenv("TWILIO_TO")

# === CARGAR DATOS DE EXCEL ===
df = pd.read_excel("Ventas - Fundamentos.xlsx", sheet_name="VENTAS", engine="openpyxl")

# === ANÁLISIS FINANCIERO ===
total_ventas = df["Precio Venta Real"].sum()
ganancia_total = (df["Precio Venta Real"] - df["Costo Vehículo"]).sum()
ventas_por_sede = df.groupby("Sede")["Precio Venta Real"].sum()
top_vendedores = df["Vendedor"].value_counts().head(5)

# === REPORTE EN TEXTO ===
reporte = f"""
📊 *Resumen de Ventas* 📊

✅ Total de ingresos por ventas: {total_ventas:,.2f} soles
✅ Ganancia estimada total: {ganancia_total:,.2f} soles

🏢 Ventas por sede:
{ventas_por_sede.to_string()}

⭐ Top 5 vendedores:
{top_vendedores.to_string()}
"""

with open("reporte.txt", "w", encoding="utf-8") as f:
    f.write(reporte)

# === GENERAR GRÁFICO DE VENTAS POR SEDE ===
ventas_por_sede.plot(kind="bar", title="Ventas por Sede", ylabel="Precio Venta Real (S/.)")
plt.tight_layout()
plt.savefig("grafico_ventas.png")
plt.close()

# === ENVIAR MENSAJE POR WHATSAPP (TWILIO) ===
client = Client(account_sid, auth_token)

message = client.messages.create(
    body=reporte,
    from_='whatsapp:+14155238886',
    to=twilio_to
)

print("Mensaje enviado con SID:", message.sid)
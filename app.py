import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Gestión de Delegados Pro", layout="centered")

st.title("Hub de Delegados")
st.markdown("---")

# 1. Conexión con Google Sheets
# Nota: En Streamlit Cloud, la URL se configura en "Secrets"
url = "TU_URL_DE_GOOGLE_SHEETS_AQUI"
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    df = conn.read(spreadsheet=url)

    # 2. Buscador y Filtros
    search_query = st.text_input("🔍 Buscar por nombre o centro...", "")

    # Filtrado lógico
    if search_query:
        df = df[df['Nombre y apellidos'].str.contains(search_query, case=False) |
                df['Centro'].str.contains(search_query, case=False)]

    # 3. Visualización de Delegados
    for index, row in df.iterrows():
        with st.container(border=True):
            # Layout de la tarjeta: Información vs Acción principal (Teléfono)
            col_info, col_call = st.columns([2, 1])

            with col_info:
                st.subheader(f"{row['Nombre y apellidos']}")
                st.caption(
                    f"🏢 {row['Centro']} | 📍 {row['Población']}, {row['Provincia']}")

                # Badges rápidos de cargos (si es TRUE, se muestra el icono)
                badges = []
                if row['Junta personal']:
                    badges.append("👥 Junta")
                if row['D. Prevencion']:
                    badges.append("🛡️ Prevención")
                if row['H.S']:
                    badges.append("🏥 H.S")
                if badges:
                    st.markdown(f"*{' | '.join(badges)}*")

            with col_call:
                # BOTÓN PRINCIPAL DE LLAMADA
                st.link_button(
                    f"📞 {row['Teléfono']}", f"tel:{row['Teléfono']}", use_container_width=True)

                # Opción de WhatsApp rápido si existe el campo o usando el mismo teléfono
                st.link_button(
                    "💬 Slack", f"{row['SLACK']}", use_container_width=True)

            # 4. Sección desplegable para datos secundarios
            with st.expander("Ver detalles completos y logística"):
                c1, c2 = st.columns(2)
                with c1:
                    st.write("**Contacto Sindical:**")
                    st.write(f"📞 Sind: {row['Telefono sindicato']}")
                    st.write(f"📠 Ext: {row['Exten Sind']}")
                    st.write(f"📧 {row['Mail']}")
                with c2:
                    st.write("**Datos de Envío:**")
                    st.write(f"🏠 {row['Dirección de envío']}")
                    st.write(f"📮 CP: {row['Código Postal']}")
                    st.write(f"🔑 Contraseña: `{row['Contraseña envios']}`")

                st.divider()
                st.caption(
                    f"Comunidad: {row['Comunidad Autonoma']} | Nombramiento: {row['NOMBRAMIENTO']}")

except Exception as e:
    st.error("Error al conectar con Google Sheets. Revisa la URL y los permisos.")
    st.write(e)


import streamlit as st
import geopandas as gpd
import folium
from folium.features import GeoJsonTooltip
from streamlit_folium import folium_static
from branca.element import Template, MacroElement

# Judul Dashboard
st.set_page_config(layout="wide")
st.title("Dashboard Klasifikasi Desa/Kelurahan - DDAC 2025 - AD/ART Team")
st.markdown("Visualisasi Peta Tematik Tingkat Pembangunan & Aksesibilitas Terhadap Fasilitas Umum di Level Kelurahan/Desa Provinsi Kalimantan Timur")

# Load shapefile klaster desa
shapefile_path = "DataDashboard.shp"
desa_gdf = gpd.read_file(shapefile_path)
desa_gdf = desa_gdf.dropna(subset=["prediksi", "NAMOBJ"])

# Warna & label
label_dict = {
    "kelas2": "Maju",
    "kelas3": "Cukup Maju",
    "kelas1": "Cukup Terbatas",
    "kelas4": "Terbatas"
}
color_dict = {
    "kelas2": "#213448",
    "kelas3": "#547792",
    "kelas1": "#94B4C1",
    "kelas4": "#ECEFCA"
}
desa_gdf["label"] = desa_gdf["prediksi"].map(label_dict)
desa_gdf["warna"] = desa_gdf["prediksi"].map(color_dict)

# Buat peta dasar
m = folium.Map(
    location=[-0.5, 116.5],
    zoom_start=7.0,
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    attr="Esri"
)

# Tambahkan layer GeoJSON
folium.GeoJson(
    desa_gdf,
    style_function=lambda feature: {
        'fillColor': feature['properties']['warna'],
        'color': 'white',
        'weight': 1,
        'fillOpacity': 0.7,
    },
    tooltip=GeoJsonTooltip(
        fields=["NAMOBJ", "WADMKK", "label"],
        aliases=["Desa/Kelurahan:","Kab/Kota:", "Kategori Klaster:"],
        localize=True
    )
).add_to(m)

# Dropdown pilihan fasilitas
pilihan_fasilitas = st.selectbox("Pilih jenis fasilitas yang ingin ditampilkan:", (
    "", "TK", "SD", "SMP", "SMA", "Pasar", "Minimarket dan Kios", "Rumah Sakit", "Puskesmas & Klinik"
))

fasilitas_paths = {
    "TK": "Jenjang_TK.shp",
    "SD": "SD_MI.shp",
    "SMP": "SMP_MTS.shp",
    "SMA": "SMA_SMK_MA.shp",
    "Pasar": "Titik Pasar.shp",
    "Minimarket dan Kios": "Titik Minimarket & Kios.shp",
    "Rumah Sakit": "Titik RS.shp",
    "Puskesmas & Klinik": "Titik Puskesmas dan Klinik.shp"
}


warna_titik = {
    "TK": "#e41a1c",
    "SD": "#377eb8",
    "SMP": "#4daf4a",
    "SMA": "#984ea3",
    "Pasar": "#ff7f00",
    "Minimarket dan Kios": "#ffff33",
    "Rumah Sakit": "#a65628",
    "Puskesmas & Klinik": "#f781bf"
}

if pilihan_fasilitas in fasilitas_paths:
    titik_gdf = gpd.read_file(fasilitas_paths[pilihan_fasilitas])
    for _, row in titik_gdf.iterrows():
        lokasi = [row.geometry.y, row.geometry.x]
        nama = row.get("Nama", "Tanpa Nama")
        popup_text = f"<b>Nama:</b> {nama}"
        folium.CircleMarker(
            location=lokasi,
            radius=4,
            color=warna_titik.get(pilihan_fasilitas, "blue"),
            fill=True,
            fill_opacity=0.8,
            popup=popup_text
        ).add_to(m)

legend_html = '''
<div style="
    font-size:14px;
    background-color: white;
    border:2px solid grey;
    padding: 10px;
    width: fit-content;
    box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
">
<b>Legenda Klaster:</b><br>
<i style="background: #213448; width: 15px; height: 15px; display:inline-block; margin-right: 8px;"></i> Maju<br>
<i style="background: #547792; width: 15px; height: 15px; display:inline-block; margin-right: 8px;"></i> Cukup Maju<br>
<i style="background: #94B4C1; width: 15px; height: 15px; display:inline-block; margin-right: 8px;"></i> Cukup Terbatas<br>
<i style="background: #ECEFCA; width: 15px; height: 15px; display:inline-block; margin-right: 8px;"></i> Terbatas
</div>
'''
import streamlit.components.v1 as components
components.html(legend_html, height=180)

# CSS & peta ditampilkan di tengah
st.markdown(
    '''
    <style>
    .map-container {
        display: flex;
        justify-content: center;
        align-items: center;
    }
    .folium-map {
        width: 100%;
        max-width: 900px;
        height: 650px;
    }
    </style>
    ''',
    unsafe_allow_html=True
)
st.markdown('<div class="map-container">', unsafe_allow_html=True)
folium_static(m, width=1100, height=700)
st.markdown('</div>', unsafe_allow_html=True)

# Membaca file shapefile untuk setiap kategori
gdf_tk = gpd.read_file("Jenjang_TK.shp")
gdf_sd = gpd.read_file("SD_MI.shp")
gdf_smp = gpd.read_file("SMP_MTS.shp")
gdf_sma = gpd.read_file("SMA_SMK_MA.shp")
gdf_pasar = gpd.read_file("Titik Pasar.shp")
gdf_minimarket = gpd.read_file("Titik Minimarket & Kios.shp")
gdf_rs = gpd.read_file("Titik RS.shp")
gdf_puskesmas = gpd.read_file("Titik Puskesmas dan Klinik.shp")

# Ambil jumlah masing-masing
tk = len(gdf_tk)
sd = len(gdf_sd)
smp = len(gdf_smp)
sma = len(gdf_sma)
pasar = len(gdf_pasar)
minimarket = len(gdf_minimarket)
rs = len(gdf_rs)
puskes = len(gdf_puskesmas)

import streamlit as st

st.markdown("## Jumlah Fasilitas Terdata")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(label="Fasilitas TK", value=tk)

with col2:
    st.metric(label="Fasilitas SD Sederajat", value=sd)

with col3:
    st.metric(label="Fasilitas SMP Sederajat", value=smp)

with col4:
    st.metric(label="Fasilitas SMA Sederajat", value=sma)

col5, col6, col7, col8 = st.columns(4)

with col5:
    st.metric(label="Fasilitas Pasar", value=pasar)

with col6:
    st.metric(label="Fasilitas Minimarket & Kios", value=minimarket)

with col7:
    st.metric(label="Fasilitas RS", value=rs)

with col8:
    st.metric(label="Fasilitas Puskesmas & Klinik", value=puskes)

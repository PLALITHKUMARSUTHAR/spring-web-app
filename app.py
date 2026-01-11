import streamlit as st
import math
import pandas as pd

st.set_page_config(page_title="Helical Spring Design", layout="centered")

st.title("Helical Compression Spring Design Calculator")
st.write("Design of Machine Elements – Web Interface")

W = st.number_input("Load W (N)", value=500.0)
tau_allow_MPa = st.number_input("Allowable shear stress τ (MPa)", value=400.0)
G = st.number_input("Modulus of rigidity G (Pa)", value=8e10, format="%.2e")
C = st.number_input("Spring index C (D/d)", value=8.0)
delta_mm = st.number_input("Required deflection δ (mm)", value=25.0)
end_type = st.selectbox("End type", ["plain", "squared", "squared_ground"])

if st.button("CALCULATE DESIGN"):

    tau_allow = tau_allow_MPa * 1e6
    delta = delta_mm / 1000
    density = 7850
    g = 9.81

    standard_diameters = [
        0.008,0.009,0.010,0.011,0.012,
        0.014,0.016,0.018,
        0.020,0.022,0.025,0.028,0.030,
        0.032,0.035,0.040
    ]

    d_min = math.sqrt((8 * W * C) / (math.pi * tau_allow))
    d_choices = [d for d in standard_diameters if d >= d_min]
    if not d_choices:
        d_choices = [d_min]

    rows = []

    for d in d_choices[:5]:
        D = C * d
        Kw = (4*C - 1)/(4*C - 4) + 0.615/C
        tau_max = Kw * (8 * W * D) / (math.pi * d**3)
        tau_max_MPa = tau_max / 1e6
        n = (delta * G * d**4) / (8 * W * D**3)
        nt = n + 2 if end_type != "plain" else n
        Ls = nt * d
        Lf = Ls + delta + 0.15 * delta
        pitch = (Lf - 2*d) / n

        wire_length = math.pi * D * nt
        volume = wire_length * (math.pi * d**2 / 4)
        mass = density * volume
        weight_kN = (mass * g) / 1000
        FoS = tau_allow / tau_max

        rows.append([
            round(d*1000,2),
            round(D*1000,2),
            round(tau_max_MPa,2),
            round(FoS,2),
            round(n,2),
            round(nt,2),
            round(Ls*1000,2),
            round(Lf*1000,2),
            round(pitch*1000,2),
            round(weight_kN,3)
        ])

    df = pd.DataFrame(rows, columns=[
        "Wire dia (mm)",
        "Mean dia (mm)",
        "Max stress (MPa)",
        "Factor of Safety",
        "Active coils",
        "Total coils",
        "Solid length (mm)",
        "Free length (mm)",
        "Pitch (mm)",
        "Spring weight (kN)"
    ])

    st.dataframe(df)

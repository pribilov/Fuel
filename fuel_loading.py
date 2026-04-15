import streamlit as st
import math
from datetime import date

st.set_page_config(page_title="Fuel Loading", page_icon="⛽", layout="centered")

st.title("⛽ Fuel Order")

# ─────────────────────────────────────────
# FLIGHT INFORMATION
# ─────────────────────────────────────────
#st.subheader("Flight Information")
#c1, c2, c3 = st.columns(3)
#with c1:
 #   station  = st.text_input("Station")
  #  flight   = st.text_input("Flight")
#with c2:
 #   fl_date  = st.date_input("Date", value=date.today())
  #  from_to  = st.text_input("From / To", placeholder="e.g. LIM-BOG")
#with c3:
 #   ac_reg   = st.text_input("A/C Reg", placeholder="e.g. OB-2034")

#st.divider()

# ─────────────────────────────────────────
# FUEL PARAMETERS
# ─────────────────────────────────────────
st.subheader("Fuel Parameters")
c1, c2 = st.columns(2)
with c1:
    density = st.number_input(
        "Density (kg/L)",
        min_value=0.001, max_value=1.0,
        value=0.800, step=0.001, format="%.3f"
    )
with c2:
    gamma = density * 3.786
    st.metric("Gamma  (density × 3.786)", f"{gamma:.4f}")

st.divider()

# ─────────────────────────────────────────
# FUEL PLAN  (coordinator + captain)
# ─────────────────────────────────────────
#st.subheader("Fuel Plan")
#c1, c2 = st.columns(2)
#with c1:
 #   takeoff_fuel = st.number_input("Take Off Fuel (kg)", min_value=0, value=0, step=10)
  #  taxi_fuel    = st.number_input("Taxi Fuel (kg)",     min_value=0, value=0, step=10)
#with c2:
 #   block_fuel = takeoff_fuel + taxi_fuel
  #  st.metric("Block Fuel (kg)  [auto]", f"{block_fuel:,}")

c1, c2 = st.columns(2)
with c1:
    captain = st.number_input(
        "Captain (kg)",
        min_value=0,
        value=int(block_fuel),
        step=10,
        help="El capitán puede solicitar más combustible que el block fuel del coordinador."
    )
with c2:
    remain = st.number_input("Remain (kg)", min_value=0, value=0, step=10)

st.divider()

# ─────────────────────────────────────────
# CALCULATED FUELING VALUES
# ─────────────────────────────────────────
st.subheader("To Be Fueled")

to_be_kg  = captain - remain
to_be_lts = to_be_kg / density if density > 0 else 0
gal_exact  = to_be_kg / gamma  if gamma  > 0 else 0
gal_up     = math.ceil(gal_exact / 100) * 100   # round up to next 100

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("To Be Fueled (kg)", f"{to_be_kg:,}")
with c2:
    st.metric("To Be Fueled (L)",  f"{to_be_lts:,.1f}")
with c3:
    st.metric("Request to Truck (gal ↑100)", f"{gal_up:,}",
              delta=f"exact: {gal_exact:,.1f}", delta_color="off")

st.divider()

# ─────────────────────────────────────────
# TRUCK READING  (what the truck screen shows)
# ─────────────────────────────────────────
st.subheader("Truck Reading")
gal_truck = st.number_input(
    "Gallons shown on truck screen",
    min_value=0, value=0, step=1
)

fueled_lts  = gal_truck * 3.786
diff_fueled = to_be_lts - fueled_lts   # positive = under-fueled, negative = over-fueled

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Fueled (L)", f"{fueled_lts:,.1f}")
with c2:
    color = "normal" if diff_fueled == 0 else ("inverse" if diff_fueled < 0 else "off")
    st.metric("Difference of Fueled (L)", f"{diff_fueled:,.1f}", delta_color=color)
with c3:
    if diff_fueled < 0:
        st.warning(f"⚠️ Se cargaron **{abs(diff_fueled):,.1f} L** de más.")
    elif diff_fueled > 0:
        st.info(f"ℹ️ Faltan **{diff_fueled:,.1f} L** por cargar.")
    else:
        st.success("✅ Carga exacta.")

# ─────────────────────────────────────────
# SUMMARY TABLE  (optional quick review)
# ─────────────────────────────────────────
